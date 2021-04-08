from discord.ext import commands
from successembed import SuccessEmbed
from errorembed import ErrorEmbed
import os

class Logout(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(description = "Logs the bot out.", aliases = ['quit'],hidden = True)
  async def logout(self, ctx):
    """An emergency reset command ONLY for the Bot Dev.  Completely logs out the bot and disconnects it from Discord."""
    if ctx.author.guild_permissions.administrator and ctx.author.id == 642550830074953758:
      embed = SuccessEmbed.success("Success", "Bot logged out!  You will have to restart the client to make the bot get back online.")
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("🛑")
      await self.client.logout()

    else:
      embed = ErrorEmbed.error("Missing Permissions", "You are **NOT** an Administrator of your current server and are **NOT** the Bot Developer!  You can't run this command.")
      await ctx.send(embed=embed)

  @commands.command(alises = ['restart'])
  async def relog(self, ctx):
    """An emergency reset command ONLY for the Bot Dev.  Logs out the bot then logs it back in, providing a full restart."""
    if ctx.author.guild_permissions.administrator and ctx.author.id == 642550830074953758:
      embed = SuccessEmbed.success("Success", "Bot relogged!  It will automatically come back online.")
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("🛑")
      await self.client.logout()
      os.system("python main.py")

    else:
      embed = ErrorEmbed.error("Missing Permissions", "You are **NOT** an Administrator of your current server and are **NOT** the Bot Developer!  You can't run this command.")
      await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Logout(client))