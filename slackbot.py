import sys

import config

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

TOKEN = config.TOKEN
COGS = config.cogs

bot = commands.Bot(command_prefix=config.cmd_prefix)


@bot.event
async def on_ready():
    print("Bot connected")
    print("------")
    print("Bot name:", bot.user.name)
    print("Bot id:", bot.user.id)
    print("Number of Servers:", len(bot.servers))
    print("Number of Channels:", len(list(bot.get_all_channels())))
    print("Number of Members:", len(list(bot.get_all_members())))


@bot.command()
async def load(cog):
    try:
        bot.load_extension(cog)
        print("Loaded {}".format(cog))
    except Exception as err:
        print("{} failed to load [{}]".format(cog, err))


@bot.command()
async def unload(cog):
    try:
        bot.unload_extension(cog)
        print("Loaded {}".format(cog))
    except Exception as err:
        print("{} failed to load [{}]".format(cog, err))


if __name__ == "__main__":
    for c in COGS:
        try:
            bot.load_extension(c)
        except Exception as e:
            print("{} failed to load [{}]".format(c, e))
    bot.run(TOKEN)
