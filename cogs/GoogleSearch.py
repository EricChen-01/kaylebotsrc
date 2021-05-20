import discord
from discord.ext import commands
import os
from google_images_download import google_images_download 

response = google_images_downlaod.google_images_downlaod()

class GoogleSearch(commands.Cog):
  def __init__(self, client):
        self.client = client
  #commands
  @commands.command()
  async def googleImage(self, ctx, *message):
    downloadimages(query=message)
  
def setup(client):
  client.add_cog(GoogleSearch(client))

def downloadimages(query):
    arguments = {"keywords": query,
                 "format": "jpg",
                 "limit":1,
                 "print_urls":True,
                 "size": "medium",
                 "aspect_ratio":"panoramic"}
    try:
        response.download(arguments)
        print()

    except FileNotFoundError: 
        arguments = {"keywords": query,
                     "format": "jpg",
                     "limit":1,
                     "print_urls":True, 
                     "size": "medium"}

        try:
            response.download(arguments) 
        except:
            pass
