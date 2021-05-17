import discord
from discord.ext import commands
import os
import asyncio
import random
from keep_alive import keep_alive

intents = discord.Intents.all()

client = commands.Bot(case_insensitive=True, command_prefix='.k ', intents=intents)
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle)


async def change_stat():
    await client.wait_until_ready()
    statuses = [
        'Jamming to Music', 'Partying!', 'Chilling', '.k help', '👀웃웃웃웃웃👀',
        f'on {len(client.guilds)} servers', 'How ya doin'
    ]
    while not client.is_closed():
        status = random.choice(statuses)
        await client.change_presence(status=discord.Status.idle,
                                     activity=discord.Activity(
                                         type=discord.ActivityType.watching,
                                         name=status))
        await asyncio.sleep(60)


@client.event
async def on_command_error(ctx, error):
  if ctx.message.author.nick == None:
    await ctx.send(f"Sorry {ctx.message.author.name}! I don't understand the command!")
  else:
    await ctx.send(f"Sorry {ctx.message.author.nick}! I don't understand the command!")
  pass


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


@client.group(case_insensitive=True, invoke_without_command=True)
async def help(ctx):
  em = discord.Embed(title = "Help", description = '[click me for help](https://ericchen-01.github.io/KAYLEBOT)', color = ctx.author.color)
  await ctx.send(embed = em)


client.loop.create_task(change_stat())
keep_alive()
client.run(os.getenv("TOKEN"))
