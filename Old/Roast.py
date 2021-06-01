import discord
import requests
import random
from discord.ext import commands

class Roast(commands.Cog):
  def __init__(self, bot: commands.Bot):
        self.bot = bot
  #commands
  @commands.command()
  async def roast(self, ctx, user:discord.Member):
    global listOfMessages
    response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json")
    if user.id == 235103490869821440:
      await ctx.send(f'{random.choice(listOfMessages)}')
    else:
      await ctx.send(f'{user.display_name}, {response.json()["insult"]}')

def setup(client):
  client.add_cog(Roast(client))