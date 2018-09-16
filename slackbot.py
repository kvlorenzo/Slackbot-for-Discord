import sys

try:
    import discord
    from discord.ext import commands
except ImportError:
    discord = None
    commands = None
    print("Discord.py not installed on the computer.\n"
          "Read the documentation on the website:\n"
          "https://github.com/Rapptz/discord.py for installation instructions.")
    sys.exit(1)

token = "NDg4OTU4ODAxMDUyMTcyMjkw.Dnjyvg.Ys7qQ2N_Jk-brciE3j5y4ONKVVM"

bot = commands.Bot(command_prefix="/")


@bot.event
async def on_ready():
    print("Bot connected")
    print("------")
    print("Bot name:", bot.user.name)
    print("Bot id:", bot.user.id)
    print("Number of Servers:", len(bot.servers))
    print("Number of Channels:", len(list(bot.get_all_channels())))
    print("Number of Members:", len(list(bot.get_all_members())))


bot.run(token)
