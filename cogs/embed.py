import discord
from discord.ext import commands
import asyncio
from errorembed import ErrorEmbed
from successembed import SuccessEmbed

class Embed(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def embed(self, ctx):
    await ctx.send("Let's make this embed! Answer the questions within 60 seconds.")

    questions = ["What channel should the embed be sent to?",
    "Embed title?",
    "Embed description?",
    "Embed color? (Send in RGB format. If any (red, green, or blue) values are not 3 digit numbers, replace the missing digits with a 0. Example: 50, 255, 14 should be sent as 050255014)",
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
    await ctx.send(type(answers[3]))

    if type(answers[3]) == "int":
      r = int(answers[3][:3])
      g = int(answers[3][3:6])
      b = int(answers[3][6:9])
      color = int((r * 256 * 256) + (g * 256) + b)
    elif type(answers[3]) == "str":
      if answers[3].lower() == "aqua" or "teal":
        color = discord.Color.teal()
      if answers[3].lower() == "green":
        color = discord.Color.green()
      if answers[3].lower() == "blue":
        color = discord.Color.blue()
      if answers[3].lower() == "purple":
        color = discord.Color.purple()
      if answers[3].lower() == "gold":
        color = discord.Color.gold()
      if answers[3].lower() == "orange":
        color = discord.Color.orange()
      if answers[3].lower() == "red":
        color = discord.Color.red()
      if answers[3].lower() == "gray" or "grey":
        color = discord.Color.gray()
      if answers[3].lower() == "darker_gray" or "darker_grey":
        color = discord.Color.darker_gray()
      if answers[3].lower() == "navy":
        color = discord.Color.navy()
      if answers[3].lower() == "dark_aqua" or "dark_teal":
        color = discord.Color.dark_teal()
      if answers[3].lower() == "dark_green":
        color = discord.Color.dark_green()
      if answers[3].lower() == "dark_blue":
        color = discord.Color.dark_blue()
      if answers[3].lower() == "dark_purple":
        color = discord.Color.dark_purple()
      if answers[3].lower() == "dark_gold":
        color = discord.Color.dark_gold()
      if answers[3].lower() == "dark_orange":
        color = discord.Color.dark_orange()
      if answers[3].lower() == "dark_red":
        color = discord.Color.dark_red()
      if answers[3].lower() == "dark_gray" or "dark_grey":
        color = discord.Color.dark_gray()
      if answers[3].lower() == "light_gray" or "light_grey":
        color = discord.Color.light_gray()
      if answers[3].lower() == "dark_navy":
        color = 128
      if answers[3].lower() == "luminous_vivid_pink":
        color = discord.Color.magenta()
      if answers[3].lower() == "dark_vivid_pink":
        color = discord.Color.dark_magenta()
    else:
      embed = ErrorEmbed.error("Invalid Embed Value(s)", "Invalid color.")
      await ctx.send(embed=embed)
      return

    try:
      embed = discord.Embed(
        title = answers[1],
        description = answers[2],
        color = color
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
    await channel.send(embed=embed)
    embed = SuccessEmbed.success("Success!", f"Your embed was sent to {answers[0]}")
    await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Embed(client))