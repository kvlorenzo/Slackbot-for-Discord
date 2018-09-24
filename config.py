# Settings for variables are set in config.py
# Variables that need setting are the following:
# - Token
# - Command prefix
# - database - path and name


# To get the token for the bot, follow the website:
# https://github.com/Chikachi/DiscordIntegration/wiki/
#   How-to-get-a-token-and-channel-ID-for-Discord
# This will give you instructions for how to start a bot. After creating the
# bot, find the area that says "token," and copy and paste the token into the
# variable below
TOKEN = "NDg4OTU4ODAxMDUyMTcyMjkw.Dnjyvg.Ys7qQ2N_Jk-brciE3j5y4ONKVVM"

# The character that precedes every command used.
cmd_prefix = "/"

cogs = ["cogs.reminder", "cogs.response"]

database_path = "database/"
database_name = "server.db"
db = database_path + database_name
