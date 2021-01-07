# Yeet
from discord.ext import commands
import discord

import sys
import os

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Infinite uptime acheived. *shuts down computer*
    @commands.command()
    async def restart(self, ctx):
        """
        Restarts the bot
        """
        
        # await ctx.send('it works')
        await ctx.send('\*\*\*  **Restarting**')
        # TODO: Flush files
        # os.fsync()
        os.execv('run.py', sys.argv)
        exit(0)

    @commands.command()
    async def neko(self, ctx):
        """
        Nekomimi
        """
        import requests
        nekos = 'https://nekos.life/api/v2/img/neko'
        nekosjson = requests.get(nekos).json()
        nekoimage = nekosjson['url']
        await ctx.send(nekoimage)

    @commands.command(name='8ball')
    async def _8ball(self, ctx):
        """
        Confused? Ask the 8ball!
        """
        import requests
        eball = 'https://nekos.life/api/v2/img/8ball'
        eballjson = requests.get(eball).json()
        eballimage = eballjson['url']
        await ctx.send(eballimage)

    @commands.command()
    @commands.is_nsfw()
    async def neko_lewd(self, ctx):
        """
        Lewd
        """
        import requests
        lewd = 'https://nekos.life/api/v2/img/lewd'
        lewdjson = requests.get(lewd).json()
        lewdimage = lewdjson['url']
        await ctx.send(lewdimage)

# So I need this thing apparently.
# tbh idk what it does
def setup(client):
    client.add_cog(Misc(client))
