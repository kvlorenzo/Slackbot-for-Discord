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
    async def response(self, ctx, task="help", *args):
        member_dict = {
            "server_id": ctx.message.server.id,
            "channel_id": ctx.message.channel.id,
            "user_id": ctx.message.author.id
        }
        await self.parse_args(member_dict, args)
        if task == "create":
            '''TODO - PARSE ARGUMENT AND ADD TO DATABASE'''
        elif task == "delete":
            '''TODO - SEARCH MESSAGE IN DATABASE TO DELETE'''
        elif task == "list":
            '''TODO - PAGINATE THE MESSAGES IN THE CURRENT SERVER'''
        elif task == "clear":
            '''TODO - REMOVE ALL MESSAGES FROM SERVER IN DATABASE'''
        else:
            '''TODO - CREATE EMBEDDED MESSAGE FOR HELP'''
        await self.client.say("Response command called")

    async def parse_args(self, member_dict, args):
        if len(args) > 2:
            await self.create_help_msg()
            return
        msg = args[0]
        response = args[1]
        # TODO: CALL THE ADD TO DATABASE FUNCTION HERE

    async def create_help_msg(self):
        await self.client.say("TODO: Create help message here")


def setup(client):
    client.add_cog(Response(client))
