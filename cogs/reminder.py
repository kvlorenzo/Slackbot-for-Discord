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
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def remind(self, ctx):
        member_dict = {
            "server_id": ctx.message.server.id,
            "channel_id": ctx.message.channel.id,
            "user_id": ctx.message.author.id
        }
        await self.client.say("Remind command called")


def setup(client):
    client.add_cog(Reminder(client))
