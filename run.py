#!/usr/bin/python3

import logging
import atexit
import discord
import json
import os
import subprocess
import datetime
from discord.ext import commands

# Set up logging
logging.basicConfig(filename='Yup.log', format='%(asctime)s:%(levelname)s:%(name)s:%(message)s', level=logging.INFO)
logger = logging.getLogger('ItDoneRightBot')
time_now = datetime.datetime.now()
logger.info(f'---- Start ---- {time_now.year}-{time_now.month}-{time_now.day} '
            f'{time_now.hour}:{time_now.minute}:{time_now.second}.{time_now.microsecond} ----\n')

# loading credentials into environment
try:
    for item in json.load(open("settings.json")).items():
        os.environ[item[0]] = str(item[1])
except FileNotFoundError:
    print('Please make a settings.json!')
    exit(1)

client = commands.AutoShardedBot(command_prefix=os.environ["DISCORD_BOT_PREFIX"], intents=discord.Intents.all())

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
    a = [_cog for _cog in os.listdir("./cogs") if _cog.endswith('.py')]
    embed = discord.Embed(title='Reloading all cogs... <a:ch_loading:810641500676816916>', color=0xFEFFFF)
    for _cog in a:
        embed.add_field(name=_cog[:-3], value='🕙', inline=False)
    msg = await ctx.reply(embed=embed)
    success = True
    for _cog in a:
        try:
            client.reload_extension(f'cogs.{_cog[:-3]}')
            embed.set_field_at(index=a.index(_cog), name=_cog[:-3], value='✅', inline=False)
            await msg.edit(embed=embed)
        except Exception as oh_fuck:
            success = False
            embed.set_field_at(index=a.index(_cog), name=_cog[:-3], value=f'🔴 Error: {oh_fuck}', inline=False)
            await msg.edit(embed=embed)
    if success:
        new_embed = discord.Embed(title='Successfully reloaded all cogs', color=0x85c781)
        for field in embed.fields:
            new_embed.add_field(name=field.name, value=field.value, inline=field.inline)
        await msg.edit(embed=new_embed)
        await ctx.reply('Successfully reloaded all cogs.')
    else:
        new_embed = discord.Embed(title='Error occured while reloading cogs', color=0xd14d4d)
        for field in embed.fields:
            new_embed.add_field(name=field.name, value=field.value, inline=field.inline)
        await msg.edit(embed = new_embed)
        await ctx.reply('An error occured while reloading cogs.')


@reload_all.error
@reload.error
@load.error
@unload.error
async def cog_load_error(ctx, error):
    await ctx.reply(f'An error occurred which trying to load/unload/reload cog(s)! Error:```py\n{error}```')


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


@client.command(name='halt', aliases=['shutdown'])
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
        await ctx.reply(content='You do not have sufficient permissions to execute this command. This incident has '
                                'been logged')
        logger.warning(f'{ctx.author.name}#{ctx.author.discriminator} ID={ctx.author.id} '
                        f'attempted to use a owner-only command.')


@client.command()
async def anna(ctx):
    """
    anna
        Named after Minecraft Discord's moderator, this command deletes the message
    :param ctx:
    :return:
    """
    await ctx.message.delete()


async def exit_handler():
    global client
    await client.close()
    _time_now = datetime.datetime.now()
    logger.info(f'---- Stop ---- {_time_now.year}-{_time_now.month}-{_time_now.day} '
                f'{_time_now.hour}:{_time_now.minute}:{_time_now.second}.{_time_now.microsecond} ----\n')

def eh_wrapper():
    asyncio.run(exit_handler)


atexit.register(eh_wrapper)
if __name__ == "__main__":
    client.run(os.environ["DISCORD_BOT_KEY"])

# vimming
