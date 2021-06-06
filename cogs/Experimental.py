import aiohttp
import asyncio
import os
import discord
from discord.ext import commands
import datetime


header = {"x-api-key": os.getenv("PRSAWAPIKEY")}

class Experimental(commands.Cog):
  def __init__(self, client):
        self.client = client
  #commands
  #experimental
  @commands.command()
  async def outside(self,ctx):
    await serverSet(self=self,ctx=ctx)
def setup(client):
  client.add_cog(Experimental(client))

async def serverSet(self,ctx):
    #Embed and variables
    em = discord.Embed(title ='***Server Setup***',color=0x14749F)
    em.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
    em.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.author.guild.icon_url}")
    em.timestamp = datetime.datetime.utcnow()
    channel = None
    joinMessage = None
    leaveMessage = None
    audit_log = None

    channelComplete = False

    #Channel
    em.add_field(name='***Channel ID: Step 1/4***', value='reply with a channel id. Reply with "NONE" to skip this step. ', inline=True)
    em.add_field(name='***NOTE:***', value ='replying with "NONE" will skips steps 2 and 3.', inline=False)
    sent = await ctx.send(embed=em)
    response = await respond(self=self,ctx=ctx)
    await sent.add_reaction('\U00000031')
    if response != "NONE":
        channel = response
        channelComplete = True

    #join message
    await clearEmbed(self, ctx, em)
    #await sent.add_reaction('\U00000032')
    if channelComplete:
        em.add_field(name='***Join Message: Step 2/4***', value='reply with a join message. Reply with "NONE" to skip this step.', inline=True)
        await sent.edit(embed=em)
        response = await respond(self=self,ctx=ctx)
        if response != "NONE":
            joinMessage = response

    #leave message
    await clearEmbed(self,ctx,em)
    #await sent.add_reaction('\U00000033')
    if channelComplete:
        em.add_field(name='***Leave Message: Step 3/4***', value='reply with a Leave Message. Reply with "NONE" to skip this step.', inline=True)
        await sent.edit(embed=em)
        response = await respond(self=self,ctx=ctx)

        if response != "NONE":
            leaveMessage = response

    #audit log
    await clearEmbed(self,ctx,em)
    #await sent.add_reaction('\U00000034')
    em.add_field(name='***Audit Log: Step 4/4***', value='reply with a channel id. Reply with "NONE" to skip this step.', inline=True)
    await sent.edit(embed=em)
    response = await respond(self=self,ctx=ctx)

    if response != "NONE":
        audit_log = response

    await ctx.send(f"Channel: {channel}\nJoinMessage: {joinMessage}\nleaveMessage: {leaveMessage}\naudit_log: {audit_log}")

@commands.command()
async def testt(self,ctx):
    msg = await ctx.send("hi")
    await msg.add_reaction('\U00000031')


async def respond(self,ctx):
    try:
        msg = await self.client.wait_for("message", check= lambda message: message.author == ctx.author and message.channel == ctx.channel, timeout = 30.0)
    except asyncio.TImeoutError:
        await ctx.send('Setup timed out.')

    else:
        message = msg.content
        if message == "NONE":
            return "NONE"
        else:
            return message

async def clearEmbed(self,ctx, embed):
    embed.clear_fields()



