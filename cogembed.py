from discord.ext import commands
import discord
import datetime

class CogEmbed:
  def embed(extension, cmds):
    embed = discord.Embed(
      title = f"Commands from extension `{extension}`",
      description = f"`{commands}`",
      color = discord.Color.green(),
      timestamp = datetime.datetime.utcnow()
    )
    return embed