from discord.ext import commands
from errorembed import ErrorEmbed
from successembed import SuccessEmbed
import json

class Prefix(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  # Change Prefix
  @commands.command()
  async def prefix(self, ctx, prefix):
    if ctx.author.guild_permissions.administrator:
      with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)

      prefixes[str(ctx.guild.id)] = prefix

      with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

      embed = SuccessEmbed.success("Successful Prefix Change!", f"New server prefix set as {prefix}!")
      await ctx.send(embed=embed)
    else:
      embed = ErrorEmbed.error("Permission Error", "You do not have the permission of **Administrator** to run this command.")
      await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Prefix(client))