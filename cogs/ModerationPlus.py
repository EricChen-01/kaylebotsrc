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
    elif result["channel"] == None or result["join"] == None or result["leave"] == None:
      return
    else:
      embed = discord.Embed(title="***Person Joined***",color=0x14749F, description=f'{result["join"]}')
      embed.set_thumbnail(url=f'{member.avatar_url}')
      embed.set_author(name=f'{member.name}', icon_url=f'{member.avatar_url}')
      embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
      embed.timestamp = datetime.datetime.utcnow()
      channel =  self.client.get_channel(id=result["channel"])
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
    elif result["channel"] == None or result["join"] == None or result["leave"] == None:
      return
    else:
      embed = discord.Embed(title="***Person Left :(***",color=0x14749F, description=f'{result["leave"]}')
      embed.set_thumbnail(url=f'{member.avatar_url}')
      embed.set_author(name=f'{member.name}', icon_url=f'{member.avatar_url}')
      embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
      embed.timestamp = datetime.datetime.utcnow()
      channel =  self.client.get_channel(id=result["channel"])
      await channel.send(embed=embed)

  #on message delete
  @commands.Cog.listener()
  async def on_message_delete(self,message):
    msg = message.content
    author = message.author

    guildID = message.guild.id
    result = svrCollection.find_one({"_id":guildID})

    if result == None:
      return
    elif result['audit_log'] == None:
      return
    else:
      embed = discord.Embed(title=f"***Message Deleted in #{message.channel.name}***",color=0x14749F, description=f'{msg}')
      embed.set_thumbnail(url=f'{author.avatar_url}')
      embed.set_author(name=f'{author.name}', icon_url=f'{author.avatar_url}')
      embed.set_footer(text=f"{author.guild}", icon_url=f"{author.guild.icon_url}")
      embed.timestamp = datetime.datetime.utcnow()
      channel =  self.client.get_channel(id=result["audit_log"])
      await channel.send(embed=embed)
  
  #server data removeal apon leave
  @commands.Cog.listener()
  async def on_guild_remove(self,guild):
    guildID = ctx.guild.id
    result = svrCollection.find_one({"_id":guildID})
    if result == None:
      return
    else:
      svrCollection.delete_one({"_id":guild.id})

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
    elif result['audit_log'] == None:
      return
    else:
      embed = discord.Embed(title=f"***Role was created: @{role_name}***",color=0x14749F)
      embed.set_thumbnail(url=f'{guild.icon_url}')
      embed.set_footer(text=f"{guild}", icon_url=f"{guild.icon_url}")
      embed.timestamp = time_of_creation
      channel =  self.client.get_channel(id=result["audit_log"])
      await channel.send(embed=embed)

  #commands  
  #server registration
  @commands.group(invoke_without_command=True)
  async def setup(self,ctx):
    await ctx.send('Setup commands: \nsetup server \nsetup channel [#channel] \nsetup join [message] \nsetup leave [message] \nsetup log [#channel] \nsetup reset')

  @setup.command()
  @commands.has_permissions(administrator=True)
  async def log(self,ctx, channel: discord.TextChannel):
    guildID = ctx.message.author.guild.id
    result = svrCollection.find_one({"_id":guildID})

    if result == None:
      await ctx.send('This server is not registered.')
    else:
      svrCollection.update_one({"_id":ctx.guild.id}, {"$set":{"audit_log": channel.id}})
      await ctx.send(f'Audit log channel has been updated to {channel.mention}')

  @setup.command()
  @commands.has_permissions(administrator=True)
  async def server(self,ctx):
    guildID = ctx.guild.id
    result = svrCollection.find_one({"_id":guildID})
    if result == None:
      newServer = {"_id":guildID, "channel": None, "join": None, "leave": None, "audit_log": None}
      svrCollection.insert_one(newServer)
      await ctx.send('Server successfully registered.')
    else:
      await ctx.send('This server is already registered.')

  @setup.command()
  @commands.has_permissions(administrator=True)
  async def channel(self,ctx, channel: discord.TextChannel):
    guildID = ctx.message.author.guild.id
    result = svrCollection.find_one({"_id":guildID})

    if result == None:
      await ctx.send('This server is not registered.')
    else:
      svrCollection.update_one({"_id":ctx.guild.id}, {"$set":{"channel": channel.id}})
      await ctx.send(f'Channel has been updated to {channel.mention}')

  @setup.command()
  @commands.has_permissions(administrator=True)
  async def join(self,ctx, *,msg):
    guildID = ctx.guild.id
    result = svrCollection.find_one({"_id":guildID})

    if result == None:
      await ctx.send('This server is not registered.')
    else:
      svrCollection.update_one({"_id":ctx.guild.id}, {"$set":{"join": msg}})
      await ctx.send(f'Welcome message has been set to "{msg}".')

  @setup.command()
  @commands.has_permissions(administrator=True)
  async def leave(self,ctx, *,msg):
    guildID = ctx.guild.id
    result = svrCollection.find_one({"_id":guildID})

    if result == None:
      await ctx.send('This server is not registered.')
    else:
      svrCollection.update_one({"_id":ctx.guild.id}, {"$set":{"leave": msg}})
      await ctx.send(f'Leave message has been set to "{msg}".')

  @setup.command()
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

  #experimental
  @commands.group(invoke_without_command=True)
  async def experimental(self,ctx):
    setup = discord.Embed(title=f"***Server Setup For {ctx.guild.name}***",color=0x14749F)
    setup.add_field(name='***Join/Leave Channel***', value=f'Please reply with channel id.', inline=True)
    setup.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.author.guild.icon_url}")
    setup.timestamp = datetime.datetime.utcnow()
    sent = await ctx.send(embed=setup)

    channel = None
    join = None
    leave = None
    auditLog = None
    try:
      reply = await self.client.wait_for(
        "message",
        timeout=10,
        check = lambda message: message.author == ctx.author and message.channel == ctx.channel
      )
      if reply: 
        await sent.delete()
        await reply.delete()
        channel = reply.content

        setup.clear_fields()
        setup.add_field(name='***Join Message***', value=f'Please reply with a message.', inline=True)

        sent = await ctx.send(embed=setup)

        reply = await self.client.wait_for(
        "message",
        timeout=10,
        check = lambda message: message.author == ctx.author and message.channel == ctx.channel
        ) 
        if reply:
          await sent.delete()
          await reply.delete()
          join = reply.content

          setup.clear_fields()
          setup.add_field(name='***Leave Message***', value=f'Please reply with a message.', inline=True)

          sent = await ctx.send(embed=setup)

          reply = await self.client.wait_for(
            "message",
            timeout=10,
            check = lambda message: message.author == ctx.author and message.channel == ctx.channel
          ) 
          if reply:
            await sent.delete()
            await reply.delete()

            leave = reply.content

            await ctx.send(f'{channel}, {join}, {leave}, {auditLog}')


    except asyncio.TimeoutError:
      await sent.delete()
      await ctx.send('Setup timedout.', delete_after=10)

def setup(client):
  client.add_cog(ModerationPlus(client))
