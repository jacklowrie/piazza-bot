import os
from dotenv import load_dotenv

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import re

# Make the app
load_dotenv()
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
url = "https://piazza.com/class/%s/post/" % os.environ.get("COURSE_ID")

# Listens to incoming messages that contain "hello"
# To learn available listener arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message(re.compile("(@\d*)"))
# @app.message(re.compile("(hi|hello|hey)"))
def message_hello(say, context):
    for match in context['matches']:
        number = match.replace('@','')
        post_url = url + number
        # say() sends a message to the channel where the event was triggered
        say(f"The number is {number}. the url is: {post_url}")


# Run the app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()