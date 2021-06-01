import discord
import praw
import random
from discord.ext import commands

reddit = praw.Reddit(client_id="YUsBCobsTc-blg",
                      client_secret="xHnG9OpjQeQHgxFFsQ8D6j8EvJqp1A",
                      username="FunYoung6999",
                      password="ZQx*HJ%EWeyrsF4",
                      user_agent="praw")


class Meme(commands.Cog):
  def __init__(self, bot: commands.Bot):
        self.bot = bot
  #commands
  @commands.command(brief='<subreddit>')
  async def meme(self,ctx, subReddit = "meme"):
    subreddit= reddit.subreddit(subReddit)
    all_subs = []
    top = subreddit.top(limit = 100)
    for submission in top:
      all_subs.append(submission)
    random_sub = random.choice(all_subs)
    
    name = random_sub.title
    url = random_sub.url

    em = discord.Embed(title = name)
    em.set_image(url = url)
    await ctx.send(embed = em)
    await ctx.send(subreddit)

def setup(client):
  client.add_cog(Meme(client))