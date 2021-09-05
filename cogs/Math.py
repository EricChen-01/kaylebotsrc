import discord
from discord.ext import commands


class Math(commands.Cog):
  def __init__(self, client):
        self.client = client
  #commands
  @commands.command()
  async def b2d(self,ctx,number: int):  
    if await isBinary(self,ctx,number):
      sum = 0
      power = 0
      while(number > 0):
        digit = number%10
        number = number//10
        sum = sum + digit * 2 ** power
        power += 1
      await ctx.send(sum)
    else:
      await ctx.send("Not a binary number.")

  @commands.command()
  async def d2b(self,ctx,number:int):
    binary = ""
    if number >= 0:
      while(number > 0):
        remainder = number % 2
        if remainder != 0:
          binary += "1"
        else:
          binary += "0"
        number = number // 2
      await ctx.send(binary [::-1])
    else:
      await ctx.send("Number not supported.")
        
  
def setup(client):
  client.add_cog(Math(client))


async def isBinary(self,ctx,number:int):
  set1 = set()
  while(number > 0):
    digit = number % 10
    set1.add(digit)
    number = int(number / 10)

  set1.discard(0)
  set1.discard(1)
    
  if (len(set1) == 0):
      return True

  return False
