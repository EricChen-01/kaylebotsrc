import aiohttp
import asyncio
import os
import urllib.parse
import discord
from discord.ext import commands


header = {"x-api-key": os.getenv("PRSAWAPIKEY")}

class KAYLEAI(commands.Cog):
  def __init__(self, client):
        self.client = client
  #AI
  @commands.Cog.listener()
  async def on_message(self, message):
    if self.client.user == message.author:
      return
    # and ( ('kayle-chat' or 'off-topic') in message.channel.name) 
    if(message.content.startswith('kayle ') ):
        sendString = message.content[6:]
        encoded = urllib.parse.quote(sendString)
        params = {'language':'en', 'type' : 'stable', 'message':encoded, 'dev_name' :'Yatami', 'bot_name' : 'KAYLE', 'unique_id':message.author.id}  

        async with aiohttp.ClientSession(headers=header) as session:
          async with session.get(url='https://api.pgamerx.com/v3/ai/response', params=params) as resp:
              text = await resp.json()
              async with message.channel.typing():
                await asyncio.sleep(1)
              await message.reply(text[0]['message'])
              await self.client.process_commands(message)


def setup(client):
  client.add_cog(KAYLEAI(client))


