import datetime
import discord
from discord.ext import commands

class Colorcalc(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(description = "Convert an RGB color code to a decimal color code.", aliases = ['rgbtdec', 'rgb2dec','rgb2d'])
  async def rgbtodecimal(self, ctx, red : int = None, green : int = None, blue : int = None):
    """Convert an RGB color code to a decimal color code."""
    if red == None or green == None or blue == None:
      await ctx.send("You have to specify a value between 0 and 255 for each red, green and blue, in that order.")
    else:
      print(int((red*256*256)+(green*256)+blue))
      color = int(red*256*256)
      color += int(green*256)
      color += int(blue)
      embed = discord.Embed(
        title = "Color Conversion Calculator",
        description = f"Your color from RGB to decimal: {color}",
        color = color,
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("🟢")

  @commands.command(description = "Convert a decimal color code to an RGB color code.", aliases = ['dec2rgb', 'dectrgb', 'd2rgb'])
  async def decimaltorgb(self, ctx, c = None):
    """Convert a decimal color code into an RGB color code."""
    if c == None:
      await ctx.send("Please specify a decimal value no greater than 16777215 to convert into RGB.")
    else:
      b = int(c) % 256
      g_0 = (int(c) % 65536 - int(b))
      r_0 = int(c) - int(g_0) - int(b)
      g = int(g_0) / 256
      r = int(r_0) / 65536
      int(r)
      int(g)
      int(b)
      embed = discord.Embed(
        title = "Color Conversion Calculator",
        description = f"Your color from Decimal to RGB: {r}, {g}, {b}",
        color = int(c),
        timestamp = datetime.datetime.utcnow()
      )
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("🟢")

def setup(client):
  client.add_cog(Colorcalc(client))