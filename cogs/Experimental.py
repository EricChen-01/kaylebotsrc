import aiohttp
import asyncio
import os
import discord
from discord.ext import commands


header = {"x-api-key": os.getenv("PRSAWAPIKEY")}

class Experimental(commands.Cog):
  def __init__(self, client):
        self.client = client
  #commands
  #experimental
  @commands.command()
  async def outside(self,ctx):
    await setup(self=self,ctx=ctx)
def setup(client):
  client.add_cog(Experimental(client))

async def setup(self,ctx):
    channel = None
    joinMessage = None
    leaveMessage = None
    audit_log = None

    channelComplete = False
    joinComplete = False
    leaveComplete = False
    auditComplete = False

    #Channel
    em = discord.Embed(title ='***Server Setup***')
    em.add_field(name='***Channel ID***', value='reply with a channel id. Reply with "NONE" to skip this step.', inline=True)
    sent = await ctx.send(embed=em)
    response = respond(self=self,ctx=ctx)
    if response == "NONE":
        channel = None
    else:
        channel = response
        channelComplete = True

    #join message
    await clearEmbed(self, ctx, em)
    if channelComplete:
        em.add_field(name='***Join Message***', value='reply with a join message. Reply with "NONE" to skip this step.', inline=True)
        sent.edit(embed=em)
        response = respond(self=self,ctx=ctx)

        if response != "NONE":
            joinMessage = response
            joinComplete = True
        else:
            joinComplete = True
    
    #leave message
    await clearEmbed(self,ctx,em)
    if joinComplete:
        em.add_field(name='***Leave Message***', value='reply with a Leave Message. Reply with "NONE" to skip this step.', inline=True)
        sent.edit(embed=em)
        response = respond(self=self,ctx=ctx)

        if response != "NONE":
            leaveMessage = response
            leaveComplete = True
        else:
            leaveComplete = True
    
    #audit log
    await clearEmbed(self,ctx,em)
    em.add_field(name='***Audit Log***', value='reply with a channel id. Reply with "NONE" to skip this step.', inline=True)
    sent.edit(embed=em)
    response = respond(self=self,ctx=ctx)

    if response != "NONE":
        audit_log = response
        auditComplete = True
    else:
        auditComplete = True

    await ctx.send(f"Channel: {channel}\nJoinMessage: {joinMessage}\nleaveMessage: {leaveMessage}\naudit_log: {audit_log}")




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



