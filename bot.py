from config import *
from wakeonlan import send_magic_packet
import subprocess

# Async Imports
from __future__ import unicode_literals
import concurrent.futures
import asyncio

# Discord API
import discord
from discord.ext import commands

class Controller(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

		# Server machine power state
		self.power = False

		######### TODO: Status check loop

	@commands.command(pass_context=True, no_pm=True)
	async def start(self, ctx):
		if self.power:
			await ctx.message.channel.send('Server system has already started...')
		else:
			send_magic_packet(MACADDRESS)
			await ctx.message.channel.send('Server system is now powering on...')

	@commands.command(pass_context=True, no_pm=True)
	async def stop(self, ctx):
		if not self.power:
			await ctx.message.channel.send('Server system has already stopped...')
		else:
			subprocess.run(['net', 'rpc', 'shutdown', '-I', IPADDRESS, '-U', '{}%{}'.format(USERNAME, PASSWORD)])
			await ctx.message.channel.send('Server system is now powering off...')

client=commands.Bot(command_prefix=commands.when_mentioned_or('server '))
client.add_cog(Controller(client))

@client.event
async def on_ready():
    print('User: '+str(client.user.name))
    print('ID: '+str(client.user.id))
    print('Ready!')

client.run(TOKEN)