import discord
from discord.ext import commands
import datetime
import random

class Invite(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def invite(self, ctx):
    """Shows the invite link to the bot.  You can add me to as many servers as you want!"""
    embed = discord.Embed(
      title = "Invite me!",
      description = "You can invite me to as many servers as you want!  Click the link below.",
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )
    embed.add_field(name = "Invite Link", value = "https://discord.com/api/oauth2/authorize?client_id=811395374798340116&permissions=519399&scope=bot", inline=False)
    await ctx.send(embed=embed)
    try:
      await ctx.author.send(embed=embed)
    except:
      pass

def setup(client):
  client.add_cog(Invite(client))