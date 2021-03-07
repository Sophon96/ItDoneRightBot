from discord.ext import commands
import discord
import subprocess

def cleanup_code(content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    else:
        return content
    
class Shell(commands.Cog):
    """
    The ability to execute shell or Python commands through my bot. These are only usable by <@560251455714361354>
    """
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def exec(self, ctx, *, args):
        """
        Execute Python code
        :param ctx:
        :param args:
        :return:
        """
        env = { #get all of the discord.py stuff in here so you can use them with {prefix}exec
            'bot': bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
        }

        env.update(globals())
        body = cleanup_code(body) #if you want to run you commands like this:
        #```python
        #print("hello world")
        #```
        stdout = io.StringIO()

        code_in_l = body.split("\n")
        code_in = ""
        for item in code_in_l:
            if item.startswith(" "):
                code_in += f"... {item}\n"
            else:
                code_in += f">>> {item}\n"

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        t1 = time.time() # start timer
        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{code_in}\n{e.__class__.__name__}: {e}\n```')
        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
                t2 = time.time()
                timep = f"#{(round((t2 - t1) * 1000000)) / 1000} ms"
        except Exception:
            value = stdout.getvalue()
            t2 = time.time()
            timep = f"#{(round((t2 - t1) * 1000000)) / 1000} ms"
            c = (f'```py\n{code_in}\n{value}{traceback.format_exc()}\n{timep}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    c = (f'```py\n{code_in}\n{value}\n{timep}\n```')
                else:
                    c = (f"```py\n{code_in}\n{timep}\n```")
            else:
                c = (f'```py\n{code_in}\n{value}{ret}\n{timep}\n```')
        
        # Make a discord embed with the title of "Output of <command>",
        # the color of #FEFFFF (I would use #FFFFFF, but that's reserved),
        # and the description of c (so we don't need to mess around with
        # add_field and such).
        embed = discord.Embed(title=f'Output of {" ".join(args)}', color=0xFEFFFF, description=c)
        # SEND DA MESSAGE
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
        a = subprocess.check_output(list(args)).decode('utf-8')
        print(args, list(args), a)
        embed = discord.Embed(type='rich', title=f'Output of {" ".join(args)}', color=0xFEFFFF, description=a)
        await ctx.reply(embed=embed)


    @commands.command()
    async def dsh(self, ctx, *args):
        """
        Execute stuff inside a docker container
        """
        import tempfile
        import os

        fd, path = tempfile.mkstemp()
        try:
            with os.fdopen(fd, 'w') as tmp:
                tmp.write(' '.join(args))

#                 print(tmp.read())
            b = subprocess.check_output(f'docker run -it --rm archlinux bash -c "$(cat {path})"', shell=True).decode('utf-8')
        finally:
            os.remove(path)
        print(b)
        embed = discord.Embed(type='rich', title=f'Output of {" ".join(args)}', color=0xFEFFFF, description=b)
        await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(Shell(client))
