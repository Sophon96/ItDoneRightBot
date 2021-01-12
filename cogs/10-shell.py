from discord.ext import commands
import discord

class Shell(commands.Cog):
    """
    The ability to execute shell or Python commands through my bot. These are only usable by <@560251455714361354>
    """
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def exec(self, ctx, *args):
        """
        Execute Python code
        :param ctx:
        :param args:
        :return:
        """
        print('yes')
        import subprocess
        b = ' '.join(args)
        print(b)
        b.replace('"', '\"')
        b.replace("'", "\'")
        print(b)
        a = subprocess.check_output(f"python -c {b}", shell=True).decode('utf-8')
        print(a)
        embed = discord.Embed(title=f'Output of {b}', color=0xfeffff, description=a)
        await ctx.reply(embed=embed)


    @commands.command(name='sh')
    @commands.is_owner()
    async def sh(self, ctx, *args):
        """
        Execute shell commands
        :param ctx:
        :param args:
        :return:
        """
        # print('yes')
        import subprocess
        a = subprocess.check_output(' '.join(args), shell=True).decode('utf-8')
        # print(a)
        embed = discord.Embed(type='rich', title=f'Output of {" ".join(args)}', color=0xFEFFFF, description=a)
        await ctx.reply(embed=embed)
        # print(a)


def setup(client):
    client.add_cog(Shell(client))
