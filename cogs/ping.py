import discord
from discord.ext import commands
import datetime
import random

class Ping(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(description = "Get the bot's ping/latency")
  async def ping(self, ctx):
    """Returns the bot's ping."""
    embed = discord.Embed(
      title = "Pong!",
      description =  f"Bot ping: {round(self.client.latency * 1000)}ms",
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🟢")

def setup(client):
  client.add_cog(Ping(client))
