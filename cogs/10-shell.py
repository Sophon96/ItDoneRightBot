from discord.ext import commands
import discord
import subprocess

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
        # Just importing some stuff
        # We are going to use os to remove the temporary file
        # and tempfile to make the temporary file
        import os
        import tempfile

        # The way that this is going to work
        # Is that we will write the command(s)
        # the owner (probably me or you) has passed
        # into a temporary file
        #
        # Then, we will use subprocess to use
        # Python to execute that file
        # 
        # We are wrapping the file related things
        # in a try finally block as we want the 
        # file deleted even if the code errors

        # Make a temporary file using tempfile
        # and assign the file descriptor to fd
        # and the path of the file to path
        fd, path = tempfile.mkstemp()

        # Start of the try block and interaction
        # with the file
        try:
            # Open the file using a with statement
            # so that the file will be automatically
            # closed
            with os.fdopen(fd, 'w') as tmp:
                # Turn the arguments from a tuple to
                # a string by putting spaces in between
                # all of the values in the tuple
                # and write it to the temporary file
                tmp.write(' '.join(args))
            # Use subprocess to use sh to use Python to
            # execute the the file and then decode the 
            # output (it's in binary by default) with 
            # UTF-8 and assign it to c
            c = subprocess.check_output(f'python {path}', shell=True).decode('utf-8')
        # Removal of the file
        finally:
            os.remove(path)
        
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
