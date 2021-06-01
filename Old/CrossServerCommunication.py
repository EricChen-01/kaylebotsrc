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
    newMessage = {"name": ctx.message.author.display_name, "message": message, "guild": ctx.message.author.guild.name}
    collection.insert_one(newMessage)
    await ctx.send(f'"{message}" has been sent to the database')

  @commands.command()
  async def receive(self, ctx):
    results =   collection.aggregate([{ "$sample": { "size": 1 } }])
    for result in results:
      await ctx.send(f'{result["name"]} from the {result["guild"]} discord server said "{result["message"]}".')
      collection.delete_one({"_id":result["_id"]})
  
    
def setup(client):
  client.add_cog(CrossServerCommunication(client))
