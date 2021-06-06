import aiohttp
import asyncio
import os
import urllib.parse
import discord
from discord.ext import commands


header = {"x-api-key": os.getenv("PRSAWAPIKEY")}

class Experimental(commands.Cog):
  def __init__(self, client):
        self.client = client
  #commands
  #experimental
  @commands.command()
  async def outside(self,ctx):
    await hi(ctx=ctx,message=ctx.message.content)
def setup(client):
  client.add_cog(Experimental(client))

async def hi(ctx,message):
    await ctx.send(f'{message} + LOL')


