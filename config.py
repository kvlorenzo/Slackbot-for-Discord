# Settings for variables are set in config.py
# Variables that need setting are the following:
# - Token
# - Command prefix
# - Cogs
# - database - path and name


# To get the token for the bot, follow the website:
# https://github.com/Chikachi/DiscordIntegration/wiki/
#   How-to-get-a-token-and-channel-ID-for-Discord
# This will give you instructions for how to start a bot. After creating the
# bot, find the area that says "token," and copy and paste the token into the
# variable below
TOKEN = "https://github.com/kvlorenzo/Slackbot-for-Discord"

# The character that precedes every command used.
cmd_prefix = "/"

# The files that contain the commands
cogs = ["cogs.reminder", "cogs.response"]

# The path and name of the database
database_path = "database/"
database_name = "server.db"
db = database_path + database_name
