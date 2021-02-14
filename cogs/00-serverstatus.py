# https://youtu.be/vQw8cFfZPx0?t=697
# example code
from discord.ext import commands
import discord
import distro
import psutil
import sys


class ServerStatus(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def status(self, ctx):
        """
        Gets server status
        ctx: discord.Context
        """
        embed = discord.Embed(title="Server Status", type="rich", color=0xFEFFFF)
        vmem = psutil.virtual_memory()
        embed.add_field(name="RAM Usage", value=f"{round(vmem.used/1073741824, 2)}GiB out of "
                                                f"{round(vmem.total/1073741824, 2)}GiB")
        embed.add_field(name="CPU Usage", value=f"{psutil.cpu_percent()}%")
        embed.add_field(name="Python information", value=sys.version, inline=True)
        embed.add_field(name="Platform information", value=sys.platform, inline=True)
        if distro.name(pretty=True):
            embed.add_field(name="Linux distro", value=distro.name(pretty=True), inline=True)
        await ctx.reply(mention_author=True, embed=embed)

    # @commands.command()
    # async def ping(self, ctx):
    #     """
    #     Tests latency (WIP)
    #     """
    #     embed = discord.Embed(title="Latency", type="rich")

    # @commands.command()
    # async def temps(self, ctx):

    @commands.command()
    async def invite(self, ctx):
        """
        Posts invite link
        """
        embed = discord.Embed(title="Invite Link", type="rich", color=0xFEFFFF, description=discord.utils.oauth_url(client_id="686423436112691275"))
        embed.set_thumbnail(url="https://i.imgur.com/lmxN3JN.png")
        # embed.add_field(name="test", value=discord.utils.oauth_url(client_id="686423436112691275"))
        await ctx.send(embed=embed)


# setup function also is good
def setup(client):
    client.add_cog(ServerStatus(client))
