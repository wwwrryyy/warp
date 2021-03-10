import discord
import datetime

class Helpcmd:
  def embed(command, description, aliases,  permission, under_which_extension):
    embed = discord.Embed(
      title = f"`{command}` Command",
      description = description,
      color = discord.Color.green(),
      timestamp = datetime.datetime.utcnow()
    )
    embed.add_field(name = "Aliases", value = f" `{aliases}`")
    embed.set_author(name = f"Command type: `{permission}`")
    embed.set_footer(text = f"Under extension {under_which_extension}")
    return embed