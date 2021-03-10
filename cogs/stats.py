import discord
from discord.ext import commands
import platform
import os
import datetime
import random

class ServerStats(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.footer_choices = ["Some nice jucy stats for you 😘", "Developed by minecraftpr03#6052"]

  @commands.command(description = "Gets the server stats and sends them as a neat embed.", aliases = ['server', 'serverstats', 'ss'])
  async def stats(self, ctx):
    """Gets the server/bot stats and sends them as a neat embed."""

    pyVer = platform.python_version()
    dpyVer = discord.__version__
    serverCount = len(self.client.guilds)
    memberCount = len(set(self.client.get_all_members()))
    name = ctx.guild.name
    description = str(ctx.guild.description)
    owner = str(ctx.guild.owner)
    serverId = str(ctx.guild.id)
    guildMemberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
      title = "Bot Stats",
      description = "Here are the bot stats, long with the stats for this server!",
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )
    embed.add_field(name = "◤✞ 𝕭𝖔𝖙 𝕾𝖙𝖆𝖙𝖘 ✞◥", value = f"Bot Owner/Developer: **minecraftpr03#6052**\n\nRunning Python version **{pyVer}**\n\nRunning discord.py version **{dpyVer}**\n\nMade with **~2350** lines of code\n\nIn **{serverCount}** server(s)\n\nWith **{memberCount}** members\n", inline = False)
    embed.add_field(name = "◤✞ 𝕾𝖊𝖗𝖛𝖊𝖗 𝕾𝖙𝖆𝖙𝖘 ✞◥", value = f"Server name: **{name}**\n\nServer description: **{description}**\n\nServer owner: **{owner}**\n\nServer ID: **{serverId}**\n\nServer Member Count: **{guildMemberCount}**")
    embed.set_thumbnail(url = icon)
    embed.set_footer(text = random.choice(self.footer_choices), icon_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlG4RyGiubWHYLKz5Y-oNQY5Sb99dDys_H4syzx9tWgbi9_1Nf:s3.amazonaws.com/pix.iemoji.com/images/emoji/apple/ios-12/256/face-blowing-a-kiss.png&usqp=CAU")
    embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("📊")

def setup(client):
  client.add_cog(ServerStats(client))