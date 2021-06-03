import aiohttp
import asyncio
import os
import discord
import requests
import datetime
from discord.ext import commands



class Other(commands.Cog):
    def __init__(self, client):
        self.client = client
    #commands
    @commands.command()
    @commands.cooldown(50000,86400, commands.BucketType.default)
    async def weather(self,ctx, *,city="New York City"):
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('WeatherAPI')}")
        currently = response.json()["weather"][0]["main"]
        description = response.json()["weather"][0]["description"]
        temperature = response.json()["main"]["temp"]
        fahrenheit = (((temperature - 273.15) * 9) / 5) + 32
        celsius = (fahrenheit - 32) * (5/9)
        weatherIcon = response.json()['weather'][0]['icon']
        
        embed = discord.Embed(title=f"***Weather Report: {city}***",color=0x14749F)
        embed.add_field(name='***Currently***', value=f'{currently}', inline=True)
        embed.add_field(name='***Description***', value=f'{description}', inline=True)
        embed.add_field(name='***Temperature***', value=f'{round(fahrenheit,2)}°F \n{round(celsius,2)}°C \n{round(temperature,2)}°K', inline=True)

        embed.set_thumbnail(url=f'http://openweathermap.org/img/wn/{weatherIcon}@2x.png')
        embed.set_author(name=f'{ctx.author.display_name}', icon_url=f'{ctx.author.avatar_url}')
        embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.author.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)
        
def setup(client):
  client.add_cog(Other(client))

