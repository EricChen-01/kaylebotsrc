import aiohttp
import asyncio
import os
import discord
from discord.ext import commands
import datetime
import pymongo
from pymongo import MongoClient

serverCluster = MongoClient(f'mongodb+srv://Kayle:{os.getenv("mongoDBPassword")}@discordkayledb.ddcpx.mongodb.net/server?retryWrites=true&w=majority')
serverdb = serverCluster["server"]
svrCollection = serverdb["server"]

class Experimental(commands.Cog):
  def __init__(self, client):
        self.client = client
  #commands
  #experimental
  @commands.command()
  async def _setup(self,ctx, setupMode = None):
    if setupMode == "auto":
        em = discord.Embed(title ='***Server Setup***',color=0x14749F)
        em.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        em.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.author.guild.icon_url}")
        await ctx.send('Auto Server Setup.')
    else:
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
    em.add_field(name='***Channel ID: Step 1/4***', value='reply with a channel id. Reply with "NONE" to skip this step. Reply with "QUIT" to end setup.', inline=True)
    em.add_field(name='***NOTE:***', value ='replying with "NONE" will skips steps 2 and 3.', inline=False)
    sent = await ctx.send(embed=em)
    await sent.add_reaction("\U0001f60e")
    while(True):
        response = await respond(self=self,ctx=ctx)
        if response == None or response == "QUIT":
            await clearEmbed(self,ctx,em)
            em.add_field(name='***Setup Cancled***', value='Server setup cancled due to timeout or user selected: "QUIT"', inline=True)
            em.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
            em.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.author.guild.icon_url}")
            em.timestamp = datetime.datetime.utcnow()
            await sent.edit(embed=em)
            return

        if response != "NONE":
            valid = await isValid(self,ctx,response)
            if valid == None:
                await ctx.send('This is an invalid text channel. Please enter a valid text channel.')
            else:
                channel = valid
                channelComplete = True
                break
        else:
            break
            

    #join message
    await clearEmbed(self, ctx, em)
    await sent.add_reaction("\U0001f922")
    if channelComplete:
        em.add_field(name='***Join Message: Step 2/4***', value='reply with a join message. Reply with "NONE" to skip this step. Reply with "QUIT" to end setup.', inline=True)
        await sent.edit(embed=em)
        response = await respond(self=self,ctx=ctx)
        if response == None or response == "QUIT":
            await clearEmbed(self,ctx,em)
            em.add_field(name='***Setup Cancled***', value='Server setup cancled due to timeout or user selected: "QUIT"', inline=True)
            em.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
            em.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.author.guild.icon_url}")
            em.timestamp = datetime.datetime.utcnow()
            await sent.edit(embed=em)
            return

        if response != "NONE":
            joinMessage = response


    #leave message
    await clearEmbed(self,ctx,em)
    await sent.add_reaction("\U0001f44d")
    if channelComplete:
        em.add_field(name='***Leave Message: Step 3/4***', value='reply with a Leave Message. Reply with "NONE" to skip this step. Reply with "QUIT" to end setup.', inline=True)
        await sent.edit(embed=em)
        response = await respond(self=self,ctx=ctx)

        if response == None or response == "QUIT":
            await clearEmbed(self,ctx,em)
            em.add_field(name='***Setup Cancled***', value='Server setup cancled due to timeout or user selected: "QUIT"', inline=True)
            em.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
            em.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.author.guild.icon_url}")
            em.timestamp = datetime.datetime.utcnow()
            await sent.edit(embed=em)
            return

        if response != "NONE":
            leaveMessage = response


    #audit log
    await clearEmbed(self,ctx,em)
    await sent.add_reaction("\U0001fab3")
    em.add_field(name='***Audit Log: Step 4/4***', value='reply with a channel id. Reply with "NONE" to skip this step. Reply with "QUIT" to end setup.', inline=True)
    await sent.edit(embed=em)
    

    while(True):
        response = await respond(self=self,ctx=ctx)
        if response == None or response == "QUIT":
            await clearEmbed(self,ctx,em)
            em.add_field(name='***Setup Cancled***', value='Server setup cancled due to timeout or user selected: "QUIT"', inline=True)
            em.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
            em.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.author.guild.icon_url}")
            em.timestamp = datetime.datetime.utcnow()
            await sent.edit(embed=em)
            return

        if response != "NONE":
            valid = await isValid(self,ctx,response)
            if valid == None:
                await ctx.send('This is an invalid text channel. Please enter a valid text channel.')
            else:
                audit_log = valid
                break
        else:
            break


    #displays final setup
    await clearEmbed(self,ctx,em)
    em.add_field(name='***Setup Complete***', value='These are your server settings.', inline=True)
    em.add_field(name='***Channel***', value=f'{channel}', inline=True)
    em.add_field(name='***Join Message***', value=f'{joinMessage}', inline=True)
    em.add_field(name='***Leave Message***', value=f'{leaveMessage}', inline=True)
    em.add_field(name='***Audit Log***', value=f'{audit_log}', inline=True)
    em.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
    em.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.author.guild.icon_url}")
    em.timestamp = datetime.datetime.utcnow()
    await sent.edit(embed=em)
    await sent.add_reaction("\U00002705")
    
    #add/update Server
    await addServer(self,ctx,channel,joinMessage, leaveMessage, audit_log)
    
async def respond(self,ctx):
    try:
        msg = await self.client.wait_for("message", check= lambda message: message.author == ctx.author and message.channel == ctx.channel, timeout = 30.0)
    except asyncio.TimeoutError:
        await ctx.send('Setup timed out.')
        return None
    else:
        message = msg.content
        if message == "NONE":
            return "NONE"
        else:
            return message

async def clearEmbed(self,ctx, embed):
    embed.clear_fields()

async def isValid(self,ctx,response):
    channel_ID= None
    guild = ctx.guild
    if response.startswith('<#'):
        size = len(response)
        channelID = response[2:size - 1]
        channel = discord.utils.get(guild.text_channels, id=int(channelID))
        if channel != None:
            channel_ID = int(channelID)
    elif response.isdecimal():
        channel = discord.utils.get(guild.text_channels, id=int(response))
        if channel != None:
            channel_ID = int(response)
    else:
        channel = None
    
    return channel_ID

async def addServer(self,ctx,channel,join, leave, audit_log):
    guildID = ctx.guild.id
    result = svrCollection.find_one({"_id":guildID})
    if result == None:
        newServer = {"_id":guildID, "channel": channel, "join": join, "leave": leave, "audit_log": audit_log}
        svrCollection.insert_one(newServer)
        await ctx.send('Server successfully registered.')
    else:
        svrCollection.update_one({"_id":ctx.guild.id}, {"$set":{"channel": channel, "join":join, "leave":leave, "audit_log": audit_log}})
        await ctx.send("Server settings updated")




