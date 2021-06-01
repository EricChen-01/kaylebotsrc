import discord
from discord.ext import commands


class Details(commands.Cog):
  def __init__(self, client):
        self.client = client
  #commands
  @commands.command(aliases=['v','-v'])
  async def version(self,ctx):
    servers = self.client.guilds
    versionEmbed = discord.Embed(title="KAYLE's Version: THE FUN UPDATE",
                                 description="""```css\nVersion 2.0```""",
                                 color=0x14749F)
    versionEmbed.add_field(name="Version Code:", value="""```css\nv1.4.1```""", inline=False)
    versionEmbed.add_field(name="2.0.0 Patch Notes:",
    value="""```
Version 2.0.0:
+ Revamped Fun,KAYLEAI, Moderation.    
+ New Moderation commands
- Cross Server Communication
- .k meme [subreddit]
- old fun commands 
    ```""",
                           inline=False)
    versionEmbed.add_field(name="Version Date Released:",
                           value="June, 2021",
                           inline=False)
    versionEmbed.add_field(name="BOT BIRTHDATE:",
                           value="March 13, 2021",
                           inline=False)
    versionEmbed.add_field(
      name="KAYLE is on many servers!",
      value=f"Connected on {str(len(servers))} servers.",
      inline=False
    )
    versionEmbed.set_footer(text="Created by Yatami")
    versionEmbed.set_author(name="KAYLE",icon_url='https://i.imgur.com/nTvmVkH.png')
    await ctx.send(embed=versionEmbed)

  @commands.command()
  async def servers(self, ctx):
    activeservers = self.client.guilds
    for guild in activeservers:
        await ctx.send(guild.name)
        print(guild.name)  
  
def setup(client):
  client.add_cog(Details(client))
