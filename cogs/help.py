import discord
from discord.ext import commands
from helpcmd import Helpcmd
from errorembed import ErrorEmbed
from cogembed import CogEmbed

class Help(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.client.remove_command("help")

  @commands.command()
  async def help(self, ctx, command : str = None):
    if command == None:
      embed = discord.Embed(
        title = "Help",
        description = "Use <prefix>help <command> for extended information on a command.",
        color = discord.Color.green()
      )
      embed.add_field(name = "**General commands**", value = "cogs, colors, decimaltorgb, embed, help, ping, poll, rgbtodecimal")
      embed.add_field(name = "**Admin-only commands**", value = "prefix")
      embed.add_field(name = "**Bot Dev-only commands**", value = "load, reload, unload")
      embed.set_footer(text = "Help :^)")
      await ctx.send(embed=embed)

    elif command.lower() == "cogs":
      embed = Helpcmd.embed("cogs", "Lists the bot's cogs and whether they are loaded or unloaded.", "listcogs, lc, botcogs", "general", "main (not an extension)")
      await ctx.send(embed=embed)

    elif command.lower() == "colors":
      embed = Helpcmd.embed("colors", "Shows the color names and the decimal values for those colors.  Helpful for deciding what color you want to make your embed. Specify a page number after **colors** to see another page of color options.", "none", "general", "colorlist")
      await ctx.send(embed=embed)
    
    elif command.lower() == "decimaltorgb":
      embed = Helpcmd.embed("decimaltorgb", "A color conversion calculator for your decimal color value into RGB format. Very useful because the embed command takes in the three RGB components (red, green and blue) (separated) when asking for a color.", "dec2rgb, dectrgb, d2rgb", "general", "colorcalc")
      await ctx.send(embed=embed)

    elif command.lower() == "embed":
      embed = Helpcmd.embed("embed", "The main command for making and sending an embed to the channel of your choice.", "none", "general", "main (not an extension)")
      await ctx.send(embed=embed)

    elif command.lower() == "ping":
      embed = Helpcmd.embed("ping", "Returns the client's latency.", "none", "general", "ping")
      await ctx.send(embed=embed)

    elif command.lower() == "rgbtodecimal":
      embed = Helpcmd.embed("rgbtodecimal", "A color conversion calculator for your RGB color value into decimal format. The opposite of the **decimaltorgb** command.", "rgbtdec, rgb2dec,rgb2d", "general", "colorcalc")
      await ctx.send(embed=embed)

    elif command.lower() == "load":
      embed = Helpcmd.embed("load", "Loads the specified extension. **ONLY FOR BOT DEV**", "none", "**Dev-only**", "main (not an extension)")
      await ctx.send(embed=embed)

    elif command.lower() == "prefix":
      embed = Helpcmd.embed("prefix", "Change server prefix.", "none", "**Admin-only**", "main (not an extension)")
      await ctx.send(embed=embed)

    elif command.lower() == "reload":
      embed = Helpcmd.embed("reload", "Reloads the specified extension. **ONLY FOR BOT DEV**", "none", "**Dev-only**", "main (not an extension)")
      await ctx.send(embed=embed)

    elif command.lower() == "unload":
      embed = Helpcmd.embed("unload", "Reloads the specified extension. **ONLY FOR BOT DEV**", "none", "**Dev-only**", "main (not an extension)")
      await ctx.send(embed=embed)

    elif command.lower() == "poll":
      embed = Helpcmd.embed("poll", "Send a poll to a channel of your choice.", "none", "general", "poll")
      await ctx.send(embed=embed)
    
    elif command.lower() == "coglist":
      embed = CogEmbed.embed(command, "cogs")
      await ctx.send(embed=embed)

    elif command.lower() == "colorcalc":
      embed = CogEmbed.embed(command, "decimaltorgb, rgbtodecimal")
      await ctx.send(embed=embed)

    elif command.lower() == "colorlist":
      embed = CogEmbed.embed(command, "colors")
      await ctx.send(embed=embed)
    
    elif command.lower() == "embed":
      embed = CogEmbed.embed(command, "embed")
      await ctx.send(embed=embed)

    elif command.lower() == "events":
      embed = CogEmbed.embed(command, "No commands.  This is just a cog for client events.")
      await ctx.send(embed=embed)

    elif command.lower() == "help":
      embed = CogEmbed.embed(command, "help")
      await ctx.send(embed=embed)

    elif command.lower() == "ping":
      embed = CogEmbed.embed(command, "ping")
      await ctx.send(embed=embed)

    elif command.lower() == "poll":
      embed = CogEmbed.embed(command, "poll")
      await ctx.send(embed=embed)

    elif command.lower() == "prefix":
      embed = CogEmbed.embed(command, "prefix")
      await ctx.send(embed=embed)
    
    else:
      embed = ErrorEmbed.error("Invalid Command", "The command you provided didn't exist.  Make sure you are not using aliases.")
      await ctx.send(embed=embed)

def setup(client):
  client.add_cog(Help(client))