from discord.ext import commands
import discord
from successembed import SuccessEmbed
from errorembed import ErrorEmbed
import datetime
import random

class Counting(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.working = 1
    self.current_number = 0
    self.current_number_sender = None

  @commands.command(description = "Start a counting game in the channel the command was invoked in.", aliases = ['counting', 'startcounting', 'count'])
  async def cstart(self, ctx):
    """Start a counting game in the channel the command was invoked in."""
    self.working = 1
    self.current_number = 0
    self.current_number_sender = None
    start = discord.Embed(
      title = "Game start",
      description = "Rules: You can't send a number twice in a row.  The number you send must be exactly one higher than the prevoulsy sent number.  If you send anything other than a number it seems to break the game.  So only send numbers.  Good luck!",
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )
    await ctx.send(embed=start)

    def check(m):
      return m.author == ctx.author and m.channel == ctx.channel
    
    while self.working == 1:
        get_msg = await self.client.wait_for('message', timeout = None, check = check)
        try:
          msg = int(get_msg.content)

          if msg == self.current_number or msg < self.current_number or msg > self.current_number + 1:
            embed = discord.Embed(
              title = "Fail!",
              description = f"You entered the wrong number!  It should have been {self.current_number + 1}.  The game has ended at {self.current_number}.",
              color = discord.Color.red(),
              timestamp = datetime.datetime.utcnow()
            )
            await ctx.send(embed=embed)
            self.working = 0
        
          elif ctx.message.author == self.current_number_sender:
            embed = discord.Embed(
              title = "Fail!",
              description = f"You can't send a number twice in a row!  The game has ended at {self.current_number}.",
              color = discord.Color.red(),
              timestamp = datetime.datetime.utcnow()
            )
            await ctx.send(embed=embed)
            self.working=0
        
          else:
            await get_msg.add_reaction("✅")
            self.current_number += 1
            self.current_number_sender = ctx.author
            print(self.current_number)
            print(self.current_number_sender)
        except:
          return

        

def setup(client):
  client.add_cog(Counting(client))