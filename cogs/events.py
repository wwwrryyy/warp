import discord
from discord.ext import commands, tasks
import json
from errorembed import ErrorEmbed
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown, CommandNotFound
import datetime
from discord.ext.commands.errors import MissingPermissions
import random
from __main__ import re_install_buttons
import time

# Get Server Prefix
def get_prefix(client, message):
  with open("prefixes.json", 'r') as f:
    prefixes = json.load(f)
  return prefixes[str(message.guild.id)]

class Events(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.cpu = ["pls my cpu", 'REEEEEEEEEEEEEEE', 'cool down pls', 'aaaaagh overloaded', "That command is currently on cooldown."]

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

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, CommandOnCooldown):
      def convert(seconds): 
        seconds = seconds % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d:%02d" % (hour, minutes, seconds)

      embed = ErrorEmbed.error("Command Cooldown Error", f"{random.choice(self.cpu)}\nPlease try again in **{convert(error.retry_after)}**.")
      await ctx.send(embed=embed)
    
    elif isinstance(error, CommandNotFound):
      embed = ErrorEmbed.error("Invalid Command", f"{ctx.author.mention} The command you just sent does not exist on this bot!")
      await ctx.author.send(embed=embed)
    
    else:
      raise error

  @commands.Cog.listener()
  async def on_ready(self):
    re_install_buttons.start()
    await self.client.change_presence(status=discord.Status.online, activity=discord.Game("eb.help for more info"))
    print(f"We have logged on as {self.client.user}")

def setup(client):
  client.add_cog(Events(client))