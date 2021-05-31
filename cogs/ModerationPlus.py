import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import os
#run python -m pip install pymongo[srv] if error
cluster = MongoClient(f'mongodb+srv://Kayle:{os.getenv("mongoDBPassword")}@discordkayledb.ddcpx.mongodb.net/KayleBotDataBase?retryWrites=true&w=majority')
db = cluster["KayleBotDataBase"]
collection = db["Users"]

class ModerationPlus(commands.Cog):
  def __init__(self, client):
        self.client = client

  #commands
  #database
  @commands.command()
  async def register(self, ctx):
    authorID = ctx.message.author.id
    result = collection.find_one({"_id":authorID})
    if result == None:
      await ctx.send(f'Registered {ctx.message.author.display_name} into the database.')
      newUser = {"_id":authorID, "name": ctx.message.author.display_name, "reports": 0, "balance": 0}
      collection.insert_one(newUser)
    else:
      await ctx.send(f'User: {ctx.message.author.display_name} is alredy in the database.')
  
  @commands.command()
  async def unregister(self, ctx):
    authorID = ctx.message.author.id
    result = collection.find_one({"_id":authorID})
    if result == None:
      await ctx.send(f'{ctx.message.author.display_name} is not in the database.')
    else:
      await ctx.send(f'Deleting: {ctx.message.author.display_name} from the database.')
      collection.delete_one({"_id":authorID})

  @commands.command()
  async def resetDataBase(self,ctx):
    if ctx.author.id == 235103490869821440:
      await ctx.send('Reseting the database.')
      collection.delete_many({})

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
  @commands.has_permissions(administrator=True)
  async def ban(self, ctx, user: discord.Member, reason='no reason'):
    userID = user.id
    await ctx.guild.ban(user)
    await self.client.send_message(user, reason)
    await ctx.send(f'{user.display_name} has been banned for the reason: {reason}')

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def unban(self, ctx, user: discord.Member, reason='no reason'):
    await ctx.guild.unban(user)
    await ctx.send(f'{user.display_name} has been unbanned for the reason: {reason}')
  
  
  
def setup(client):
  client.add_cog(ModerationPlus(client))
