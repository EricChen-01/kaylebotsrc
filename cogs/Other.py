import aiohttp
import asyncio
import os
import discord
import requests
from discord.ext import commands



class Other(commands.Cog):
    def __init__(self, client):
        self.client = client
    #commands
    @commands.command()
    @commands.cooldown(1,3600, commands.BucketType.default)
    async def weather(self,ctx, *,city="New York City"):
        response = requests.get(f"api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('TOKEN')}")
        currently = response.json()["weather"]["main"]
        description = response.json()["weather"]["description"]
        temperature = response.json()["weather"]["temp"]
        fahrenheit = ((temperature - 273.15) * 9) / 5
        celsius = (fahrenheit - 32) * (5/9)
        await ctx.send(f'{city}: currently:{currently}\ndescription:{description}\nTemperature:{fahrenheit}°F    {celsius}°C    {temperature}°K')
        
def setup(client):
  client.add_cog(Other(client))

