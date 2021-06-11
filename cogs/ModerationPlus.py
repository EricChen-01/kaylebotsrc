import discord
from discord.ext import commands
from discord.ext.commands.core import is_owner
import pymongo
from pymongo import MongoClient
import os
import datetime
import asyncio
#run python -m pip install pymongo[srv] if error
cluster = MongoClient(f'mongodb+srv://Kayle:{os.getenv("mongoDBPassword")}@discordkayledb.ddcpx.mongodb.net/KayleBotDataBase?retryWrites=true&w=majority')
db = cluster["KayleBotDataBase"]
collection = db["Users"]

serverCluster = MongoClient(f'mongodb+srv://Kayle:{os.getenv("mongoDBPassword")}@discordkayledb.ddcpx.mongodb.net/server?retryWrites=true&w=majority')
serverdb = serverCluster["server"]
svrCollection = serverdb["server"]



class ModerationPlus(commands.Cog):
  def __init__(self, client):
        self.client = client

  #events
  #join/leave messages
  @commands.Cog.listener()
  async def on_member_join(self, member):
    #welcome message if server is registered and all required fields are active.
    guildID = member.guild.id
    result = svrCollection.find_one({"_id":guildID})
    if result == None:
      return
    
    channel = discord.utils.get(member.guild.text_channels, id=result["channel"])

    #custom variables for messages
    userName = member.name
    guildName = member.guild
    mentionUser = member.mention
    count = member.guild.member_count

    if result["channel"] == None or channel == None or result["join"] == None:
      return
    else:
      embed = discord.Embed(title="***Person Joined***",color=0x14749F, description=str(result["join"]).format(count=count,mention=mentionUser,user=userName, guildName=guildName))
      embed.set_thumbnail(url=f'{member.avatar_url}')
      embed.set_author(name=f'{member.name}', icon_url=f'{member.avatar_url}')
      embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
      embed.timestamp = datetime.datetime.utcnow()
      await channel.send(embed=embed)

    #checks if user is registered and registers then if not
    authorID = member.id
    result = collection.find_one({"_id":authorID})
    if result == None:
      newUser = {"_id":authorID, "name": member.display_name, "reports": 0, "balance": 0}
      collection.insert_one(newUser)

  @commands.Cog.listener()
  async def on_member_remove(self, member):
    guildID = member.guild.id
    result = svrCollection.find_one({"_id":guildID})

    if result == None:
      return

    channel = discord.utils.get(member.guild.text_channels, id=result["channel"])


    #custom variables for messages
    userName = member.name
    guildName = member.guild
    mentionUser = member.mention
    count = member.guild.member_count

    if result["channel"] == None or channel == None or result["leave"] == None:
      return
    else:
      embed = discord.Embed(title="***Person Left :(***",color=0x14749F, description=str(result["leave"]).format(count=count,mention=mentionUser,user=userName, guildName=guildName))
      embed.set_thumbnail(url=f'{member.avatar_url}')
      embed.set_author(name=f'{member.name}', icon_url=f'{member.avatar_url}')
      embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
      embed.timestamp = datetime.datetime.utcnow()
      await channel.send(embed=embed)

  #on message delete
  @commands.Cog.listener()
  async def on_message_delete(self,message):
    msg = message.content
    author = message.author

    guildID = message.guild.id
    result = svrCollection.find_one({"_id":guildID})

    channel = discord.utils.get(message.guild.text_channels, id=result["audit_log"])

    if result == None or result['audit_log'] == None or channel == None:
      return
    else:
      embed = discord.Embed(title=f"***Message Deleted in #{message.channel.name}***",color=0x14749F, description=f'{msg}')
      embed.set_thumbnail(url=f'{author.avatar_url}')
      embed.set_author(name=f'{author.name}', icon_url=f'{author.avatar_url}')
      embed.set_footer(text=f"{author.guild}", icon_url=f"{author.guild.icon_url}")
      embed.timestamp = datetime.datetime.utcnow()
      await channel.send(embed=embed)
  
  #server data removeal apon leave
  @commands.Cog.listener()
  async def on_guild_remove(self,guild):
    guildID = guild.id
    result = svrCollection.find_one({"_id":guildID})
    if result == None:
      return
    else:
      svrCollection.delete_one({"_id":guildID})

  #on role creation
  @commands.Cog.listener()
  async def on_guild_role_create(self,role):
    role_name = role.name 
    time_of_creation = role.created_at

    guildID = role.guild.id
    guild = role.guild
    result = svrCollection.find_one({"_id":guildID})

    if result == None:
      return
    
    channel = discord.utils.get(guild.text_channels, id=result["audit_log"])

    if result['audit_log'] == None or channel == None:
      return
    else:
      embed = discord.Embed(title=f"***Role was created: @{role_name}***",color=0x14749F)
      embed.set_thumbnail(url=f'{guild.icon_url}')
      embed.set_footer(text=f"{guild}", icon_url=f"{guild.icon_url}")
      embed.timestamp = time_of_creation
      await channel.send(embed=embed)

  #commands  
  #server registration
  @commands.command()
  async def setup(self,ctx, setupMode = None):
    if setupMode == "auto":
        #creating a new category
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(send_messages=True)
        }
        category = await ctx.guild.create_category(name='SERVER INFO', overwrites=overwrites)

        welcomeChannel = await category.create_text_channel(name="Welcome", overwrites = overwrites)
        joinMessage = "Welcome {user} to the server!"
        leaveMessage = "{user} left the server :("
        logChannel = await category.create_text_channel(name="logs", overwrites = overwrites)

        em = discord.Embed(title ='***Server Auto Setup***',color=0x14749F)
        em.add_field(name='***Setup Complete***', value='These are your server settings.', inline=False)
        em.add_field(name='***Channel***', value=f'{welcomeChannel.id}', inline=False)
        em.add_field(name='***Join Message***', value=f'{joinMessage}', inline=False)
        em.add_field(name='***Leave Message***', value=f'{leaveMessage}', inline=False)
        em.add_field(name='***Audit Log***', value=f'{logChannel.id}', inline=False)
        em.set_author(name=f'{ctx.author.name}', icon_url=f'{ctx.author.avatar_url}')
        em.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.author.guild.icon_url}")
        em.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=em)
        await addServer(self,ctx, welcomeChannel.id, joinMessage, leaveMessage, logChannel.id)
    else:
        await serverSet(self=self,ctx=ctx)

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def log(self,ctx, channel: discord.TextChannel):
    guildID = ctx.message.author.guild.id
    result = svrCollection.find_one({"_id":guildID})

    if result == None:
      await ctx.send('This server is not registered.')
    else:
      svrCollection.update_one({"_id":ctx.guild.id}, {"$set":{"audit_log": channel.id}})
      await ctx.send(f'Audit log channel has been updated to {channel.mention}')

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def channel(self,ctx, channel: discord.TextChannel):
    guildID = ctx.message.author.guild.id
    result = svrCollection.find_one({"_id":guildID})

    if result == None:
      await ctx.send('This server is not registered.')
    else:
      svrCollection.update_one({"_id":ctx.guild.id}, {"$set":{"channel": channel.id}})
      await ctx.send(f'Channel has been updated to {channel.mention}')

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def join(self,ctx, *,msg):
    guildID = ctx.guild.id
    result = svrCollection.find_one({"_id":guildID})

    if result == None:
      await ctx.send('This server is not registered.')
    else:
      svrCollection.update_one({"_id":ctx.guild.id}, {"$set":{"join": msg}})
      await ctx.send(f'Welcome message has been set to "{msg}".')

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def leave(self,ctx, *,msg):
    guildID = ctx.guild.id
    result = svrCollection.find_one({"_id":guildID})

    if result == None:
      await ctx.send('This server is not registered.')
    else:
      svrCollection.update_one({"_id":ctx.guild.id}, {"$set":{"leave": msg}})
      await ctx.send(f'Leave message has been set to "{msg}".')

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def reset(self,ctx, *,resets = "all"):
    guildID = ctx.guild.id
    result = svrCollection.find_one({"_id":guildID})
    if result == None:
      await ctx.send('This server is not registered.')
      return
    
    listOfResets = resets.split(',')
    for element in listOfResets:
      if element == "all":
        svrCollection.update_one({"_id":ctx.guild.id}, {"$set":{"channel": None, "join":None, "leave":None, "audit_log": None}})
      elif element == "channel":
        svrCollection.update_one({"_id":ctx.guild.id}, {"$set":{"channel": None}})
      elif element == "join":
        svrCollection.update_one({"_id":ctx.guild.id}, {"$set":{"join": None}})
      elif element == "leave":
        svrCollection.update_one({"_id":ctx.guild.id}, {"$set":{"leave": None}})
      elif element == "audit_log":
        svrCollection.update_one({"_id":ctx.guild.id}, {"$set":{"audit_log": None}})
      else:
        await ctx.send(f'{element} could not be found.')
    
    await ctx.send("Server setting(s) reset.")

  @commands.command()
  @commands.has_permissions(administrator = True)
  async def settings(self,ctx):
    guildID = ctx.guild.id
    result = svrCollection.find_one({"_id":guildID})
    if result == None:
      await ctx.send('There are no settings for this server. Please register server using ".k setup server" and customize accordingly.')
      return
    
    settings = ""
    for field in result:
      settings = settings + f'{field} = {result[field]}\n'
    
    await ctx.send(settings)

  #reports/details
  @commands.command()
  async def report(self,ctx, user: discord.Member=None, field="-i"):
    if user == None:
      await ctx.send('Please specify a user to report.')
    else:
      result = collection.find_one({"_id":user.id})
      if result == None:
        await ctx.send('User cannot be reported')
      elif field == "-i":
        collection.update_one({"_id": user.id},{"$inc":{"reports": 1}})
        await ctx.send(f'{user.display_name} has been reported.')  
      elif field == "-d":
        result = collection.find_one({"_id": user.id})
        if result["reports"] - 1 < 0:
          collection.update_one({"_id": user.id},{"$set":{"reports": 0}})
        else:
          collection.update_one({"_id": user.id},{"$inc":{"reports": -1}})
        await ctx.send(f"{user.display_name}'s report has been decremented.")  
      elif field == "-rs":
        collection.update_one({"_id": user.id},{"$set":{"reports": 0}})
        await ctx.send(f"{user.display_name}'s reports has been reset to zero.")      
    
  @commands.command()
  async def whois(self, ctx, user: discord.Member=None):
    if user == None:
      await ctx.send('Please specify a user.')
    else:
      result = collection.find_one({"_id": user.id})
      if result == None:
        await ctx.send('User is not registered.')
      else:
        userDetails = discord.Embed(title=f'***{result["name"]}***', color=0x14749F)
        userDetails.add_field(name='***ID***', value=f'{result["_id"]}', inline=False)
        userDetails.add_field(name='***Reports***', value=f'{result["reports"]}', inline=False)
        userDetails.add_field(name='***Balance***', value=f'{result["balance"]}', inline=False)
        userDetails.set_image(url= user.avatar_url)
        await ctx.send(embed=userDetails)

  #unregistering user
  @commands.command()
  @commands.has_permissions(administrator = True)
  async def unregister(self, ctx):
    authorID = ctx.message.author.id
    result = collection.find_one({"_id":authorID})
    if result == None:
      await ctx.send(f'{ctx.message.author.display_name} is not in the database.')
    else:
      await ctx.send(f'Deleting: {ctx.message.author.display_name} from the database.')
      collection.delete_one({"_id":authorID})
  
  #chat moderation
  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def clear(self, ctx, amount=None, notif="-ns"):
    if amount == None:
      await ctx.channel.purge(limit=5 + 1)
      if( not(notif == "-s") ):
        await ctx.send(f'Cleared 5 messages')
    elif amount == "all":
      await ctx.channel.purge()
      if( not(notif == "-s") ):
        await ctx.send(f'Cleared all messages from the past 14 day')
    elif int(amount) <= 0 or int(amount) > 30:
        await ctx.send('bruh you stoopid')
    else:
      await ctx.channel.purge(limit=int(amount) + 1)
      if( not(notif == "-s") ):
        await ctx.send(f'Cleared {amount} messages')

  @commands.command(pass_context=True)
  @commands.has_permissions(manage_messages=True)
  async def nick(self,ctx, member: discord.Member, *,nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')

  @commands.command()
  @commands.has_permissions(ban_members = True)
  async def ban(self, ctx, user: discord.Member, reason='no reason'):
    await user.send(f'You have been banned from {user.guild.name} for the reason: {reason}.')
    await user.ban(reason=reason)
    await ctx.send(f'{user.display_name} has been banned for the reason: {reason}.')

  @commands.command()
  @commands.has_permissions(ban_members = True)
  async def unban(self, ctx, *, member):

    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')

    for banned_entry in banned_users:
      user = banned_entry.user

      if (user.name,user.discriminator) == (member_name,member_disc):
        await ctx.guild.unban(user)
        await ctx.send(f'{member_name} has been unbanned.')
        return
    ctx.send(f'{member}was not found.')

  @commands.command()
  @commands.has_permissions(kick_members = True)
  async def kick(self, ctx, user:discord.Member, *,reason='no reason'):
    await user.kick(reason=reason)
    await user.send(f'You have been kicked from {user.guild.name} for the reason: {reason}.')
    await ctx.send(f'{user.display_name} has been kicked for: "{reason}"')

  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def lockdown(self, ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send('This channel is now locked.')

  @commands.command()
  @commands.has_permissions(manage_channels=True)
  async def unlock(self, ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send('This channel has been unlocked.')


def setup(client):
  client.add_cog(ModerationPlus(client))

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
        em.add_field(name='***Join Message: Step 2/4***', value='Reply with a join message. Reply with "NONE" to skip this step. Reply with "QUIT" to end setup.', inline=True)
        em.add_field(name='***Special tags***', value="Add {count}, {guildName} ,{mention}, and {user} to customize the message :D", inline=False)
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
        em.add_field(name='***Special tags***', value="Add {count}, {guildName} ,{mention}, and {user} to customize the message :D", inline=False)
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
        msg = await self.client.wait_for("message", check= lambda message: message.author == ctx.author and message.channel == ctx.channel, timeout = 60.0)
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