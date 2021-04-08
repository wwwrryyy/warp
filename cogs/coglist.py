import discord
from discord.ext import commands
import os
import json
import datetime

class Coglist(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(description = "Get the list of the bot's cogs.", aliases=['listcogs', 'lc','botcogs', 'coglist', 'extensions'])
  async def cogs(self, ctx):
    """Lists the bot's cogs."""
    embed = discord.Embed(
      title = "Bot Cogs",
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )
    embed.set_author(name = "Cog Manager")
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py') or filename.endswith('.pyc'):
        with open("cogstatus.json", 'r') as f:
          cog = json.load(f)
        embed.add_field(name = f" - {filename[:-3]} -", value = f"Status: {cog[str(filename[:-3])]}")
    embed.add_field(name=f"**Real** Extension Names (for use in the *help* command, ex. {ctx.prefix}help Colorcalc)", value = "***Coglist***, ***Colorcalc***, ***Colorlist***, ***CooldownCommands***, ***Embed***, ***Events***, ***Fun***, ***Help***, ***Image***, ***Invite***, ***Logout***, ***Minecraft***, ***OnThisDay***, ***Poll***, ***Stats***, ***Tools***, ***Vote***", inline=False)
    
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("⚙️")

def setup(client):
  client.add_cog(Coglist(client))