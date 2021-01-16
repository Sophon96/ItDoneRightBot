#!/usr/bin/python3

import sys
from discord.ext import commands
import discord
import json
import os

# loading credentials into environment
try:
    for item in json.load(open("settings.json")).items():
        os.environ[item[0]] = str(item[1])
except FileNotFoundError:
    print('Please make a settings.json!')
    exit(1)


client = commands.Bot(command_prefix=os.environ["DISCORD_BOT_PREFIX"])


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')


@client.command()
@commands.is_owner()
async def load(ctx, extension):
	client.load_extension(f"cogs.{extension}")


# https://www.youtube.com/watch?v=vQw8cFfZPx0
for cog in os.listdir("./cogs"):
	if cog.endswith('.py'):
		client.load_extension(f'cogs.{cog[:-3]}')


@client.command()
@commands.is_owner()
async def halt(ctx):
	"""
	kills the bot
	:param ctx:
	:return:
	"""

	embed = discord.Embed(title="Exiting")
	await ctx.send(embed=embed)
	print('Exited via Discord command')
	sys.exit(0)


@client.command()
@commands.is_owner()
async def restart(ctx):
	"""
	Restarts the bot
	"""

	await ctx.reply(content='\*\*\*  **Restarting**', mention_author=True)
	# TODO: Flush files
	# os.fsync()
	os.execv('run.py', sys.argv)
	exit(0)


@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		yeet = discord.Embed(title='Unknown command', color=0xfeffff, description=ctx.message.content)
		await ctx.reply(embed=yeet)
	elif isinstance(error, commands.NotOwner):
		await ctx.reply(content='You do not have sufficient permissions to execute this command. This incident will be '
																		'reported')
		print(f'!!! {ctx.author.name} ID={ctx.author.id} attempted to use a owner-only command.')


@client.command()
async def anna(ctx):
	"""
	anna
	:param ctx:
	:return:
	"""
	await ctx.message.delete()


if __name__ == "__main__":
	client.run(os.environ["DISCORD_BOT_KEY"])
# vimming
