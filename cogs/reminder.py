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


class Reminder:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def remind(self, ctx, *args):
        user = ctx.message.author
        channel = ctx.message.channel
        print(user, channel)
        await self.bot.say("Remind command called")


def setup(bot):
    bot.add_cog(Reminder(bot))
