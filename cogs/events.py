import discord
from discord.ext import commands
import json

class Events(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    with open("prefixes.json", 'r') as f:
      prefixes = json.load(f)

    prefixes[str(guild.id)] = 'eb.'

    with open('prefixes.json', 'w') as f:
      json.dump(prefixes, f, indent=4)

  @commands.Cog.listener()
  async def on_guild_remove(self, guild):
    with open("prefixes.json", 'r') as f:
      prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
      json.dump(prefixes, f, indent=4)

def setup(client):
  client.add_cog(Events(client))