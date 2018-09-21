import sys

from database import insert_to_db

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
        if task == "create":
            await self.parse_msg_and_response(member_dict, args)
        elif task == "delete":
            '''TODO - SEARCH MESSAGE IN DATABASE TO DELETE'''
        elif task == "list":
            '''TODO - PAGINATE THE MESSAGES IN THE CURRENT SERVER'''
        elif task == "clear":
            '''TODO - REMOVE ALL MESSAGES FROM SERVER IN DATABASE'''
        else:
            '''TODO - CREATE EMBEDDED MESSAGE FOR HELP'''

    async def parse_msg_and_response(self, member_dict, args):
        if len(args) != 2:
            await self.create_help_msg()
            return
        msg = args[0]
        response = args[1]
        entry = insert_to_db.Entry("database/server.db", member_dict)
        entry.add_response(msg, response)
        result_str = "Response added\n" + \
                     "Message: " + msg + "\n" + \
                     "Response: " + response
        await self.client.say(result_str)

    async def create_help_msg(self):
        await self.client.say("TODO: Add help message here")


def setup(client):
    client.add_cog(Response(client))
