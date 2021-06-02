import discord
from discord.ext import commands
import os
import asyncio
import random

intents = discord.Intents.all()

client = commands.Bot(case_insensitive=True, command_prefix='.k ', intents=intents)
client.remove_command("help")

#Bot is ready
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle)


#changing bot status
async def change_stat():
    await client.wait_until_ready()
    statuses = [
        'Chilling', '.k help', 'Version 2.0',
        f'on {len(client.guilds)} servers', 
    ]
    while not client.is_closed():
        status = random.choice(statuses)
        await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=status))
        await asyncio.sleep(60)


#error handling
@client.event
async def on_command_error(ctx, error):
  displayName = ctx.message.author.display_name

  if isinstance(error, commands.MissingPermissions):
    await ctx.send(f"Sorry {displayName}! You do not have the permission use this.")
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f"Sorry {displayName}! Missing required arguments!")
  elif isinstance(error, commands.CommandOnCooldown):
    await ctx.send(f"Sorry {displayName}! This command is on cooldown. Please try again in {round(error.retry_after, 2)} seconds")
  else:
    await ctx.send(f"Sory {displayName}! I don't know this command!")
  pass


#cog loaders
@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


#help command
@client.group(case_insensitive=True, invoke_without_command=True)
async def help(ctx):
  em = discord.Embed(title = "Help", description = '[click me for help](https://ericchen-01.github.io/KAYLEBOT)', color = ctx.author.color)
  await ctx.send(embed = em)


client.loop.create_task(change_stat())
client.run(os.getenv("TOKEN"))
