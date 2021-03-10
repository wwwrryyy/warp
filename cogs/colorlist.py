from discord.ext import commands
import discord
from errorembed import ErrorEmbed
import datetime
import random

class Colorlist(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(description = "Get the list of colors that the bot can take in through an embed.")
  async def colors(self, ctx, page : int = None):
    """Get the list of colors that the bot can take in through an embed."""
    if page == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You didn't provide a valid  page number.  Provide a page number between 1 and 5.")
      await ctx.send(embed=embed)

    elif page == 1:
      embed = discord.Embed(
        title = "Built-in color names for Embeds",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      embed.add_field(name = "aqua", value =  "Decimal value: 1752220")
      embed.add_field(name = "green", value =   "Decimal value: 3066993")
      embed.add_field(name = "blue", value =  "Decimal value: 3447003")
      embed.add_field(name = "purple", value =  "Decimal value: 10181046")
      embed.add_field(name = "gold", value =  "Decimal value: 15844367")
      embed.set_footer(text = "Page 1/5")
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("🟢")

    elif page == 2:
      embed = discord.Embed(
        title = "Built-in color names for Embeds",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      embed.add_field(name = "orange", value =  "Decimal value: 15105570")
      embed.add_field(name = "red", value =   "Decimal value: 15158332")
      embed.add_field(name = "grey", value =  "Decimal value: 9807270")
      embed.add_field(name = "darker_grey", value   = "Decimal value: 8359053")
      embed.add_field(name = "navy", value =  "Decimal value: 3426654")
      embed.set_footer(text = "Page 2/5")
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("🟢")

    elif page == 3:
      embed = discord.Embed(
        title = "Built-in color names for Embeds",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      embed.add_field(name = "dark_aqua", value =   "Decimal value: 1146986")
      embed.add_field(name = "dark_green", value  = "Decimal value: 2067276")
      embed.add_field(name = "dark_blue", value =   "Decimal value: 2123412")
      embed.add_field(name = "dark_purple", value   = "Decimal value: 7419530")
      embed.add_field(name = "dark_gold", value =   "Decimal value: 12745742")
      embed.set_footer(text = "Page 3/5")
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("🟢")

    elif page == 4:
      embed = discord.Embed(
        title = "Built-in color names for Embeds",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      embed.add_field(name = "dark_orange", value   = "Decimal value: 11027200")
      embed.add_field(name = "dark_red", value =  "Decimal value: 10038562")
      embed.add_field(name = "dark_grey", value =   "Decimal value: 9936031")
      embed.add_field(name = "light_grey", value  = "Decimal value: 12370112")
      embed.add_field(name = "dark_navy", value =   "Decimal value: 2899536")
      embed.set_footer(text = "Page 4/5")
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("🟢")

    elif page == 5:
      embed = discord.Embed(
        title = "Built-in color names for Embeds",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      embed.add_field(name =  "luminous_vivid_pink", value = "Decimal  value: 16580705")
      embed.add_field(name = "dark_vivid_pink",   value = "Decimal value: 12320855")
      embed.set_footer(text = "Page 5/5")
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("🟢")

    elif page > 5:
      embed = ErrorEmbed.error("Command Invocation Error", "That page does not exist for the **colors** command.")
      await ctx.send(embed)

def setup(client):
  client.add_cog(Colorlist(client))