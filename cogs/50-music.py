# https://youtu.be/vQw8cFfZPx0?t=697
# example code
from discord.ext import commands
import discord
import youtube_dl
import os
import datetime
import asyncio
from youtube_search import YoutubeSearch


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        options = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'ignoreerrors': False,
                'quiet': True,
                'no_warnings': True,
                'default_search': 'ytsearch'
                }
        self.ytdl = youtube_dl.YoutubeDL(options)
        self.queue = {}

    @commands.command()
    async def join(self, ctx):
        """
        Connects the bot to the VC
        :param ctx:
        :return:
        """
        if ctx.author.voice is not None:
            if ctx.voice_client is not None and ctx.voice_client.channel != ctx.author.voice.channel:
                await ctx.voice_client.move_to(ctx.author.voice.channel)
                await ctx.reply('Connnected!')
            else:
                vc = ctx.author.voice.channel
                await vc.connect()
                await ctx.reply('Connected!')
        else:
            await ctx.reply('You are not connected to a voice channel.')

    @commands.command()
    async def leave(self, ctx):
        """
        Disconnects bot
        :return:
        """
        if ctx.guild.voice_client is not None:
            await ctx.guild.voice_client.disconnect()
            await ctx.reply('Disconnected!')
        else:
            await ctx.reply('I am not connected to a voice channel')

    async def embed_maker(self, ctx, ytdl_info):
        """
        Embed maker for play command.
        """
        embed = discord.Embed(title='Playing', color=0xFEFFFF, )
        try:
            embed.set_thumbnail(url=ytdl_info['thumbnail'])
        except:
            pass
        try:
            embed.add_field(name='Title', value=f'[{ytdl_info["title"]}]({ytdl_info["url"]})', inline=False)
        except:
            pass
        try:
            embed.add_field(name='Channel', value=f'[{ytdl_info["uploader"]}]({ytdl_info["uploader_url"]})', inline=False)
        except:
            pass
        try:
            embed.add_field(name='Duration', value=f'{str(datetime.timedelta(seconds=ytdl_info["duration"]))}', inline=False)
        except:
            pass
        await ctx.reply(embed=embed)

    async def play(self, ctx, name):
        if ctx.guild.voice_client is not None and ctx.author.voice is not None:
            if ctx.author.voice.channel == ctx.guild.voice_client.channel:
                b = ctx.voice_client
                c = self.ytdl.extract_info(url=name, download=False)
                if 'entries' in c:
                    c = c['entries'][0]
                if b.is_playing() or b.is_paused():
                    b.stop()
                b.play(discord.FFmpegOpusAudio(c['url']), after=lambda e: print('Player error: %s' % e) if e else None)
                await self.embed_maker(ctx=ctx, ytdl_info=c)
            else:
                print(ctx.voice_client.channel)
                await ctx.voice_client.move_to(ctx.author.voice.channel)
                # Seems like the `await` doesn't actually wait until it finishes before calling stuff below, oddly.
                # This `sleep` line ensures that the bot will move before b is defined and all the other stuff happens.
                # I mean, its not like Discord bots need to be *that* fast, right?
                await asyncio.sleep(2)
                b = ctx.voice_client # b = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
                print(b.channel)
                c = self.ytdl.extract_info(url=name, download=False)
                if 'entries' in c:
                    c = c['entries'][0]
                if b.is_playing() or b.is_paused():
                    b.stop()
                b.play(discord.FFmpegOpusAudio(c['url']), after=lambda e: print('Player error: %s' % e) if e else None)
                await self.embed_maker(ctx=ctx, ytdl_info=c)
        elif ctx.author.voice is not None:
            b = await ctx.author.voice.channel.connect()
            await self.embed_maker(ctx=ctx, ytdl_info=self.ytdl.extract_info(url=name, download=False) if 'entries' not in self.ytdl.extract_info(url=name, download=False) else self.ytdl.extract_info(url=name, download=False)['entries'][0])
            b.play(discord.FFmpegOpusAudio(self.ytdl.extract_info(url=name, download=False)['url']), after=lambda e: print('Player error: %s' % e) if e else None)
        else:
            await ctx.reply('You are not connected to a voice channel')

    @commands.command(name='play')
    async def _play(self, ctx, name):
        await self.play(ctx=ctx, name=name)

    @_play.error
    async def play_error(self, ctx, error):
        print(f'\033[31m---------------\nctx: {ctx}\nError: {error}\n---------------\033[0m')
        
    @commands.command()
    async def search(self, ctx, *terms):
        """
        """
        term = ' '.join(terms)
        results = self.ytdl.extract_info(url=f'ytsearch10:{term}', download=False)['entries']
        embed = discord.Embed(title='Results', color=0xFEFFFF)
        for i in results:
            embed.add_field(name=f'{results.index(i) + 1}. {i["title"]}', value=f'Channel: {i["uploader"]}\nURL: {i["url"]}\nDuration: {i["duration"]}\nViews: {i["view_count"]}\nBitrate: {i["abr"]}\n[Thumbnail]({i["thumbnails"][0]})', inline=False)
        await ctx.reply(embed=embed)
        channel = ctx.channel

        def check_int(e):
            try:
                int(e.content)
                if e.channel == channel:
                    return True
                else:
                    return False
            except:
               return False
        try:
            num = await self.client.wait_for('message', timeout=60.0, check=check_int)
        except Exception as e:
            print(e)
            await ctx.reply('You did not choose a valid song in time.')
        else:
            await self.play(ctx=ctx, name=f'{results[int(num.content) - 1]["url"]}')

    @search.error
    async def yeet(self, ctx, error):
        print(f'ctx: {ctx}\nError: {error}')


# setup function also is good
def setup(client):
    client.add_cog(Music(client))
