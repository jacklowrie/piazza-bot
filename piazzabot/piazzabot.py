import logging
import os
import re

from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store.sqlalchemy import SQLAlchemyInstallationStore
from slack_sdk.oauth.state_store.sqlalchemy import SQLAlchemyOAuthStateStore

from sqlalchemy.orm import Session

from piazzabot.database import Base, Course, dbengine
from piazzabot.constants import CLIENT_ID, CLIENT_SECRET, SIGNING_SECRET, ERROR_NO_FORUM_ID, BASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
cache = {}

# Set up Oauth backend
installation_store = SQLAlchemyInstallationStore(
    client_id=CLIENT_ID,
    engine=dbengine,
    logger=logger
)
oauth_state_store = SQLAlchemyOAuthStateStore(
    expiration_seconds=120,
    engine=dbengine,
    logger=logger
)

try:
    dbengine.execute("select count(*) from slack_bots")
except Exception as e:
    installation_store.metadata.create_all(dbengine)
    oauth_state_store.metadata.create_all(dbengine)

Base.metadata.create_all(dbengine)

# Set up app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=SIGNING_SECRET,
    installation_store=installation_store,
    oauth_settings=OAuthSettings(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        state_store=oauth_state_store,
        scopes=[
            "chat:write.public",
            "chat:write",
            "channels:history",
            "groups:history",
            "im:history",
            "mpim:history",
            "commands"
        ]
    )
)
app_handler = SlackRequestHandler(app)


# Provides a means of setting the forum ID from a running app.
@app.command("/piazza-update-id")
def update_forum_id(ack, respond, command, context):
    logging.warning("in command handler.")
    global cache
    ack()

    workspace_id = context['team_id']
    forum_id = command['text']

    # update in mem
    cache[workspace_id] = forum_id
    logging.info(f"after cache insert. cache[{workspace_id}] should be {forum_id}, is {cache[workspace_id]}")
    c = Course(workspace=workspace_id, forum=forum_id)

    with Session(dbengine) as session:
        session.merge(c)
        session.commit()

    respond(f"Updated forum! new id is {forum_id}", )


# Listens for any message with a piazza tag in it. Piazza tags take the form
# "@123", where the number is the id of a post on Piazza.
#
# https://regex101.com/r/fBz50F/1
@app.message(re.compile(r'@(\d+[,|\ |\n|.|?|\r|\t]|\d+$)'))
def regex_message_match(say, context, event, client, logger, body):
    global cache
    forum_id = cache.get(context["team_id"], None)
    team_id = context["team_id"]
    logger.info(f"Match detected. Team ID: {team_id} Forum ID: {forum_id}")
    logger.info(body)

    if forum_id is None:
        first_match = context["matches"][0]
        logger.warning(f"Forum not set. First ID is: {first_match}")
        client.chat_postEphemeral(
            text=ERROR_NO_FORUM_ID,
            channel=context["channel_id"],
            user=context["user_id"]
        )
        return

    posts_url = BASE_URL + forum_id + "/post/"
    # build message contents
    text = ""
    for match in context['matches']:
        logger.info(f"match: {match}")
        url = posts_url + match
        text += f"<{url}|View post {match} on Piazza>\n"

    # send the message
    thread_ts = event.get("thread_ts", None)
    if thread_ts is None:
        say(
            text=text.strip("\n"),
            thread_ts=event.get("ts"),
            reply_broadcast=True
        )
    else:
        say(
            text=text.strip("\n"),
            thread_ts=thread_ts
        )
