# Yeet
from discord.ext import commands
import discord
import requests
import sys
import os

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
    
    @commands.command(name='mcstatus', aliases=['mccheck', 'mcch', 'mcs', 'mccheckhealth'])
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

# So I need this thing apparently.
# tbh idk what it does
def setup(client):
    client.add_cog(Misc(client))
