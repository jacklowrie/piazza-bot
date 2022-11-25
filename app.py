import os
from signal import signal, SIGINT
from sys import exit

from slack_bolt import App
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.installation_store.sqlalchemy import SQLAlchemyInstallationStore
from slack_sdk.oauth.state_store.sqlalchemy import SQLAlchemyOAuthStateStore

import sqlalchemy
from sqlalchemy.engine import Engine

import re

import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

db_host, db_user, db_pass, db_name = (
    os.environ.get("DB_HOST"),
    os.environ.get("DB_USER"),
    os.environ.get("DB_PASS"),
    os.environ.get("DB_NAME")
)

client_id, client_secret, signing_secret = (
    os.environ["SLACK_CLIENT_ID"],
    os.environ["SLACK_CLIENT_SECRET"],
    os.environ["SLACK_SIGNING_SECRET"],
)

connection = f"mysql+mysqldb://{db_user}:{db_pass}@{db_host}/{db_name}"
print(connection)

engine: Engine = sqlalchemy.create_engine(connection)
installation_store = SQLAlchemyInstallationStore(
    client_id=client_id,
    engine=engine,
    logger=logger,
)
oauth_state_store = SQLAlchemyOAuthStateStore(
    expiration_seconds=120,
    engine=engine,
    logger=logger,
)

try:
    engine.execute("select count(*) from slack_bots")
except Exception as e:
    installation_store.metadata.create_all(engine)
    oauth_state_store.metadata.create_all(engine)

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=signing_secret,
    installation_store=installation_store,
    oauth_settings=OAuthSettings(
        client_id=client_id,
        client_secret=client_secret,
        state_store=oauth_state_store,
    ),
)
cache = {}

error = "Sorry, the forum id hasn't been set! "
error += "You can set it via slash command:\n"
error += "`/piazza-update-id [course_id]`\n"
error += "You can find the course id in any url on your piazza forum. "
error += "it'll be the long alphanumeric string."

base_url = "https://piazza.com/class/"


# Provides a means of setting the forum ID from a running app.
@app.command("/piazza-update-id")
def update_forum_id(ack, respond, command, context):
    global cache
    ack()

    workspace = context['team_id']
    forum_id = command['text']

    # update in mem
    cache[workspace] = forum_id

    respond(f"Updated forum! new id is {forum_id}", )


@app.message("thunder")
def post_link(say):
    say("lightning")


# Listens for any message with a piazza tag in it. Piazza tags take the form
# "@123", where the number is the id of a post on Piazza.
#
# https://regex101.com/r/eMmguY/1
@app.message(re.compile(r"@(\d+\b)"))
def post_link(say, context, event, client):
    global cache
    forum_id = cache.get(context["team_id"], None)

    if forum_id is None:
        client.chat_postEphemeral(
            text=error,
            channel=context["channel_id"],
            user=context["user_id"]
        )
        return

    posts_url = base_url + forum_id + "/post/"

    # build message contents
    text = ""
    for match in context['matches']:
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


# exit handler
def cleanup(signal_received, frame):
    print("\nShutting down PiazzaBot...")
    print("goodbye!")
    exit(0)


# Run the app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
