import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import os
#run python -m pip install pymongo[srv] if error
cluster = MongoClient(f'mongodb+srv://Kayle:{os.getenv("mongoDBPassword")}@discordkayledb.ddcpx.mongodb.net/server?retryWrites=true&w=majority')
db = cluster["server"]
collection = db["server"]

class CrossServerCommunication(commands.Cog):
  def __init__(self, client):
        self.client = client
  #events
  

  #commands
  @commands.command()
  async def talk(self, ctx, *, message):
    await ctx.send(message)
  
  

  

 
  
def setup(client):
  client.add_cog(CrossServerCommunication(client))
