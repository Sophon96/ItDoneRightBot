#!/usr/bin/python3

import logging
from time import sleep
from discord.ext import commands
import discord
import json
import os
import subprocess

logging.basicConfig(level=logging.INFO)
# loading credentials into environment
try:
    for item in json.load(open("settings.json")).items():
        os.environ[item[0]] = str(item[1])
except FileNotFoundError:
    print('Please make a settings.json!')
    exit(1)

client = commands.AutoShardedBot(command_prefix=os.environ["DISCORD_BOT_PREFIX"])

halt_state = False

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.reply(f'Successfully unloaded cog {extension}.')


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.reply(f'Successfully loaded cog {extension}.')


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.reload_extension(f'cogs.{extension}')
    await ctx.reply(f'Successfully reloaded cog {extension}.')


@client.command()
@commands.is_owner()
async def reload_all(ctx):
    for _cog in os.listdir("./cogs"):
        if cog.endswith('.py'):
            client.reload_extension(f'cogs.{cog[:-3]}')
    await ctx.reply('Successfully reloaded all cogs.')


@reload_all.error
@reload.error
@load.error
@unload.error
async def cog_load_error(ctx, error):
    ctx.reply(f'An error occurred which trying to load/unload/reload cog(s)! Error:```py\n{error}```')


# https://www.youtube.com/watch?v=vQw8cFfZPx0
for cog in os.listdir("./cogs"):
    if cog.endswith('.py'):
        client.load_extension(f'cogs.{cog[:-3]}')


@client.command()
@commands.is_owner()
async def gp(ctx):
    """
    Update the bot by git pull
    :param ctx:
    :return:
    """
    a = subprocess.check_output('git pull origin master', shell=True).decode('utf-8')
    embed = discord.Embed(title="Results", color=0xFEFFFF, description=a)
    await ctx.reply(embed=embed)


@client.command(name='halt', aliases=['stop', 'shutdown'])
@commands.is_owner()
async def halt(ctx):
    """
    kills the bot
    :param ctx:
    :return:
    """

    global halt_state
    embed = discord.Embed(title="Exiting", color=0xFEFFFF)
    await ctx.send(embed=embed)
    # print('Exited via Discord command')
    halt_state = True
    await client.close()


@client.command()
@commands.is_owner()
async def restart(ctx):
    """
    Restarts the bot
    """

    global halt_state
    await ctx.reply(content='🟥🟩 **Restarting** 🟩🟥', mention_author=True)
    halt_state = False
    await client.clear()


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
        Named after Minecraft Discord's moderator, this command deletes the message
    :param ctx:
    :return:
    """
    await ctx.message.delete()


if __name__ == "__main__":
    client.run(os.environ["DISCORD_BOT_KEY"])
# vimming
