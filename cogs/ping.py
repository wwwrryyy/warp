import discord
from discord.ext import commands

class Ping(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def ping(self, ctx):
      embed = discord.Embed(
        title = "Pong!",
        description =  f"Bot ping: {round(self.client.latency * 1000)}ms",
        color = discord.Color.green()
      )
      await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Ping(client))
