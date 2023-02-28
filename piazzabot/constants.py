import os
from urllib import parse

CLIENT_ID, CLIENT_SECRET, SIGNING_SECRET = (
    os.environ["SLACK_CLIENT_ID"],
    os.environ["SLACK_CLIENT_SECRET"],
    os.environ["SLACK_SIGNING_SECRET"],
)

DB_HOST, DB_USER, DB_PASS, DB_NAME = (
    os.environ.get("DB_HOST"),
    os.environ.get("DB_USER"),
    parse.quote_plus(os.environ.get("DB_PASS")),
    os.environ.get("DB_NAME")
)

BASE_URL = "https://piazza.com/class/"

ERROR_NO_FORUM_ID = "Sorry, the forum id hasn't been set! "
ERROR_NO_FORUM_ID += "You can set it via slash command:\n"
ERROR_NO_FORUM_ID += "`/piazza-update-id [course_id]`\n"
ERROR_NO_FORUM_ID += "You can find the course id in any url on your piazza forum. "
ERROR_NO_FORUM_ID += "it'll be the long alphanumeric string."
