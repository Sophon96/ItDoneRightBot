# https://youtu.be/vQw8cFfZPx0?t=697
# example code
from discord.ext import commands
import discord

import psutil
import sys
class AddUser(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def adduser(self, ctx, pubkey):
        # key 
        file = open()


# setup function also is good
def setup(client):
    client.add_cog(ServerStatus(client))