from discord.ext import commands
from errorembed import ErrorEmbed
from successembed import SuccessEmbed
import json
from discord.ext.commands import cooldown, BucketType
import discord
import datetime

class CooldownCommands(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  # Change Prefix
  @commands.command(description = "Change the bot's prefix for a server (Only for administrators)  Cooldown: 15 seconds")
  @cooldown(1, 15, BucketType.user)
  async def prefix(self, ctx, prefix = None):
    """Change the bot's prefix for a server (Only for server admins)"""
    if prefix == None:
      embed = discord.Embed(
        title = f"My prefix in {ctx.guild}",
        description = ctx.prefix,
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      await ctx.send(embed=embed)
    else:
      if ctx.author.guild_permissions.administrator:
        with open("prefixes.json", 'r') as f:
          prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:
          json.dump(prefixes, f, indent=4)

        embed = SuccessEmbed.success("Successful Prefix Change!", f"New server prefix set as **{prefix}**!")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✔️")
      else:
        embed = ErrorEmbed.error("Permission Error", "You do not have the permission of **Administrator** to run this command.")
        await ctx.send(embed=embed)

  # Feedback
  @commands.command(description = "Send feedback to the bot devs!")
  @cooldown(1, 30, BucketType.user)
  async def feedback(self, ctx, anonymous = "true", *, message):
    """Send feedback to the bot dev(s).  Cooldown: 30 seconds"""
    if anonymous.lower() == 'true':
      username = "anonymously sent"
    elif anonymous.lower() == "false":
      username = ctx.author
    elif anonymous or message == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You must provide whether you want to send the feedback anonymously (true/false), and the message you want to send!")
      await ctx.send(embed=embed)
      return
      
    with open("feedback.txt", "a") as f:
      f.write(f"Username: {username}  --  Message: {message}\n")
      f.close()
    embed = SuccessEmbed.success("Feedback sent!", "Thank you for your feedback!")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("✔️")

def setup(client):
  client.add_cog(CooldownCommands(client))