import discord
from discord.ext import commands
from errorembed import ErrorEmbed
from successembed import SuccessEmbed

class Poll(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command()
  async def poll(self, ctx, channel = None, *, message = None):
    try:
      if channel or message == None:
        embed = ErrorEmbed.error("Missing Command Arguments", "Please check to make sure you are specifying a channel to send the poll to and the poll message.")
        await ctx.send(embed=embed)
      else:
        pfp = ctx.author.avatar_url
        c_id = int(channel[2:-1])
        chnl = self.client.get_channel(c_id)

        embed=discord.Embed(title="⏳NEW POLL!", description=f"{message}")
        embed.set_thumbnail(url=pfp)
        embed.set_footer(text="This poll was sent by {}".format(ctx.author.display_name))
        msg = await chnl.send(embed=embed)

        await msg.add_reaction('✅')
        await msg.add_reaction('🤷‍♂️')
        await msg.add_reaction('❎')
        embed = SuccessEmbed.success("Success!", f"Embed sent to {channel}")
    except:
      embed = ErrorEmbed.error("Missing Command Arguments", "Please check to make sure you are specifying a channel to send the poll to and the poll message.")
      await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Poll(client))