# https://youtu.be/vQw8cFfZPx0?t=697
# example code
from discord.ext import commands
import discord
import youtube_dl
import datetime
import asyncio
import logging


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        ytdl_logger = logging.getLogger('ItDoneRightBot.cogs.50-music.YoutubeDL')
        ytdl_logger.setLevel(level=logging.DEBUG)
        options = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'ignoreerrors': False,
            'quiet': False,
            'no_warnings': False,
            'default_search': 'ytsearch',
            'logger': ytdl_logger
        }
        self.ytdl = youtube_dl.YoutubeDL(options)
        # TODO: Implement queue
        # self.queue = {}

    @commands.command()
    async def join(self, ctx):
        """
        Connects the bot to a voice channel
        :param ctx:
        :return:
        """
        if ctx.author.voice is not None:
            if ctx.voice_client is not None and ctx.voice_client.channel != ctx.author.voice.channel:
                await ctx.voice_client.move_to(ctx.author.voice.channel)
                await ctx.reply('Connected!')
            else:
                vc = ctx.author.voice.channel
                await vc.connect()
                await ctx.reply('Connected!')
        else:
            await ctx.reply('You are not connected to a voice channel.')

    @commands.command()
    async def leave(self, ctx):
        """
        Disconnects bot from a voice channel
        :return:
        """
        if ctx.guild.voice_client is not None:
            await ctx.guild.voice_client.disconnect()
            await ctx.reply('Disconnected!')
        else:
            await ctx.reply('I am not connected to a voice channel')

    @staticmethod
    async def embed_maker(ctx, ytdl_info):
        """
        Embed maker for play command.
        """
        embed = discord.Embed(title='Playing', color=0xFEFFFF, )
        try:
            # Set thumbnail for embed, if possible
            embed.set_thumbnail(url=ytdl_info['thumbnail'])
        except KeyError:
            pass
        try:
            # Set title of the song
            embed.add_field(name='Title', value=f'[{ytdl_info["title"]}]({ytdl_info["webpage_url"]})', inline=False)
        except KeyError:
            pass
        try:
            # YouTube Channel
            embed.add_field(name='Channel', value=f'[{ytdl_info["uploader"]}]({ytdl_info["uploader_url"]})',
                            inline=False)
        except KeyError:
            pass
        try:
            # Duration of the track
            embed.add_field(name='Duration', value=f'{str(datetime.timedelta(seconds=ytdl_info["duration"]))}',
                            inline=False)
        except KeyError:
            pass
        await ctx.reply(embed=embed)

    async def play(self, ctx, name):
        """
        Plays a track from url. If its not a valid url, the bot will search YouTube.
        :param ctx:
        :param name:
        :return:
        """

        # Check if the bot and user are joined to a voice channel
        if ctx.guild.voice_client is not None and ctx.author.voice is not None:

            # Check if they are joined to the same voice channel
            if ctx.author.voice.channel == ctx.guild.voice_client.channel:
                b = ctx.voice_client

                # Get the song info
                c = self.ytdl.extract_info(url=name, download=False)

                # There will be a list when ytdl search YouTube for videos,
                # regardless of how many results you set.
                # There will only be one in this case.
                if 'entries' in c:
                    c = c['entries'][0]

                # If the bot is currently playing something, stop.
                if b.is_playing() or b.is_paused():
                    b.stop()

                # Play new stuff
                b.play(discord.FFmpegOpusAudio(c['url']), after=lambda e: print('Player error: %s' % e) if e else None)

                # Make and send a embed with the song info.
                await self.embed_maker(ctx=ctx, ytdl_info=c)

            # If the user and the bot are not in the same voice channel
            else:

                # Move to the user's voice channel
                await ctx.voice_client.move_to(ctx.author.voice.channel)

                # NOTE:
                # Seems like the `await` doesn't actually wait until it finishes before calling stuff below, oddly.
                # This `sleep` line ensures that the bot will move before b is defined and all the other stuff happens.
                # I mean, its not like Discord bots need to be *that* fast, right?
                await asyncio.sleep(2)

                # Get the new voiceclient.
                b = ctx.voice_client

                # Get the song info
                c = self.ytdl.extract_info(url=name, download=False)

                # See line 102
                if 'entries' in c:
                    c = c['entries'][0]

                if b.is_playing() or b.is_paused():
                    b.stop()

                b.play(discord.FFmpegOpusAudio(c['url']), after=lambda e: print('Player error: %s' % e) if e else None)
                await self.embed_maker(ctx=ctx, ytdl_info=c)

        # If the user is in a voice channel, but the bot is not
        elif ctx.author.voice is not None:

            x = self.ytdl.extract_info(url=name, download=False)
            x = x if 'entries' not in x else x['entries'][0]
            b = await ctx.author.voice.channel.connect()
            await self.embed_maker(ctx=ctx, ytdl_info=x)
            b.play(discord.FFmpegOpusAudio(x['url']),
                   after=lambda e: print('Player error: %s' % e) if e else None)

        # If the user is not a voice channel
        else:
            await ctx.reply('You are not connected to a voice channel')

    @commands.command(name='play')
    async def _play(self, ctx, *name):
        # Just calls the real play function
        await self.play(ctx=ctx, name=' '.join(name))

    @_play.error
    async def play_error(self, ctx, error):
        # Escape codes don't work yet
        print(f'\033[31m---------------\nctx: {ctx}\nError: {error}\n---------------\033[0m')

    @commands.command()
    async def search(self, ctx, *terms):
        """
        Searches YouTube for music/videos, then play it.
        :param ctx:
        :param terms:
        :return:
        """
        # Join all the search terms into one string
        term = ' '.join(terms)

        # Use YoutubeDL to get 10 results matching the search terms
        results = self.ytdl.extract_info(url=f'ytsearch10:{term}', download=False)['entries']

        # Initialize embed
        embed = discord.Embed(title='Results', color=0xFEFFFF)

        for i in results:
            # Add helpful info for each song.
            embed.add_field(name=f'{results.index(i) + 1}. {i["title"]}',
                            value=f'Channel: {i["uploader"]}\n'
                                  f'Duration: {datetime.timedelta(seconds=i["duration"])}\n',
                            inline=False)
        await ctx.reply(embed=embed)
        channel = ctx.channel

        # The check for the following wait_for
        def check_int(f):
            try:
                # Checks to see if the user sent a valid integer less that 10
                # and that the message was sent in the same channel
                if int(f.content) <= 10 and f.channel == channel:
                    return True
                else:
                    # Not the same channel
                    return False
            except ValueError:
                # Not a valid integer
                return False

        try:
            # Wait for the user to pick a song
            num = await self.client.wait_for('message', timeout=60.0, check=check_int)
        except asyncio.TimeoutError:
            # User didn't respond in time
            await ctx.reply('You did not choose a valid song in time.')
        except Exception as e:
            # Something else went wrong
            await ctx.reply(f'A error occurred!\nError:\n```py\n{e}```')
        else:
            # If nothing went wrong, just play the chosen song.
            await self.play(ctx=ctx, name=f'{results[int(num.content) - 1]["webpage_url"]}')

    @search.error
    async def yeet(self, ctx, error):
        print(f'ctx: {ctx}\nError: {error}')

    @commands.command()
    async def stop(self, ctx):
        """
        Stops playing music.
        :param ctx:
        :return:
        """
        ctx.voice_client.stop()

    @commands.command()
    async def pause(self, ctx):
        """
        Pauses music.
        :param ctx:
        :return:
        """
        ctx.voice_client.pause()


# setup function also is good
def setup(client):
    client.add_cog(Music(client))
