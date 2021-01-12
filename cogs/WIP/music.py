# https://youtu.be/vQw8cFfZPx0?t=697
# example code
from discord.ext import commands
import discord

import os


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        """
        Connects the bot to the VC
        :param ctx:
        :return:
        """
        vs = ctx.author.voice
        # print(vs)
        vc = vs.channel
        # print(vc)
        # print(type(vc))
        # print('yeet')
        # a = discord.VoiceClient(channel=vc)
        # await a.connect(reconnect=False, timeout=0.01)
        # await vc.connect()
        # I am so fcking tired right now lmao
        global a
        a = await vc.connect()
        # print('done?')

    @commands.command()
    async def leave(self, ctx):
        """
        Disconnects bot
        :return:
        """
        global a
        await a.disconnect()

    @commands.command()
    async def download(self, ctx, url):
        """
        Downloads a song from URL
        :param ctx:
        :param url:
        :return:
        """



# setup function also is good
def setup(client):
    client.add_cog(Music(client))
