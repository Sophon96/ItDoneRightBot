# https://youtu.be/vQw8cFfZPx0?t=697
# example code
from discord.ext import commands
import discord
import youtube_dl
import os


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        os.system('rm -rf /tmp/Yup_music/* && mkdir /tmp/Yup_music')

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
        await vc.connect()
        # print('done?')

    @commands.command()
    async def leave(self, ctx):
        """
        Disconnects bot
        :return:
        """
        a = ctx.author.voice.channel
        await a.disconnect()

    @commands.command()
    async def download(self, ctx, *urls):
        """
        Downloads a song from URL
        :param ctx:
        :param url:
        :return:
        """
        await ctx.reply(embed=discord.Embed(title='Downloading...', color=0xFEFFFF))
        os.system('mkdir /tmp/Yup_music')
        with youtube_dl.YoutubeDL({'outtmpl': '/tmp/Yup_music/%(title)s.%(ext)s'}) as ydl:
            ydl.download(list(urls))
        await ctx.reply(embed=discord.Embed(title='Downloaded!', color=0xFEFFFF, description='\n'.join(list(urls))))
    
    @commands.command(name='listmusic', aliases=['lm'])
    async def listmusic(self, ctx):
        a = os.listdir('/tmp/Yup_music/')
        embed = discord.Embed(title='Availible Music', color=0xFEFFFF, description='\n'.join(a))
        await ctx.reply(embed=embed)

    @commands.command()
    async def play(self, ctx, name):
        a = ctx.author.voice.channel
        print(a)
        b = await a.connect()
        b.play(discord.FFmpegOpusAudio(source=f'/tmp/Yup_music/{name}'))


# setup function also is good
def setup(client):
    client.add_cog(Music(client))
