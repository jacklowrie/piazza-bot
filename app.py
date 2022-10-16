import os
from dotenv import load_dotenv
from signal import signal, SIGINT
from sys import exit

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import logging

import re
from tinydb import TinyDB, Query

# Make the app
load_dotenv()
logging.basicConfig(level=logging.ERROR)

app = App(token = os.environ.get("SLACK_BOT_TOKEN"))
db = TinyDB('data/db.json')
Course = Query()

error = "Sorry, the forum id hasn't been set! "
error += "You can set it via slash command:\n"
error += "`/piazza-update-id [course_id]`\n"
error += "You can find the course id in any url on your piazza forum. "
error += "it'll be the long alphanumeric string."

base_url = "https://piazza.com/class/"


# Provides a means of setting the forum ID from a running app.
@app.command("/piazza-update-id")
def update_forum_id(ack, respond, command, context):
    ack()
    
    team_id = context['team_id']
    forum_id = command['text']
    
    db.upsert(
        {'workspace': team_id, 'forum': forum_id },
        Course.workspace == team_id
    )

    respond(f"Updated forum! new id is {forum_id}",)


# Listens for any message with a piazza tag in it. Piazza tags take the form
# "@123", where the number is the id of a post on Piazza.
# 
# https://regex101.com/r/eMmguY/1
@app.message(re.compile(r"@(\d+\b)"))
def post_link(say, context, event, client):
    c = db.get((Course.workspace == context["team_id"]))

    if c == None:
        client.chat_postEphemeral(
            text = error,
            channel = context["channel_id"],
            user = context["user_id"]
        )
        return
    posts_url = base_url + c["forum"] + "/post/"
    # build message contents
    text = ""
    for match in context['matches']:
        url = posts_url + match
        text += f"<{url}|View post {match} on Piazza>\n"

    # send the message
    thread_ts = event.get("thread_ts", None)
    if thread_ts == None:
        say(
            text = text.strip("\n"), 
            thread_ts = event.get("ts"), 
            reply_broadcast = True
        )
    else:
        say(
            text = text.strip("\n"), 
            thread_ts = thread_ts
        )


# exit handler
def cleanup(signal_received, frame):
    print("\nShutting down PiazzaBot...")
    db.close()
    print("goodbye!")
    exit(0)



# Run the app
if __name__ == "__main__":
    signal(SIGINT, cleanup)
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
