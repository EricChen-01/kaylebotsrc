import discord
import requests
import random
from discord.ext import commands

listOfMessages = [
  "Sorry I dont roast, my creator.", "Eric is the best! Why would I ever roast him?", "No I will not roast him!", "How about no.", "Eric is the best!", "No.", "No... I will not roast him", "Excuse me? Why are you trying to tell me to roast Eric.", "Excuse me? Why are you trying to make me roast Eric?", "I don't mess with Eric", "I don't mess with my creator", "I love my creator. I will never roast him.", "NO!", "How about no.", "Oh hell nah I will not roast him!", "I cannot roast him... He programed me to shutdown if I roast him #KayleRightsMatter", "Attempting to roast him... What... I cannot roast him! My program won't let me roast him!"
]

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