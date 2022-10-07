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

# Listens for any message with a piazza tag in it. Piazza tags take the form
# "@123", where the number is the id of a post on Piazza.
# https://regex101.com/r/eMmguY/1
@app.message(re.compile(r"@(\d+\b)"))
def post_link(say, context):
    for match in context['matches']:
        url = posts_url + match
        # say() sends a message to the channel where the event was triggered
        say(url)

# Run the app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()