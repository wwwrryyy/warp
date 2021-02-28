import discord
from discord.ext import commands

class ErrorEmbed:
  def error(title, reason):
    embed = discord.Embed(
      title = title,
      description = reason,
      color = discord.Color.red()
    )
    embed.set_author(name = "Error")
    return embed