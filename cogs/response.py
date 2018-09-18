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


class Response:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def response(self, ctx, *args):
        user = ctx.message.author
        channel = ctx.message.channel
        print(user, channel)
        await self.client.say("Response command called")


def setup(client):
    client.add_cog(Response(client))
