import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import os
#run python -m pip install pymongo[srv] if error
cluster = MongoClient(f'mongodb+srv://Kayle:{os.getenv("mongoDBPassword")}@discordkayledb.ddcpx.mongodb.net/server?retryWrites=true&w=majority')
db = cluster["server"]
collection = db["server"]

class ServerDetails(commands.Cog):
  def __init__(self, client):
        self.client = client
  #events
  

  #commands
  @commands.command()
  async def addServer(self, ctx, channel_id:int):
    id = ctx.message.guild.id
    guild = self.client.get_guild(id)
    newServer = {"_id":id, "count": guild.member_count, "channel_id": channel_id}
    collection.insert_one(newServer)
  
  @commands.command()
  async def join(self, ctx):
    id = ctx.message.guild.id
    guild = self.client.get_guild(id)
    channel = self.client.get_channel("841370909432217611")
    collection.update_one({"_id": id},{"$set":{"count": guild.member_count}})
    await self.client.edit_channel(channel, name=f"{}")
    
  
  @commands.command()
  async def leave(self, ctx):
    id = ctx.message.guild.id
    guild = self.client.get_guild(id)
    collection.update_one({"_id": id},{"$set":{"count": guild.member_count}})

  

 
  
def setup(client):
  client.add_cog(ServerDetails(client))
