import math
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
            await self.display_list(member_dict["server_id"], args)
        elif task == "clear":
            await self.clear_responses(member_dict["server_id"])
        else:
            await self.create_help_msg()

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

    async def display_list(self, server_id, args):
        # Hard-coded value that can change in the future
        msg_per_pg = 1
        q = query.Query("database/server.db")

        # Responses will hold a tuple of all the messages and the corresponding
        # responses like so:
        # ((msg1, resp1), (msg2, resp2), (msg3, resp3))
        responses = q.get_all_responses(server_id)
        resp_len = len(responses)

        # pg is current page number - if over the page limit, default = last pg
        pg = 1
        if args and str(args[0]).isdigit():
            pg = min(math.floor(resp_len / msg_per_pg), int(args[0]))
            if pg <= 0:
                pg = 1

        # The start_idx is the index where the first item in the list will
        # be found in the tuple. It's calculated by multiplying the page number
        # by the messages per page and subtracting messages per page
        #  Ex. page 2 for 10 msg per page -> (2 * 10) - 10 = start at idx 10
        start_idx = (msg_per_pg * pg) - msg_per_pg
        # Calculates how many items will appear on the page. This will be the
        # default messages per page or less if the current page will hold less
        # items
        items_in_pg = min(msg_per_pg, resp_len - start_idx)

        msg_list = ""
        for i in range(start_idx, start_idx + items_in_pg):
            msg_list += "Message: " + responses[i][0] + "\n" + \
                        "Response: " + responses[i][1] + "\n\n"
        print(msg_list, "Length:", len(msg_list))
        embed = discord.Embed(
            title="Automatic responses",
            description="\u200b",
            colour=discord.Colour.orange()
        )
        embed.add_field(name="\u200b", value=msg_list, inline=False)
        embed.set_footer(text="Page " + str(pg) + " of " +
                              str(math.ceil(resp_len / items_in_pg)))
        await self.client.say(embed=embed)

    async def create_help_msg(self):
        embed = discord.Embed(
            title="Help page for response commands",
            description="\u200b",
            colour=discord.Colour.orange()
        )
        embed.add_field(name="Help", value="/response help", inline=False)
        embed.add_field(name="Create a Response",
                        value="/response create [\"message\"] [\"response\"]\n"
                              "(without brackets - NOTE: message and response "
                              "must be in quotations)\n\n",
                        inline=False)
        embed.add_field(name="Delete a Response by Message",
                        value="/response delete message [\"message\"]\n"
                              "(without brackets, quotes not required)\n\n",
                        inline=False)
        embed.add_field(name="Delete a Response by Response",
                        value="/response delete message [\"response\"]\n"
                              "(without brackets, quotes not required)",
                        inline=False)
        embed.add_field(name="Display all active responses",
                        value="/response list",
                        inline=False)
        await self.client.say(embed=embed)


def setup(client):
    client.add_cog(Response(client))
