import discord
from discord.ext import commands
import asyncio
from errorembed import ErrorEmbed
from successembed import SuccessEmbed
from discord.ext.commands import cooldown, BucketType
import datetime

def get_discord_color(string):
      if string.lower() == "aqua" or "teal":
        color = discord.Color.teal()
      if string.lower() == "green":
        color = discord.Color.green()
      if string.lower() == "blue":
        color = discord.Color.blue()
      if string.lower() == "purple":
        color = discord.Color.purple()
      if string.lower() == "gold":
        color = discord.Color.gold()
      if string.lower() == "orange":
        color = discord.Color.orange()
      if string.lower() == "red":
        color = discord.Color.red()
      if string.lower() == "gray" or "grey":
        color = discord.Color.gray()
      if string.lower() == "darker_gray" or "darker_grey":
        color = discord.Color.darker_gray()
      if string.lower() == "navy":
        color = discord.Color.navy()
      if string.lower() == "dark_aqua" or "dark_teal":
        color = discord.Color.dark_teal()
      if string.lower() == "dark_green":
        color = discord.Color.dark_green()
      if string.lower() == "dark_blue":
        color = discord.Color.dark_blue()
      if string.lower() == "dark_purple":
        color = discord.Color.dark_purple()
      if string.lower() == "dark_gold":
        color = discord.Color.dark_gold()
      if string.lower() == "dark_orange":
        color = discord.Color.dark_orange()
      if string.lower() == "dark_red":
        color = discord.Color.dark_red()
      if string.lower() == "dark_gray" or "dark_grey":
        color = discord.Color.dark_gray()
      if string.lower() == "light_gray" or "light_grey":
        color = discord.Color.light_gray()
      if string.lower() == "dark_navy":
        color = 128
      if string.lower() == "luminous_vivid_pink":
        color = discord.Color.magenta()
      if string.lower() == "dark_vivid_pink":
        color = discord.Color.dark_magenta()

      return color

class Embed(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(description = "The embed command, where you make your own embed, and then send it to the channel of your choice!")
  @cooldown(1, 15, BucketType.user)
  async def embed(self, ctx):
    """The embed command, where you make your own embed, and then send it to the channel of your choice!  Cooldown: 15 seconds"""
    await ctx.send("Let's make this embed! Answer the questions within 60 seconds.")

    questions = ["What channel should the embed be sent to?",
    "Embed title?",
    "Embed description?",
    "Embed color? (Send in RGB format. If any (red, green, or blue) values are not 3 digit numbers, replace the missing digits with a 0. Example: 50, 255, 14 should be sent as 050255014). Please don't send any text inputs, because it will break the command.",
    "How many fields do you want in your embed?",
    "Embed thumbnail? (Link to image)",
    "Embed footer icon? (Link)",
    "Embed footer text?"]

    answers = []
    fieldtitles = []
    fieldvalues = []
    fieldinline = []

    def check(m):
      return m.author == ctx.author and m.channel == ctx.channel

    for i in questions:
      await ctx.send(i)

      try:
        msg = await self.client.wait_for('message', timeout = 60.0, check = check)
      except asyncio.TimeoutError:
        embed = ErrorEmbed.error("Timeout Error", "You didn\'t answer in time, please be quicker next time!")
        await ctx.send(embed=embed)
        return
      else:
        answers.append(msg.content)

    try:
      c_id = int(answers[0][2:-1])
    except:
      embed = ErrorEmbed.error("Invalid Embed Value(s)", f"You didn't mention a channel properly! Do it like this {ctx.channel.mention} next time.")
      await ctx.send(embed=embed)
      return
    
    channel = self.client.get_channel(c_id)

    thing = answers[3]

    try:
      r = int(thing[:3])
      g = int(thing[3:6])
      b = int(thing[6:9])
      color = int((r * 256 * 256) + (g * 256) + b)
    except:
      embed = ErrorEmbed.error("Invalid Embed Value(s)", "Invalid color.")
      await ctx.send(embed=embed)
      return

    try:
      embed = discord.Embed(
        title = answers[1],
        description = answers[2],
        color = color,
        timestamp = datetime.datetime.utcnow()
      )
    except:
      embed = ErrorEmbed.error("Invalid Embed Value(s)", "Embed setup canceled. Next time, please make sure all of your embed details are entered correctly.")
      await ctx.send(embed=embed)
      return
    if answers[5].lower() == "none":
      pass
    elif answers[6].lower() == "none" and answers[7] != "none":
      pass
    elif answers[6].lower() == "none":
      embed.set_footer(text = answers[7])
    elif answers[7].lower() == "none":
      embed.set_footer(icon_url = answers[6])
    else:
      embed.set_thumbnail(url = answers[5])
      embed.set_footer(icon_url = answers[6], text = answers[7])

    for field in range(int(answers[4])):
      await ctx.send(f"Field {field + 1} title?")
      try:
        msg = await self.client.wait_for('message', timeout = 60.0, check = check)
      except asyncio.TimeoutError:
        embed = ErrorEmbed.error("Timeout Error", "You didn\'t answer in time, please be quicker next time!")
        await ctx.send(embed=embed)
        return
      else:
        fieldtitles.append(msg.content)

      await ctx.send(f"Field {field + 1} value/text?")
      try:
        msg = await self.client.wait_for('message', timeout = 60.0, check = check)
      except asyncio.TimeoutError:
        embed = ErrorEmbed.error("Timeout Error", "You didn\'t answer in time, please be quicker next time!")
        await ctx.send(embed=embed)
        return
      else:
        fieldvalues.append(msg.content)

      await ctx.send(f"Do you want field {field + 1} to be inline? (Answer with True or False, case sensitive)?")
      try:
        msg = await self.client.wait_for('message', timeout = 60.0, check = check)
      except asyncio.TimeoutError:
        embed = ErrorEmbed.error("Timeout Error", "You didn\'t answer in time, please be quicker next time!")
        await ctx.send(embed=embed)
        return
      else:
        fieldinline.append(msg.content)

      embed.add_field(name = fieldtitles[field], value = fieldvalues[field], inline = fieldinline[field])
      
      field += 1

    channel = self.client.get_channel(c_id)
    # answers[8], answers[9], and answers[10] are for the author.  Author is currently WIP.
    try:
      await channel.send(embed=embed)
      embed = SuccessEmbed.success("Success!", f"Your embed was sent to {channel.mention}")
      add_react = await ctx.send(embed=embed)
      await add_react.add_reaction("👍")
    except:
      embed = ErrorEmbed.error("Invalid Command Arguments", "Please try again and make sure that you are entering in valid arguments to create the embed.")
      await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Embed(client))