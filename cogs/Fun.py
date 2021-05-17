import discord
import random
import requests
from PIL import Image
from io import BytesIO
from discord.ext import commands


listOfResponses = [
    'It is certain', 'It is decidedly so', 'Without a doubt',
    'Yes – definitely', 'You may rely on it', 'As I see it, yes',
    'Most likely', 'Outlook good', 'Yes Signs point to yes', 'Reply hazy',
    'try again', 'Ask again later', 'Better not tell you now',
    'Cannot predict now', 'Concentrate and ask again', 'Dont count on it',
    'My reply is no', 'My sources say no', 'Outlook not so good',
    'Very doubtful'
]

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    #commands
    @commands.command(brief='<@someone> <@someone> <reason>')
    async def marry(self, ctx, user1: discord.Member, user2: discord.Member , *, reason='because they lob eachother'):
        global listOfResponses
        await ctx.send(f'{user1.display_name} and {user2.display_name} just got married for the reason "{reason}"')
        await ctx.send(
            f'Will the marrage last? {random.choice(listOfResponses)}')

    @commands.command(brief='<@someone> <reason>')
    async def slap(self,ctx,  user:discord.Member, *,reason="no reason"):
        await ctx.send(f'**{user.display_name}** just got slapped for **{reason}**')
        await ctx.send('https://tenor.com/view/penguins-penguin-siblings-gif-7249411')


    @commands.command(brief='<question>', aliases=['q'], description="<question>")
    async def question(self, ctx, *, question):
        listOfResponses = [
            'It is certain', 'It is decidedly so', 'Without a doubt',
            'Yes – definitely', 'You may rely on it', 'As I see it, yes',
            'Most likely', 'Outlook good', 'Yes Signs point to yes', 'Yes.',
            'try again', 'Ask again later', 'Better not tell you now',
            'Cannot predict now', 'Concentrate and ask again',
            'Dont count on it', 'My reply is no', 'My sources say no',
            'Outlook not so good', 'Very doubtful',
            f'LMAO THE QUESTION "{question}" IS SO STUPID HAHAHHA?? LOL YOU HAVE IQ OF 0 LOLOLOLOL!! Never EVER talk to me AGAIN',
            'No.', 'Maybe.', 'Uhh yup 100%! Go for it!',
            'According to my intense calculation that involves M.L and A.I enhancements: YES!',
            'According to my intense calculation that involves M.L and A.I enhancements: NOPE!'
        ]
        await ctx.send(f'{random.choice(listOfResponses)}')

    @commands.command(aliases=['pog'])
    async def pogcat(self,ctx):
      if ctx.message.author.nick == None:
        await ctx.send(f'**{ctx.message.author.name}** said')
      else:  
        await ctx.send(f'**{ctx.message.author.nick}** said ')
      await ctx.send('<a:wii:803088527935537182>')

    @commands.command(aliases=['vibing','vibe'])
    async def catvibe(self, ctx):
      if ctx.message.author.nick == None:
        await ctx.send(f'**{ctx.message.author.name}** said')
      else:  
        await ctx.send(f'**{ctx.message.author.nick}** said ')
      await ctx.send('<a:vibe:821159121796726844>')

    @commands.command(aliases=['sloop', 'snomislap', 'penguinslap'])
    async def sammislap(self, ctx):
      if ctx.message.author.nick == None:
        await ctx.send(f'**{ctx.message.author.name}** said')
      else:
       await ctx.send(f'**{ctx.message.author.nick}** said ')
      await ctx.send(
        'https://tenor.com/view/penguins-penguin-siblings-gif-7249411')

    @commands.command()
    async def np(self,ctx):
      if ctx.message.author.nick == None:
        await ctx.send(f'**{ctx.message.author.name}** said')
      else:
       await ctx.send(f'**{ctx.message.author.nick}** said ')
      await ctx.send(
        'https://cdn.discordapp.com/emojis/748202594513715270.gif?v=1')

    @commands.command()
    async def haha(self,ctx):
      if ctx.message.author.nick == None:
        await ctx.send(f'**{ctx.message.author.name}** said')
      else:
       await ctx.send(f'**{ctx.message.author.nick}** said ')
      await ctx.send(
        'https://tenor.com/view/anime-cute-lol-laugh-laughs-gif-13300641')
    
    @commands.command(aliases=['pkmn'])
    async def POKEMON(self, ctx):
      await ctx.send("""
    ```                                  ___
    _.----.        ____         ,'  _\   ___    ___     ____
_,-'       `.     |    |  /`.   \,-'    |   \  /   |   |    \  |`.
\      __    \    '-.  | /   `.  ___    |    \/    |   '-.   \ |  |
 \.    \ \   |  __  |  |/    ,','_  `.  |          | __  |    \|  |
   \    \/   /,' _`.|      ,' / / / /   |          ,' _`.|     |  |
    \     ,-'/  /   \    ,'   | \/ / ,`.|         /  /   \  |     |
     \    \ |   \_/  |   `-.  \    `'  /|  |    ||   \_/  | |\    |
      \    \ \      /       `-.`.___,-' |  |\  /| \      /  | |   |
       \    \ `.__,'|  |`-._    `|      |__| \/ |  `.__,'|  | |   |
        \_.-'       |__|    `-._ |              '-.|     '-.| |   |
                                `'                            '-._|
    ```
    """)

    @commands.command()
    async def bear(self, ctx):
      await ctx.send('ʕ•ᴥ•ʔ')

    @commands.command()
    async def hi(self, ctx):
      if ctx.message.author.nick == None:
        await ctx.send(f'**{ctx.message.author.name}** said')
      else:
       await ctx.send(f'**{ctx.message.author.nick}** said ')
      await ctx.send(
        'https://cdn.discordapp.com/emojis/621517681379770383.gif?v=1')


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

    @commands.command()
    async def huggie(self,ctx):
      if ctx.message.author.nick == None:
        await ctx.send(f'**{ctx.message.author.name}** said')
      else:  
        await ctx.send(f'**{ctx.message.author.nick}** said ')
      await ctx.send('https://tenor.com/view/excited-happy-hi-gif-20937598')

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
    async def hug(self, ctx, user: discord.Member = None):
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

      await ctx.send(file = discord.File("./images/profile_hug.jpeg"))

    @commands.command(aliases=['brain'])
    async def bigbrain(self, ctx, user: discord.Member = None):
      if user == None:
        user = ctx.author
      
      brain = Image.open("./images/brain.jpeg")
      asset = user.avatar_url_as(size = 128 )
      data = BytesIO(await asset.read())
      pfp = Image.open(data)
      
      pfp = pfp.resize( (139,139) )
      brain.paste(pfp, (350,300))

      brain.save("./images/profile_brain.jpeg")

      await ctx.send(file = discord.File("./images/profile_brain.jpeg"))

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
    async def advice(self, ctx):
      response = requests.get('https://api.adviceslip.com/advice')
      await ctx.send(response.json()['slip']['advice'])

    @commands.command(aliases=['cmpt'])
    async def compliment(self, ctx, user:discord.Member):
      response = requests.get("https://complimentr.com/api")
      await ctx.send(f'{user.display_name}, {response.json()["compliment"]}')

def setup(client):
    client.add_cog(Fun(client))
