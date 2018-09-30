import asyncio
import sys

import dateparser

import config
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
            """TODO: Create a method that deletes a reminder"""
        elif task_or_recipient == "clear":
            """TODO: Delete all reminders pertaining to user or channel"""
        elif task_or_recipient == "list":
            """TODO: List out all the reminders"""
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
                self.create_help_msg()
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
            self.create_help_msg()
            return
        entry = insert_to_db.Entry(config.db, member_dict)
        entry.add_reminder(recipient_symbol, recipient_id, msg, send_time_utc)
        if recipient_symbol == "#":
            recipient = str(server.channel(recipient_id))
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

    async def create_help_msg(self):
        await self.client.say("I am a help message. Make me.")

    async def send_reminders(self):
        print("Send reminders called")
        await self.client.wait_until_ready()
        while not self.client.is_closed:
            await self.client.say("I am a test reminder")
            print("Test")
            await asyncio.sleep(10)


def setup(client):
    client.add_cog(Reminder(client))
