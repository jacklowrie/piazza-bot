# PiazzaBot
PiazzaBot is a simple slack bot that makes discussing posts on Piazza easier.
When a post is mentioned by ID, PiazzaBot will respond with a link to that
post.

<a href="https://slack.com/oauth/v2/authorize?client_id=4080246706931.4080375380706&scope=chat:write.public,chat:write,channels:history,groups:history,im:history,mpim:history,commands&user_scope="><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcSet="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>

<img src="https://github.com/jacklowrie/piazza-bot/blob/main/demo.gif" width=100% height=100%>

**\*Note**: I am not affiliated with or endorsed by Piazza or Slack in any way. Neither
is this bot.

## Installation (adding to your workspace, and updates)
This app isn't registered through the slack app directory. For now, it's meant
to be used by one workspace per install/instance. To add to your workspace,
we need to do two things:
1. Register a new app in your workspace, and add the appropriate permissions.
2. Set the app up on your host.
3. Once PiazzaBot is up and running, add it to any channel you want to use in.

### Register the app (3-5 min)
1. _[Register a new app](https://api.slack.com/apps?new_app=1) for your
workspace._ Open that link (in a new window/tab). Choose to register the app
from manifest, then copy & paste everything from the `slack-manifest.json`
file in this repo into the window (make sure it's the `json` window and not
the `yaml` window). Click through and confirm the app. This should take you
to the "basic information" settings page.
2. _Install to workspace._ Click the install to workspace button.
3. _Add the piazza icon._ From the "basic information" page, at the bottom
under "display information", upload the icon from this repo as the app icon.
4. _Generate and save App-Level Token._ Under "App Level Tokens", generate a
token with read/write authorizations. Note the token, as we'll need it to set
the app up on your host.
5. _save bot token._ Finally, note the bot token. In the left-side nav, click
into "Features"->"Oauth & Permissions", and note the Bot User OAuth Token.

### Host the app (3-5 min)

1. _Clone this repo._ This is the easiest way to handle updates, since you
can just pull from `main` and restart the app whenever there's an update.
Alternatively, if you need to modify the app for your workspace, fork instead.
2. _Install dependencies._ Set up a virtual environment, and install the
required modules from `requirements.txt`. There's an install script `install.sh`
which contains the commands you'll need to run. Either run each command
individually, or try running the script **make sure python3 is installed on
your system before running**.
3. _Add tokens._ create a `.env` file from `.env-sample` and add the
corresponding tokens you noted when registering the app.
4. _Add Course ID._ Go to your course's dashboard (if you're viewing a question,
click the logo). add the long alphanumeric string to your `.env` as the `COURSE_ID`.
5. create new directory `data/` and a blank file `db.json` inside of it.
6. _Run the app._ Run the app! `python app.py`

## Contributing
Still thinking about the ideal workflow, however I'd like to keep PM on
GitHub for now. If you'd like to contribute, first of all, _thank you_!
Please first discuss the change you wish to make with the owners of this
repository, ideally via issue, before making a change or opening a pull request.
Take a look at the
[contribution guidelines ](https://github.com/jacklowrie/piazza-bot/blob/main/CONTRIBUTING.md)
for more.

## Development
PiazzaBot is built using [Slack's Bolt framework](https://github.com/SlackAPI/bolt-python).
As such, most developer documentation can be found there.

Because the app uses socket mode, it isn't really possible to have multiple
developers working on the bot in the same workspace. So, the best way to set
up this app for local development is to:
1. create a test workspace (so changes don't interrupt a real workspace)
2. Follow the installation instructions above, but register the app to that
workspace instead. Thanks to socket mode, you can run the app on your computer
and it will work in that test workspace!
