import discord
from discord.ext import commands
import os
import asyncio
import random
import datetime

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
  em = discord.Embed(title = "***Help***", description = 'These are the categories for commands.', color = ctx.author.color)
  em.add_field(name='***Fun***', value='[FUN](https://ericchen-01.github.io/KAYLEBOT/#fun)', inline=True)
  em.add_field(name='***KAYLE AI***', value=f'[AI](https://ericchen-01.github.io/KAYLEBOT/#KAYLEAI)', inline=True)
  em.add_field(name='***Details***', value='[DETAILS](https://ericchen-01.github.io/KAYLEBOT/#details)', inline=True)
  em.add_field(name='***Moderation***', value='[MODERATION](https://ericchen-01.github.io/KAYLEBOT/#moderation)', inline=True)

  em.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar_url}')
  em.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.author.guild.icon_url}")
  em.timestamp = datetime.datetime.utcnow()
  await ctx.send(embed=em)


client.loop.create_task(change_stat())
client.run(os.getenv("TOKEN"))
