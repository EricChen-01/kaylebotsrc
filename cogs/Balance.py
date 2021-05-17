import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import os
#run python -m pip install pymongo[srv] if error
cluster = MongoClient(f'mongodb+srv://Kayle:{os.getenv("mongoDBPassword")}@discordkayledb.ddcpx.mongodb.net/KayleBotDataBase?retryWrites=true&w=majority')
db = cluster["KayleBotDataBase"]
collection = db["Users"]

class Balance(commands.Cog):
  def __init__(self, client):
        self.client = client
  #commands
  
  
def setup(client):
  client.add_cog(Balance(client))
