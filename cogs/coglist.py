import discord
from discord.ext import commands
import os
import json

class Coglist(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(aliases=['listcogs', 'lc','botcogs', 'coglist'])
  async def cogs(self, ctx):
    embed = discord.Embed(
      title = "Bot Cogs",
      color = discord.Color.green()
    )
    embed.set_author(name = "Cog Manager")
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py') or filename.endswith('.pyc'):
        with open("cogstatus.json", 'r') as f:
          cog = json.load(f)
        embed.add_field(name = f" - {filename[:-3]} -", value = f"Status: {cog[str(filename[:-3])]}")
    
    await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Coglist(client))