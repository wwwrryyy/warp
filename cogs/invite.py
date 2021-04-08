import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import datetime
from errorembed import ErrorEmbed
from successembed import SuccessEmbed

class Invite(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def invite(self, ctx):
    """Shows the invite link to the bot.  You can add me to as many servers as you want!"""
    embed = discord.Embed(
      title = "Invite me!",
      description = "You can invite me to as many servers as you want!  Click the link below.",
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )
    embed.add_field(name = "Invite Link", value = "https://discord.com/api/oauth2/authorize?client_id=811395374798340116&permissions=519399&scope=bot", inline=False)
    await ctx.send(embed=embed)
    try:
      await ctx.author.send(embed=embed)
    except:
      pass

  @commands.command(aliases=['createinvite', 'ci', 'mi', 'generateinvite', 'gi'])
  @cooldown(1, 30, BucketType.user)
  async def makeinvite(self, ctx, channel = None, max_age=0, max_uses=0, temporary=False, *, reason=None):
    """Make an invite for the current channel (if none is specified).  Takes in max_age (int, days), max_uses (int), temporary membership (True/False), and a reason for creation.  Cooldown: 30 seconds"""
    if ctx.author.guild_permissions.create_instant_invite:
      try:
        if not channel:
          channel = ctx.channel.mention
        try:
          c_id = int(channel[2:-1])
        except:
          embed = ErrorEmbed.error("Invalid Embed Value(s)", f"You didn't mention a channel properly! Do it like this {ctx.channel.mention} next time.")
          await ctx.send(embed=embed)
          return
        chnl = self.client.get_channel(c_id)
        if not chnl:
          chnl = ctx.channel
        inv = await chnl.create_invite(max_age=max_age, max_uses=max_uses, temporary=temporary, reason=reason)
        embed = SuccessEmbed.success("Invite Creation Successful", f"Your invite was created!  Check it out here: {inv}")
        await ctx.send(embed=embed)
      except:
        embed = ErrorEmbed.error("Invite Creation Failed", "Please check to make sure your values are valid. (**max_age** and **max_uses** should be an int >= 0, **temporary** should be True or False, and **reason** should be a str.")
        await ctx.send(embed=embed)

    else:
      embed = ErrorEmbed.error("Missing Permissions", "You need the **Create Instant Invite** permission to run that command.")
      await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Invite(client))