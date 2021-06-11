import aiohttp
import asyncio
import os
import discord
from discord.ext import commands
import datetime
import pymongo
from pymongo import MongoClient

serverCluster = MongoClient(f'mongodb+srv://Kayle:{os.getenv("mongoDBPassword")}@discordkayledb.ddcpx.mongodb.net/server?retryWrites=true&w=majority')
serverdb = serverCluster["server"]
svrCollection = serverdb["server"]

class Experimental(commands.Cog):
  def __init__(self, client):
        self.client = client
  #commands
  #experimental
  @commands.command()
  async def _setup(self,ctx):
    channel = discord.utils.get(ctx.guild.text_channels, id=None)
    if channel == None:
        await ctx.send('False')
    else:
        await ctx.send('True')
def setup(client):
  client.add_cog(Experimental(client))


