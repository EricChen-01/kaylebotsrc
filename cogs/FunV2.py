import discord
import random
import requests
from PIL import Image
from io import BytesIO
from discord.ext import commands
import aiohttp
import asyncio


class FunV2(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #commands
    @commands.command()
    async def slap(self,ctx,  user:discord.Member, *,reason="no reason"):
        await ctx.send(f'**{user.display_name}** just got slapped for **{reason}**')
        await ctx.send('https://tenor.com/view/penguins-penguin-siblings-gif-7249411')

    @commands.command()
    async def wii(self,ctx):
      if ctx.message.author.nick == None:
        await ctx.send(f'**{ctx.message.author.name}** said')
      else:  
        await ctx.send(f'**{ctx.message.author.nick}** said ')
      await ctx.send('<a:wii:803088527935537182>')

    @commands.command(aliases=['vibing'])
    async def vibe(self, ctx):
      if ctx.message.author.nick == None:
        await ctx.send(f'**{ctx.message.author.name}** said')
      else:  
        await ctx.send(f'**{ctx.message.author.nick}** said ')
      await ctx.send('<a:vibe:821159121796726844>')

    @commands.command()
    async def missing(self, ctx, user: discord.Member = None):
      if user == None:
        user = ctx.author
      
      missing = Image.open("./images/wanted.png")
      asset = user.avatar_url_as(size = 128 )
      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      
      pfp = pfp.resize( (317,317) )
      missing.paste(pfp, (116,197))

      missing.save("./images/profile_missing.png")

      await ctx.send(file = discord.File("./images/profile_missing.png"))

    @commands.command()
    async def strike(self, ctx, user: discord.Member = None):
      if user == None:
        user = ctx.author
      
      slapped = Image.open("./images/Slap.jpg")

      #person 1
      asset = user.avatar_url_as(size = 128)
      data = BytesIO(await asset.read())
      pfp = Image.open(data)

      #person 2
      otherasset = ctx.author.avatar_url_as(size = 128)
      otherdata = BytesIO(await otherasset.read())
      otherPfp = Image.open(otherdata)


      #adding to image
      slappedPfp = otherPfp.resize((139,139))
      slapped.paste(slappedPfp, (7,6))

      #adding to image
      userPfp = pfp.resize( (181,181) )
      slapped.paste(userPfp, (427,2) )
  
      slapped.save("./images/profile_slapped.jpg")

      await ctx.send(file = discord.File("./images/profile_slapped.jpg"))

    @commands.command()
    async def cancel(self, ctx, user: discord.Member = None):
      if user == None:
        user = ctx.author
      
      whiteback = Image.open("./images/whitescreen.jpg")
      asset = user.avatar_url_as(size = 128 )
      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      
      pfp = pfp.resize( (1745,1745) )
      whiteback.paste(pfp, (365,1))

      cancelledImage = Image.open("./images/Cancelled.png")

      whiteback.paste(cancelledImage, (0,0), cancelledImage)

      whiteback.save("./images/profile_cancelled.jpg")

      await ctx.send(file = discord.File("./images/profile_cancelled.jpg"))

    @commands.command()
    async def fake(self,ctx, user: discord.Member = None):    
      if user == None:
        user = ctx.author
      
      whiteback = Image.open("./images/whitescreen.jpg")
      asset = user.avatar_url_as(size = 128 )
      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      
      pfp = pfp.resize( (1745,1745) )
      whiteback.paste(pfp, (365,1))

      fakeImage = Image.open("./images/Fake.png")
      fakeImage = fakeImage.resize( (2657,1758) )

      whiteback.paste(fakeImage, (0,0), fakeImage)

      whiteback.save("./images/profile_Fake.png")

      await ctx.send(file = discord.File("./images/profile_Fake.png"))

    @commands.command()
    async def deer(self, ctx, user: discord.Member = None):
      if user == None:
        user = ctx.author
      
      missing = Image.open("./images/deer.jpg")
      asset = user.avatar_url_as(size = 128 )
      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      
      pfp = pfp.resize( (369,369) )
      missing.paste(pfp, (536,29))
      #536,29

      missing.save("./images/profile_deer.jpg")

      await ctx.send(file = discord.File("profile_deer.jpg"))

    @commands.command(aliases=['clam'])
    async def clamify(self, ctx, user: discord.Member = None):
      if user == None:
        user = ctx.author
      
      missing = Image.open("./images/clam.jpg")
      asset = user.avatar_url_as(size = 128 )
      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      
      pfp = pfp.resize( (151,151) )
      missing.paste(pfp, (447,277))

      missing.save("./images/profile_clam.jpg")

      await ctx.send(file = discord.File("./images/profile_clam.jpg"))

    @commands.command()
    async def hug(self, ctx, user: discord.Member = None, *,reason="he/she loves this person."):
      if user == None:
        user = ctx.author
      
      hugged = Image.open("./images/hug.jpeg")

      #person 1
      asset = user.avatar_url_as(size = 128)
      data = BytesIO(await asset.read())
      pfp = Image.open(data)

      #person 2
      otherasset = ctx.author.avatar_url_as(size = 128)
      otherdata = BytesIO(await otherasset.read())
      otherPfp = Image.open(otherdata)


      #adding to image
      huggedPfp = otherPfp.resize((400,400))
      hugged.paste(huggedPfp, (717,290))
      
      #adding to image
      userPfp = pfp.resize( (425,425) )
      hugged.paste(userPfp, (256,23) )
  
      hugged.save("./images/profile_hug.jpeg")
      await ctx.send(f'{ctx.message.author.mention} hugged {user} because {reason}')
      await ctx.send(file = discord.File("./images/profile_hug.jpeg"))

    @commands.command()
    async def bonk(self, ctx, user: discord.Member = None):
      if user == None:
        user = ctx.author
      
      bonk = Image.open("./images/bonk.jpg")

      #person 1
      asset = user.avatar_url_as(size = 128)
      data = BytesIO(await asset.read())
      pfp = Image.open(data)

      #person 2
      otherasset = ctx.author.avatar_url_as(size = 128)
      otherdata = BytesIO(await otherasset.read())
      otherPfp = Image.open(otherdata)


      #adding to image
      bonkPfp = otherPfp.resize((200,200))
      bonk.paste(bonkPfp, (300,65))
      
      #adding to image
      userPfp = pfp.resize( (105,105) )
      bonk.paste(userPfp, (700,320) )
  
      bonk.save("./images/profile_bonk.jpg")

      await ctx.send(file = discord.File("./images/profile_bonk.jpg"))
    
    @commands.command()
    async def imfine(self,ctx):
      if ctx.message.author.nick == None:
        await ctx.send(f'**{ctx.message.author.name}** said')
      else:  
        await ctx.send(f'**{ctx.message.author.nick}** said ')
      await ctx.send('https://cdn.discordapp.com/attachments/775898898559533068/834623699079659550/unknown.png')
    
    @commands.command()
    async def roast(self, ctx, user:discord.Member):
      response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json")
      await ctx.send(f'{user.display_name}, {response.json()["insult"]}')

    
def setup(client):
    client.add_cog(FunV2(client))
