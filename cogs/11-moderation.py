from discord.ext import commands
import discord


class Moderation(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	@commands.is_owner()
	async def clear(self, ctx, number_of_messages):
		"""
		Delete message
		:param number_of_messages:
		:param ctx:
		:return:
		"""

		# await ctx.message.delete()
		embed = discord.Embed(title=f'Clear', color=0xfeffff, description=f'Clearing **{number_of_messages}** '
																								f'messages in <#{ctx.channel.id}>')
		await ctx.reply(embed=embed)
		# The +1 is to account for the message the bot sends
		# EDIT: The +2 is to account for the message sent and the message the bot sends
		await ctx.channel.purge(limit=(int(number_of_messages) + 2))
		embed = discord.Embed(title='Clear', color=0xfeffff, description='**DONE**\n*Self-destructing in 15 seconds*')
		await ctx.reply(embed=embed, delete_after=15.0)


def setup(client):
	client.add_cog(Moderation(client))
