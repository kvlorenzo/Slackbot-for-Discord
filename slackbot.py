from discord.ext import commands

token = "NDg4OTU4ODAxMDUyMTcyMjkw.Dnjyvg.Ys7qQ2N_Jk-brciE3j5y4ONKVVM"

client = commands.Bot(command_prefix="/")


@client.event
async def on_ready():
    print("Bot connected")
    print("------")


client.run(token)
