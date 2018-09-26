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
    async def remind(self, ctx, task_or_recipient="help", msg="", time=""):
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
            recipient_info = self.parse_recipient(recipient_symbol,
                                                  task_or_recipient[2:-1],
                                                  mentions)
            if recipient_info is not None:
                self.update_reminder(member_dict, recipient_info, msg, time)

    async def update_reminder(self, member_dict, recipient_info, msg, time):
        """TODO: Add to sql database"""

    async def parse_recipient(self, recipient_symbol, recipient, mentions):
        recipient_list = [recipient_symbol]
        for mention in mentions:
            if mention == recipient:
                recipient_list.append(recipient)
        if len(recipient_list) <= 1:
            self.create_help_msg()
            return None
        return recipient_list

    async def create_help_msg(self):
        await self.client.say("I am a help message. Make me.")

def setup(client):
    client.add_cog(Reminder(client))
