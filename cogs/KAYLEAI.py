import aiohttp
import asyncio
import os
import urllib.parse
import discord
from discord.ext import commands
import requests


header = {"x-api-key": os.getenv("PRSAWAPIKEY")}

class KAYLEAI(commands.Cog):
  def __init__(self, client):
        self.client = client
  #AI
  @commands.Cog.listener()
  async def on_message(self, message):
    url = "https://random-stuff-api.p.rapidapi.com/ai"
    content =  message.content[6:]
    if self.client.user == message.author:
      return
    if(message.content.startswith('kayle ') ):
        encoded = urllib.parse.quote(content)
        querystring = {"msg":encoded,"bot_name":"TEST","bot_gender":"male","bot_master":"TEST","bot_age":"19","id": message.author.id,"bot_location": "United States"}

        headers = {
        'authorization': 'URIDaYVJoZRJ',#os.getenv('APIKEY'),
        'x-rapidapi-host': "random-stuff-api.p.rapidapi.com",
        'x-rapidapi-key': '6df8e54493mshb53e746b3c30065p1de934jsn891d42f50ba7',#os.getenv('rapidapi-key')
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        events = response.json()
        async with message.channel.typing():
          await asyncio.sleep(1)
          await message.reply(events["AIResponse"])
          await self.client.process_commands(message)


def setup(client):
  client.add_cog(KAYLEAI(client))


