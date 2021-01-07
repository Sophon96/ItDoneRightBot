from discord.ext import commands
import discord

class Shell(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def exec(self, ctx, *args):
        if ctx.author.id == 560251455714361354:
            await ctx.channel.send(' '.join(args))
            exec(' '.join(args))
        else:
            await ctx.channel.send("You are not priviledged enough to do this. This incident will be reported.")
            print(f'{ctx.author.name} attempted to use exec')

    @commands.command(name='sh')
    async def sh(self, ctx, *args):
        import subprocess
        if ctx.author.id == 560251455714361354:
            a = subprocess.check_output(' '.join(args), shell=True).decode('utf-8')
            await ctx.channel.send(a)
            print(a)
        else:
            await ctx.channel.send('no lmao, dont even think about it')
            print(f'{ctx.author.name} attempted to do something sus with bash')

def setup(client):
    client.add_cog(Shell(client))
