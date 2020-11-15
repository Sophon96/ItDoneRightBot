import os

from discord.ext import commands
import discord
import json
import os

# client = commands.Bot(command_prefix="!")


# loading credentials into environemnt
for item in json.load(open("settings.json")).items():
    os.environ[item[0]] = str(item[1])

client = commands.Bot(command_prefix=os.environ["DISCORD_BOT_TOKEN"])

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command
@commands.is_owner()
async def load(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

# https://www.youtube.com/watch?v=vQw8cFfZPx0
for cog in os.listdir("./cogs"):
    if cog.endswith('.py'):
        client.load_extension(f'cogs.{cog[:-3]}')

if __name__ == "__main__":
    client.run(os.environ["DISCORD_BOT_KEY"])
# vimming
