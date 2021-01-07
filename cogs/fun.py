# Yeet
from discord.ext import commands
import discord

import os

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def restart(self, ctx):
        """
        Restarts the bot
        """
        await ctx.send('\*\*\*  **Restarting**')
        os.fsync()
        os.execl(__file__)
        exit(0)

# So I need this thing apparently.
# tbh idk what it does
def setup(client):
    client.add_cog(Misc(client))
