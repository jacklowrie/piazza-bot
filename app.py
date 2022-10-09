import os
from dotenv import load_dotenv

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import re

# Make the app
load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

base_url = "https://piazza.com/class/%s" % os.environ.get("COURSE_ID")
posts_url = f"{base_url}/post/" 

# Listens to incoming messages that contain "hello"
# To learn available listener arguments, visit 
# https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
# https://regex101.com/r/eMmguY/1
@app.message(re.compile(r"@(\d+\b)"))
def post_link(say, context, event):
    for match in context['matches']:
        url = posts_url + match

        thread_ts = event.get("thread_ts", None)
        # say() sends a message to the channel where the event was triggered
        say(text=url, thread_ts=thread_ts)

# Run the app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()