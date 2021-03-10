from discord.ext import commands
from errorembed import ErrorEmbed
from successembed import SuccessEmbed
import subprocess
import discord
import datetime
from utilities.utility import Pag
import time
import random

class Utils(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  # Bash commands
  @commands.command(aliases = ['bash', 'console'])
  async def os(self, ctx, show_complete_output="false", *bash_command):
    """Runs a bash command directly in the project console and returns the full output if the user states 'true' for the first argument. Also, if the user states true, the successful execution embed is deleted and overridden by the command output pager. If the user states anything else, the successful execution embed is NOT deleted, but the full output of the command is **NOT** shown."""
    if ctx.author.guild_permissions.administrator and ctx.author.id == 642550830074953758:
      try:
        embed = discord.Embed(
          title = "Executing...",
          color = 0x5f10a3,
          timestamp = datetime.datetime.utcnow()
        )
        first_msg = await ctx.send(embed=embed)
        command = ""
        for i in range(len(bash_command)):
          command += f"{bash_command[i]} "
        command = command[:-1]
        subprocess.run(bash_command, check = True)
        embed = SuccessEmbed.success("Successful Command Execution", f"Your Bash command (`{command}`) worked!")
        await first_msg.delete()
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✔️")
        if show_complete_output.lower() == "true":
          await msg.delete()
          output = subprocess.getoutput(command)
          pager = Pag(
            title = "Bash Command Output",
            timeout = 1000,
            entries = [output[i: i + 1000] for i in range(0, len(output), 1000)],
            length=1,
            color = 0x5f10a3
          )
          await pager.start(ctx)
        else:
          pass

      except:
        await first_msg.delete()
        command = ""
        for i in range(len(bash_command)):
          command += f"{bash_command[i]} "
        command = command[:-1]
        embed = ErrorEmbed.error("Bash Command Error", f"Please try again.  That command (`{command}`) didn't work.")
        await ctx.send(embed=embed)
    
    else:
      embed = ErrorEmbed.error("Permission Error", "You are not the bot developer, and you don't have the permission of **Administrator**.")
      await ctx.send(embed=embed)

  # Work on change presence command and put here

  # End of Change presence

  @commands.command(aliases = ['purge', 'deletemessages', 'delmessages', 'remove'])
  async def clear(self, ctx, messages=1):
    """A utility command for people with the permission of **Manage Messages** associated with their role.  Default message remove count is 1 message."""
    if ctx.author.guild_permissions.manage_messages:
      await ctx.message.delete()
      await ctx.channel.purge(limit=messages)
      embed = SuccessEmbed.success("Success!", f"{messages} messages removed from {ctx.channel.mention}.")
      await ctx.send(embed=embed)

    else:
      embed = ErrorEmbed.error("Missing Permissions", "You need the permission of **Manage Messages** to run that command.")
      await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Utils(client))
