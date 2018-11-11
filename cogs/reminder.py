import asyncio
import math
import sys

import dateparser

import config
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


class Reminder:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def remind(self, ctx, task_or_recipient="help", msg="", send_time=""):
        member_dict = {
            "server_id": ctx.message.server.id,
            "channel_id": ctx.message.channel.id,
            "user_id": ctx.message.author.id
        }
        if task_or_recipient == "delete":
            await self.del_reminder(member_dict["server_id"], msg)
        elif task_or_recipient == "clear":
            await self.clear_reminders(member_dict["server_id"])
        elif task_or_recipient == "list":
            await self.display_list(member_dict["server_id"], msg)
        else:
            # The task_or_recipient, if mentioning a channel or user, will
            # appear in the form of this:
            # <@12345> for users or <#12345> for channels
            # To distinguish between the two, we parse out the second character
            # to check if it is either an @ or a #
            recipient_symbol = task_or_recipient[1]
            mentions = []
            if recipient_symbol == "@":
                mentions = ctx.message.mentions
            elif recipient_symbol == "#":
                mentions = ctx.message.channel_mentions
            else:
                await self.create_help_msg()
                return
            recipient_id = await self.parse_recipient(task_or_recipient[2:-1],
                                                      mentions)
            if recipient_id is not None:
                await self.update_reminder(member_dict, ctx.message.server,
                                           recipient_symbol, recipient_id,
                                           msg, send_time)

    async def update_reminder(self, member_dict, server, recipient_symbol,
                              recipient_id, msg, send_time):
        send_time_utc = dateparser.parse(send_time)
        if send_time is None:
            err_str = "Sorry. I couldn't understand the time. Please try again."
            await self.client.say(err_str)
            return
        entry = insert_to_db.Entry(config.db, member_dict)
        entry.add_reminder(recipient_symbol, recipient_id, msg, send_time_utc)
        if recipient_symbol == "#":
            recipient = str(server.get_channel(recipient_id))
        else:
            recipient = str(server.get_member(recipient_id))
        result_str = "Will remind " + recipient + " at " + \
                     str(send_time_utc.ctime()) + " (UTC time) " + msg
        await self.client.say(result_str)

    async def parse_recipient(self, recipient, mentions):
        for mention in mentions:
            if mention.id == recipient:
                return recipient
        return None

    async def send_reminders(self):
        await self.client.wait_until_ready()
        q = query.Query(config.db)
        deletion = delete_from_db.Deletion(config.db)
        while not self.client.is_closed:
            # Reminders tuple: {recipient_type, recipient_id, message}
            reminders = q.get_current_reminders()
            for reminder in reminders:
                if reminder[0] == '@':
                    recipient = await self.client.get_user_info(reminder[1])
                    await self.client.send_message(recipient, reminder[2])
                    deletion.del_user_reminder(reminder[1], reminder[2])
                else:
                    recipient = self.get_channel(reminder[1])
                    server_id = recipient.server.id
                    await self.client.send_message(recipient, reminder[2])
                    deletion.del_reminder(server_id, reminder[2])
            await asyncio.sleep(10)

    async def del_reminder(self, server_id, msg):
        if not msg:
            await self.create_help_msg()
            return
        deletion = delete_from_db.Deletion(config.db)
        if not deletion.del_reminder(server_id, msg):
            err_str = "Error. Can't find the message: " + msg
            await self.client.say(err_str)
        else:
            await self.client.say("Message deleted")

    async def clear_reminders(self, server_id):
        deletion = delete_from_db.Deletion(config.db)
        if not deletion.del_all_reminders(server_id):
            await self.client.say("Error: Could not clear the responses")
        else:
            await self.client.say("Responses cleared.")

    async def display_list(self, server_id, args):
        # Hard-coded value that can change in the future
        msg_per_pg = 10
        q = query.Query(config.db)

        # Reminders will hold a tuple of all the messages and times like so:
        # ((time1, reminder1), (time2, reminder2), (time3, reminder3))
        reminders = q.get_all_server_reminders(server_id)
        print(reminders)
        rem_len = len(reminders)
        if rem_len < 1:
            await self.client.say("No responses found")
            return

        # pg is current page number - if over the page limit, default = last pg
        pg = 1
        if args and str(args[0]).isdigit():
            pg = min(math.floor(rem_len / msg_per_pg), int(args[0]))
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
        items_in_pg = min(msg_per_pg, rem_len - start_idx)

        msg_list = ""
        for i in range(start_idx, start_idx + items_in_pg):
            msg_list += reminders[i][0] + ": " + \
                        reminders[i][1] + "\n\n"
        embed = discord.Embed(
            title="Reminders",
            description="\u200b",
            colour=discord.Colour.orange()
        )
        embed.add_field(name="\u200b", value=msg_list, inline=False)
        embed.set_footer(text="Page " + str(pg) + " of " +
                              str(math.ceil(rem_len / items_in_pg)))
        await self.client.say(embed=embed)

    async def create_help_msg(self):
        embed = discord.Embed(
            title="Help page for remind commands",
            description="\u200b",
            colour=discord.Colour.orange()
        )
        embed.add_field(name="Help", value="/remind help", inline=False)
        embed.add_field(name="Create a Reminder",
                        value="/remind [\"user/channel\"] [\"reminder\"] "
                              "[\"time\"]\n"
                              "(without brackets - NOTE: reminder & time "
                              "must be in quotations)\n\n",
                        inline=False)
        embed.add_field(name="Delete a Reminder",
                        value="/remind delete [\"remind message\"]\n"
                              "(without brackets, quotes required)",
                        inline=False)
        embed.add_field(name="Display All Active Reminders",
                        value="/remind list",
                        inline=False)
        embed.add_field(name="Clear All Active Reminders",
                        value="/remind clear",
                        inline=False)
        await self.client.say(embed=embed)

    def get_channel(self, channel_id):
        channels = self.client.get_all_channels()
        for channel in channels:
            if channel.id == str(channel_id):
                return channel
        return None


def setup(client):
    client.add_cog(Reminder(client))
    client.loop.create_task(Reminder(client).send_reminders())
