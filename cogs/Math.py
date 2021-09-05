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
        await ctx.send("your number is {number}")
        while(number != 0):
          digit = number%10
          number = number/10
          await ctx.send("Digit is:{digit} and current number is {number}")



  
def setup(client):
  client.add_cog(Math(client))
