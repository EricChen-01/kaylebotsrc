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
    @commands.cooldown(1,5, commands.BucketType.default)
    async def weather(self,ctx, city="New York City"):
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('WeatherAPI')}")
        currently = response.json()["weather"][0]["main"]
        description = response.json()["weather"][0]["description"]
        temperature = response.json()["main"]["temp"]
        fahrenheit = ((temperature - 273.15) * 9) / 5
        celsius = (fahrenheit - 32) * (5/9)
        await ctx.send(f'{city}: currently:{currently}\ndescription:{description}\nTemperature:{round(fahrenheit,2)}°F    {round(celsius,2)}°C    {round(temperature,2)}°K')
        
def setup(client):
  client.add_cog(Other(client))

