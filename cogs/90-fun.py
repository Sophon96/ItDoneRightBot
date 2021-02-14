# Yeet
from discord.ext import commands
import discord
import requests


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def neko(self, ctx):
        """
        Nekomimi
        """
        nekos = 'https://nekos.life/api/v2/img/neko'
        nekosjson = requests.get(nekos).json()
        nekoimage = nekosjson['url']
        await ctx.send(nekoimage)

    @commands.command(name='8ball')
    async def _8ball(self, ctx):
        """
        Confused? Ask the 8ball!
        """
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
        lewd = 'https://nekos.life/api/v2/img/lewd'
        lewdjson = requests.get(lewd).json()
        lewdimage = lewdjson['url']
        await ctx.send(lewdimage)

    @staticmethod
    def checkIfMDSP(ctx):
        return ctx.guild.id == 764981968579461130

    @commands.command(name='mcstatus', aliases=['mccheck', 'mcch', 'mcs', 'mccheckhealth'])
    @commands.check(checkIfMDSP)
    async def _mc_check_health(self, ctx):
        """
        Check the health of MC servers. Made for MDSP.
        """
        checklist = requests.get('https://status.mojang.com/check').json()
        sites = {}
        siteres = {}
        for i in checklist:
            try:
                a = requests.get('http://' + list(i.keys())[0])
                if a.ok:
                    sites.update({list(i.keys())[0]: True})
                    siteres.update({list(i.keys())[0]: 0})
                else:
                    sites.update({list(i.keys())[0]: f'{a.status_code} {a.reason}'})
                    siteres.update({list(i.keys())[0]: 1})
            except Exception as e:
                sites.update({list(i.keys())[0]: e})
                siteres.update({list(i.keys())[0]: 2})
        # print(sites)
        embed = discord.Embed(title='MC Service Health', color=0xFEFFFF, description='**NOTE**: `401 Unauthorized` for session.minecraft.net and `404 Not Found` for sessionserver.mojang.com are normal')
        for i2 in list(sites.keys()):
            if siteres[i2] == 2:
                embed.add_field(name=i2, value=f'🟥{sites[i2]}', inline=True)
            elif siteres[i2] == 1:
                embed.add_field(name=i2, value=f'🟨 {sites[i2]}', inline=True)
            elif siteres[i2] == 0:
                embed.add_field(name=i2, value=f'🟩', inline=True)
            else:
                exit('Issue with mc_check_health, 90-fun.py')
        embed.add_field(name='\u200B', value='\u200B')
        await ctx.reply(embed=embed)

    # TODO: Potentially fix later
    # def checkInt(e):
    #     try:
    #         int(e)
    #         return True
    #     except ValueError:
    #         return False
    
    @commands.command(name='xkcd')
    async def _xkcd(self, ctx, *numbers):
        """
        Get a xkcd comic
        """
        # print(numbers)
        for i in numbers:
            # print(i)
            # TODO: Potentially fix later
            # if not checkInt(i):
            #     print(0)
            #     await ctx.reply(embed=discord.Embed(title=f'{i} is not a valid integer!', description="yeet"))
            #     continue
            # print('Before requests')
            a = requests.get(f'https://xkcd.com/{i}/info.0.json')
            # print(a)
            if a.ok:
                # print(1)
                a = a.json()
                yeet = discord.Embed(color=0xFEFFFF, title=a["title"])
                yeet.add_field(name='Year', value=a["year"])
                yeet.add_field(name='Month', value=a["month"])
                yeet.add_field(name='Day', value=a["day"])
                yeet.set_footer(text=a["alt"])
                yeet.set_image(url=a["img"])
                await ctx.reply(embed=yeet)
            else:
                # print(2)
                bad = discord.Embed(color=0xFEFFFF, title=f'Bad response getting xkcd {i}')
                bad.add_field(name='Status code', value=str(a.status_code))
                bad.add_field(name='Reason', value=a.reason)
                await ctx.reply(embed=bad)

    @commands.command(name='checksite', aliases=['cs'])
    async def _checksite(self, ctx, *urls):
        """
        Check the health of a site.
        """
        embed = discord.Embed(title='Site Health', color=0xFEFFFF)
        for i in urls:
            try:
                if i[0:7] == 'http://' or i[0:8] == 'https://':
                    a = requests.get(i)
                else:
                    await ctx.reply(embed=discord.Embed(title='No Schema Supplied!', color=0xFEFFFF, description='Assuming http://'))
                    a = requests.get('http://' + i)
                if a.ok:
                    embed.add_field(name=i, value='🟩', inline=True)
                else:
                    embed.add_field(name=i, value=f'🟨 {a.status_code} {a.reason}', inline=True)
            except Exception as e:
                embed.add_field(name=i, value=f'🟥 {e}', inline=True)
        await ctx.reply(embed=embed)

    @commands.command(name='checkserver', aliases=['ms', 'sc', 'chksvr'])
    async def _check_mc_server(self, ctx, *servers):
        """
        Check the stats of a Minecraft server
        """
        
        for i in servers:
            embed = discord.Embed(title=f'{i} stats', color=0XFEFFFF)
            try:
                a = requests.get(f'https://api.mcsrvstat.us/2/{i}').json()
                if a['online']:
                    embed.add_field(name='Online', value='Yes', inline=True)
                    if a['players']['online'] > 0:
                        embed.add_field(name='Players', value=f'{a["players"]["online"]}/{a["players"]["max"]}', inline=True)
                        try:
                            embed.add_field(name='Player Names', value=', '.join(a["players"]["list"]), inline=True)
                        except KeyError:
                            embed.add_field(name='Player Names', value='Unknown', inline=True)
                    else:
                        embed.add_field(name='Players', value=f'0/{a["players"]["max"]}', inline=True)
                    if len(a['motd']['clean']) == 2:
                        embed.add_field(name='Name', value=f'{a["motd"]["clean"][0]}', inline=True)
                        embed.add_field(name='MOTD', value=f'MOTD: {a["motd"]["clean"][1]}', inline=True)
                    else:
                        embed.add_field(name='Name', value=f'{a["motd"]["clean"][0]}', inline=True)
                else:
                    embed.add_field(name='Online', value='No')
            except Exception as e:
                embed.add_field(name=i, value=f'Something went wrong!\nException: {e}', inline=True)
            await ctx.reply(embed=embed)

    @commands.command()
    async def avatar(self, ctx, *user):
        if not user:
            await ctx.send(ctx.author.avatar_url)
        else:
            user = int(user[0].strip('<>@!'))
            print(user)
            user = self.client.get_user(user)
            await ctx.send(user.avatar_url)

    @avatar.error
    async def _0001(self, ctx, error):
        print(error)


# So I need this thing apparently.
# tbh idk what it does
def setup(client):
    client.add_cog(Misc(client))
