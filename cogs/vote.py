import discord
from discord.ext import commands
import datetime

class Vote(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def vote(self, ctx):
    """Get the vote links for the bot."""
    embed = discord.Embed(
      title = "**Ultimate Embed Bot** vote links",
      description = "Thank you for voting! It helps the publicity of the bot a lot and lets more people know about it!",
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )
    embed.add_field(name="Top.gg", value = "https://top.gg/bot/811395374798340116/vote", inline=False)
    embed.add_field(name="botsfordiscord.com", value = "https://botsfordiscord.com/bot/811395374798340116/vote", inline=False)
    embed.add_field(name="discordbotlist.com", value="https://discordbotlist.com/bots/ultimate-embed-bot/upvote", inline=False)

    await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Vote(client))