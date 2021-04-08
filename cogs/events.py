import discord
from discord.ext import commands
import json
from errorembed import ErrorEmbed
from discord.ext.commands import CommandOnCooldown
import datetime
import random
from __main__ import re_install_buttons

def get_day():
    from datetime import date

    today = date.today()

    day = today.strftime("%d/%m/%y")[:2]
    return day

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
  async def on_member_join(self, member):
    serverCount = len(self.client.guilds)
    memberCount = len(set(self.client.get_all_members()))
    await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"eb.help | {serverCount} servers | {memberCount} users"))

  @commands.Cog.listener()
  async def on_member_remove(self, member):
    serverCount = len(self.client.guilds)
    memberCount = len(set(self.client.get_all_members()))
    await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"eb.help | {serverCount} servers | {memberCount} users"))
  
  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    with open("prefixes.json", 'r') as f:
      prefixes = json.load(f)

    prefixes[str(guild.id)] = 'eb.'

    with open('prefixes.json', 'w') as f:
      json.dump(prefixes, f, indent=4)

    serverCount = len(self.client.guilds)
    memberCount = len(set(self.client.get_all_members()))
    await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"eb.help | {serverCount} servers | {memberCount} users"))

  @commands.Cog.listener()
  async def on_guild_remove(self, guild):
    
    with open("prefixes.json", 'r') as f:
      prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
      json.dump(prefixes, f, indent=4)

    serverCount = len(self.client.guilds)
    memberCount = len(set(self.client.get_all_members()))
    await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"eb.help | {serverCount} servers | {memberCount} users"))

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, CommandOnCooldown):
      def convert(seconds): 
        seconds = seconds % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d.%02d" % (hour, minutes, seconds)

      embed = ErrorEmbed.error("Command Cooldown Error", f"{random.choice(self.cpu)}\nPlease try again in **{convert(error.retry_after)}**.")
      await ctx.send(embed=embed)
    
    else:
      raise error

  @commands.Cog.listener()
  async def on_ready(self):
    re_install_buttons.start()
    serverCount = len(self.client.guilds)
    memberCount = len(set(self.client.get_all_members()))
    await self.client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"eb.help | {serverCount} servers | {memberCount} users"))
    print(f"We have logged on as {self.client.user}")

  @commands.Cog.listener()
  async def on_message(self, message):
    mention = f'<@!{self.client.user.id}>'
    with open("prefixes.json", 'r') as f:
      prefixes = json.load(f)
    gpf = prefixes[str(message.guild.id)]
    if mention in message.content:
      embed = discord.Embed(
        title = f"My prefix in {message.guild}",
        description = gpf,
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      embed.set_author(name="👋 Hello there! 👋")
      embed.set_footer(text = message.author, icon_url=message.author.avatar_url)
      await message.channel.send(embed=embed)

def setup(client):
  client.add_cog(Events(client))