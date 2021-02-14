import discord
import asyncio
from discord.ext import commands


class Shell(commands.Cog):
    """
    Cog for executing arbitrary Python code or shell commands, usable only by the owner of the bot.
    """
    def __init__(self, client):
        self.client = client

    @commands.command(name='exec', aliases=['eval'])
    @commands.is_owner()
    async def exec(self, ctx, *args):
        """
        Execute arbitrary Python code
        :param ctx:
        :param args:
        :return:
        """
        a = ' '.join(args)
        b = compile(a, 'Discord', 'eval', optimize=2)
        c = eval(b)
        embed = discord.Embed(title='Results', color=0xFEFFFF)
        embed.add_field(name='Input', value=f'```py\n{a}\n```', inline=False)
        embed.add_field(name='Output', value=f'```\n{c}\n```', inline=False)
        await ctx.reply(embed=embed)

    @commands.command(name='sh')
    @commands.is_owner()
    async def sh(self, ctx, *args):
        """
        Execute arbitrary shell commands
        :param ctx:
        :param args:
        :return:
        """
        c = ' '.join(args)
        a = await asyncio.create_subprocess_shell(c, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
        b = await a.communicate()
        embed = discord.Embed(type='rich', title='Results', color=0xFEFFFF)
        embed.add_field(name='Input', value=f'```sh\n{c}\n```', inline=False)
        embed.add_field(name='Output', value=f'```\n{b[0].decode()}\n```', inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def dsh(self, ctx, *args):
        """
        Execute arbitrary shell commands inside a docker container
        """
        a = await asyncio.create_subprocess_shell('docker run -t --rm --cpus=0.1 -m 50M archlinux ' + ' '.join(args),
                                                  stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
        a = await a.communicate()
        a = a[0].decode()
        b = ' '.join(args)
        embed = discord.Embed(type='rich', title='Results', color=0xFEFFFF)
        embed.add_field(name='Input', value=f'```sh\n{b}\n```', inline=False)
        embed.add_field(name='Output', value=f'```\n{a}\n```', inline=False)
        await ctx.reply(embed=embed)


def setup(client):
    """
    Setup function. Do not touch.
    :param client:
    :return:
    """
    client.add_cog(Shell(client))
