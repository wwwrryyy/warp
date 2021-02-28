import discord
from discord.ext import commands

class SuccessEmbed:
  def success(title : str = "Success!", desc : str =  "Command executed successfully!"):
    embed = discord.Embed(
      title = title,
      description = desc,
      color = discord.Color.green()
    )
    embed.set_author(name = "Success")
    return embed