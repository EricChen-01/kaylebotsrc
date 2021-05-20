import discord
from discord.ext import commands
import os


class GoogleSearch(commands.Cog):
  def __init__(self, client):
        self.client = client
  #commands
  @commands.command()
  async def googleImage(self, ctx, *message):
  
def setup(client):
  client.add_cog(GoogleSearch(client))
