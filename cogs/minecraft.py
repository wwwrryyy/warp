import discord
from discord.ext import commands
import json
import urllib.request
from errorembed import ErrorEmbed

class Minecraft(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(aliases=['server', 'mcserver'])
  async def minecraftserver(self, ctx, serverName=None):
    """Get the stats of a Minehut server."""
    if serverName == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You must provide a Minehut server name to check!")
      await ctx.send(embed=embed)
    else:
      url = f"https://api.minehut.com/server/{serverName}?byName=true"
      try:
        data = urllib.request.urlopen(url).read().decode()
      except:
        embed = ErrorEmbed.error("Server Info Fetch Error", "Either that server doesn't exist, or the server is private.  Also, the API could be down at the moment.  Please try again later.")
        await ctx.send(embed=embed)
        return
      obj = json.loads(data)
      description = obj["server"]["motd"]
      online = obj["server"]["online"]
      players = obj["server"]["playerCount"]

      embed = discord.Embed(
        title = f"Statistics for the Minehut Server {serverName}",
        color = discord.Color.green()
      )
      embed.add_field(name = "Description", value = description)
      embed.add_field(name = "Online", value = online)
      embed.add_field(name = "Players", value = players)

      await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Minecraft(client))