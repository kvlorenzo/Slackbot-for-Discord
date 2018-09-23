import sys

from database import delete_from_db
from database import insert_to_db
from database import query

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
            await self.parse_del_args(member_dict["server_id"], args)
        elif task == "list":
            '''TODO - PAGINATE THE MESSAGES IN THE CURRENT SERVER'''
        elif task == "clear":
            await self.clear_responses(member_dict["server_id"])
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

    async def parse_del_args(self, server_id, args):
        if not args or len(args) < 2:
            await self.create_help_msg()
            return
        deletion = delete_from_db.Deletion("database/server.db")
        msg_type = args[0]
        input_str = " ".join(args[1:])
        if msg_type == "message":
            if not deletion.del_msg(server_id, input_str):
                err_str = "Error. Can't find the message: " + input_str
                await self.client.say(err_str)
            else:
                await self.client.say("Message deleted")
        elif msg_type == "response":
            if not deletion.del_response(server_id, input_str):
                err_str = "Error. Can't find the response: " + input_str
                await self.client.say(err_str)
            else:
                await self.client.say("Response deleted")
        else:
            await self.create_help_msg()

    async def on_message(self, message):
        # This prevents bot from reading its own messages in on_message
        if not message.author.bot:
            q = query.Query("database/server.db")
            response = q.get_msg_response(message.server.id, message.content)
            if response is not None:
                await self.client.send_message(message.channel, response)

    async def clear_responses(self, server_id):
        deletion = delete_from_db.Deletion("database/server.db")
        if not deletion.del_all_responses(server_id):
            await self.client.say("Error: Could not clear the responses")
        else:
            await self.client.say("Responses cleared.")

    async def create_help_msg(self):
        await self.client.say("TODO: Add help message here")


def setup(client):
    client.add_cog(Response(client))
