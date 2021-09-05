import discord
from discord.ext import commands


class Math(commands.Cog):
  def __init__(self, client):
        self.client = client
  #commands
  @commands.command()
  async def binaryToDecimal(self,ctx, number = None):
      if number == None:
        await ctx.send("Enter a binary number")
      else:
        for digit in number:
          digit = number%10
          await ctx.send(digit)


  
def setup(client):
  client.add_cog(Math(client))
