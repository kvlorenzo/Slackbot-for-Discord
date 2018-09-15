import sys

try:
    from discord.ext import commands
except ImportError:
    commands = None
    print("Discord.py not installed on the computer.\n"
          "Read the documentation on the website:\n"
          "https://github.com/Rapptz/discord.py for installation instructions.")
    sys.exit(1)

token = "NDg4OTU4ODAxMDUyMTcyMjkw.Dnjyvg.Ys7qQ2N_Jk-brciE3j5y4ONKVVM"

client = commands.Bot(command_prefix="/")

@client.event
async def on_ready():
    print("Bot connected")
    print("------")

client.run(token)
