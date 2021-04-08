import discord
from discord.ext import commands
from errorembed import ErrorEmbed
from successembed import SuccessEmbed
import datetime
from discord.ext.commands import cooldown, BucketType

numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟")

class Poll(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(description = "Send a quick poll to the specified channel.")
  @cooldown(1, 30, BucketType.user)
  async def poll(self, ctx, channel=None, question=None, *options):
    """Send a quick poll to the specified channel.  Question (the second argument) must be in double quotation marks. ("")"""
    if ctx.author.guild_permissions.manage_messages:
      if len(options) > 10:
        embed = ErrorEmbed.error("Too many arguments", "You can only have 10 options per poll.")
        await ctx.send(embed=embed)
        return
      else:
        try:
          c_id = int(channel[2:-1])
        except:
          embed = ErrorEmbed.error("Invalid Embed Value(s)", f"You didn't mention a channel properly! Do it like this {ctx.channel.mention} next time.")
          await ctx.send(embed=embed)
          return
        chnl = self.client.get_channel(c_id)
        embed = discord.Embed(
          title = "Poll",
          description = f" - **{question}** -",
          color = 0x5f10a3,
          timestamp = datetime.datetime.utcnow()
        )
        embed.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)
        embed.set_author(name = "Poll")

        fields = [("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False), ("\n - **Instructions** -", "React to cast a vote!", False)]

        for name, value, inline in fields:
          embed.add_field(name=name, value=value, inline=inline)
        try:
          add_reactions_to = await chnl.send(embed=embed)
        except:
          embed = ErrorEmbed.error("Something went wrong", "Please make sure that you are mentioning a channel correctly, and that you are specifying no more than 10 options for the poll.")
          await ctx.send(embed=embed)
          return
        
        for emoji in numbers[:len(options)]:
          await add_reactions_to.add_reaction(emoji)

        success = SuccessEmbed.success(desc = f"Poll successfully sent to {chnl.mention}!")
        msg = await ctx.send(embed=success)
        await msg.add_reaction("📊")

    else:
      embed = ErrorEmbed.error(
        "Missing Permissions",
        "To avoid spam in servers, only people with the permission of Manage Messages can use this command."
      )
      await ctx.send(embed=embed)

  @commands.command(aliases = ['suggestion', 'question', 'q'])
  @cooldown(1, 30, BucketType.user)
  async def suggest(self, ctx, channel=None, *, suggestion=None):
    """Similar to a poll, but there are no options and is just an idea.  Only "yes" or "no" for choices."""
    if ctx.author.guild_permissions.manage_messages:
      if channel== None:
        embed = ErrorEmbed.error("Missing Command Arguments", "You must specify a channel to send the suggestion to and the suggestion itself.")
        await ctx.send(embed=embed)

      else:
        try:
            c_id = int(channel[2:-1])
        except:
          embed = ErrorEmbed.error("Invalid Embed Value(s)", f"You didn't mention a channel properly! Do it like this {ctx.channel.mention} next time.")
          await ctx.send(embed=embed)
          return
        chnl = self.client.get_channel(c_id)
        embed = discord.Embed(
          title = "Suggestion",
          description = f" - **{suggestion}** -",
          color = 0x5f10a3,
          timestamp = datetime.datetime.utcnow()
        )
        embed.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)
        embed.set_author(name = "Suggestion")
        msg = await chnl.send(embed=embed)
        await msg.add_reaction("⬆️")
        await msg.add_reaction("⬇️")
        success = SuccessEmbed.success("Success!", f"Suggestion successfully sent to {chnl.mention}")
        msg = await ctx.send(embed=success)
        await msg.add_reaction("📊")

    else:
      embed = ErrorEmbed.error(
        "Missing Permissions",
        "To avoid spam in servers, only people with the permission of Manage Messages can use this command."
      )
      await ctx.send(embed=embed)


def setup(client):
  client.add_cog(Poll(client))

