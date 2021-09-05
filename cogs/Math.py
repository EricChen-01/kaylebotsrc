import discord
from discord.ext import commands


class Math(commands.Cog):
  def __init__(self, client):
        self.client = client
  #commands
  @commands.command()
  async def b2d(self,ctx,number):  
    await ctx.send(f"attempting to convert {number} to binary.")
    if isBinary(self,ctx,number):
      await ctx.send(f"your number is {number}")
      sum = 0
      power = 0
      while(number != 0):
        digit = number%10
        number = number//10
        sum = sum + digit * 2 ** power
        power += 1
      await ctx.send(sum)
    else:
      await ctx.send("Not a binary number.")


  
def setup(client):
  client.add_cog(Math(client))


async def isBinary(self,ctx,number):
  set1 = set()
  await ctx.send(f"inside isBinary")
  while(number > 0):
    digit = number % 10
    set1.add(digit)
    number = int(number / 10)

  set1.discard(0)
  set1.discard(1)
    
  if (len(set1) == 0):
      return True

  return False
