import discord
from discord.ext import commands, tasks
from server import bot_server
from errorembed import ErrorEmbed
from successembed import SuccessEmbed
from helpcmd import Helpcmd
import os
import asyncio
import json
from utilities.utility import clean_code
import contextlib
import io
import textwrap
from traceback import format_exception
from utilities.utility import Pag
import datetime
import random

os.system("pip install buttons")

# Get Server Prefix
def get_prefix(client, message):
  with open("prefixes.json", 'r') as f:
    prefixes = json.load(f)
  return prefixes[str(message.guild.id)]

# Define Client
client = commands.Bot(command_prefix = get_prefix, intents = discord.Intents.all())

@tasks.loop(seconds=60)
async def re_install_buttons():
  os.system("pip install buttons")

@client.remove_command("help")

@client.command(hidden=True)
async def specialchar(ctx):
  await ctx.send("`")

@client.command(hidden=True)
async def evaltemplate(ctx):
  await ctx.send("eb.eval ```python\n\n```")

@client.command(name="eval", aliases=["exec", "e", "evaluate", "execute"])
async def _eval(ctx, *, code):
  """A dev-only command to execute Python code using Discord messages."""
  if ctx.author.guild_permissions.administrator and ctx.author.id == 642550830074953758:
    code = clean_code(code)
    
    local_variables = {
      "discord": discord,
      "commands": commands,
      "client": client,
      "ctx": ctx,
      "channel": ctx.channel,
      "author": ctx.author,
      "guild": ctx.guild,
      "message": ctx.message 
    }

    stdout = io.StringIO()

    try:
      with contextlib.redirect_stdout(stdout):
        exec(
          f"async def func():\n{textwrap.indent(code, '    ')}", local_variables
        )

        obj = await local_variables["func"]()

        result = f"{stdout.getvalue()}\n-- {obj}\n"

    except Exception as e:
      result = "".join(format_exception(e, e, e.__traceback__))

    pager = Pag(
      timeout = 100,
      entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
      length=1,
      prefix = "```py",
      suffix = "```"
    )

    await pager.start(ctx)
    

  else:
    embed = ErrorEmbed.error("Permission Error", "You are not the bot developer, and you don't have the permission of **Administrator**.")
    await ctx.send(embed=embed)

# Loading/Unloading Cogs
@client.command(description = "Load an extension. (Bot dev only)")
async def load(ctx, extension):
  """Loads an extension. (Dev-only)"""
  try:
    if ctx.author.guild_permissions.administrator and ctx.author.id == 642550830074953758:
      if extension.lower() == "all":
        for filename in os.listdir('./cogs'):
          if filename.endswith('.py') or filename.endswith('.pyc'):
            client.load_extension(f'cogs.{filename[:-3]}')
            with open("cogstatus.json", 'r') as f:
              cog = json.load(f)
              cog[str(filename[:-3])] = "loaded"
            with open('cogstatus.json', 'w') as f:
              json.dump(cog, f, indent=4)
        embed = discord.Embed(
          title = "✅ Load Cog",
          description = "Successfully loaded all extensions",
          color = 0x5f10a3,
          timestamp = datetime.datetime.utcnow()
        )
        embed.set_author(name = "Cog Manager")
        msg = await ctx.send(embed = embed)
        await msg.add_reaction("⚙️")
      else:
        client.load_extension(f"cogs.{extension}")
        embed = discord.Embed(
          title = " ✅ Load Cog",
          description = f"Successfully loaded extension {extension}",
          color = 0x5f10a3,
          timestamp = datetime.datetime.utcnow()
        )
        embed.set_author(name = "Cog Manager")
        with open("cogstatus.json", 'r') as f:
          cog = json.load(f)
        cog[str(extension)] = "loaded"
        with open('cogstatus.json', 'w') as f:
          json.dump(cog, f, indent=4)
        msg = await ctx.send(embed = embed)
        await msg.add_reaction("⚙️")

    else:
      print(ctx.author.id)
      embed = ErrorEmbed.error("Permission Error", "You are not the bot developer, and you don't have the permission of **Administrator**.")
      await ctx.send(embed=embed)
  
  except:
    ErrorEmbed.error("Cog Load Error", "Either something is wrong with the cog code or the cog is already loaded.")

@client.command(description = "Unload an extension. (Bot dev only)")
async def unload(ctx, extension):
  """Unloads an extension. (Dev-only)"""
  try:
    if ctx.author.guild_permissions.administrator and ctx.author.id == 642550830074953758:
      if extension.lower() == "all":
        for filename in os.listdir('./cogs'):
          if filename.endswith('.py') or filename.endswith('.pyc'):
            client.unload_extension(f'cogs.{filename[:-3]}')
            with open("cogstatus.json", 'r') as f:
              cog = json.load(f)
              cog[str(filename[:-3])] = "unloaded"
            with open('cogstatus.json', 'w') as f:
              json.dump(cog, f, indent=4)
        embed = discord.Embed(
          title = "✅ Unload Cog",
          description = "Successfully unloaded all extensions",
          color = 0x5f10a3,
          timestamp = datetime.datetime.utcnow()
        )
        embed.set_author(name = "Cog Manager")
        msg = await ctx.send(embed = embed)
        await msg.add_reaction("⚙️")

      else:
        client.unload_extension(f"cogs.{extension}")
        embed = discord.Embed(
          title = "✅ Unload Cog",
          description = f"Successfully unloaded extension {extension}",
          color = 0x5f10a3,
          timestamp = datetime.datetime.utcnow()
        )
        embed.set_author(name = "Cog Manager")
        with open("cogstatus.json", 'r') as f:
          cog = json.load(f)
        cog[str(extension)] = "unloaded"
        with open('cogstatus.json', 'w') as f:
          json.dump(cog, f, indent=4)
        msg = await ctx.send(embed = embed)
        await msg.add_reaction("⚙️")
    
    else:
      embed = ErrorEmbed.error("Permission Error", "You are not the bot developer, and you don't have the permission of **Administrator**.")
      await ctx.send(embed=embed)

  except:
    ErrorEmbed.error("Cog Unload Error", "Either something is wrong with the cog code or the cog is already unloaded.")
  

@client.command(description = "Reload an extension. (Bot dev only)")
async def reload(ctx, extension):
  """Reloads an extension. (Dev-only)"""
  try:
    if ctx.author.guild_permissions.administrator and ctx.author.id == 642550830074953758:
      if extension.lower() == "all":
        for filename in os.listdir('./cogs'):
          if filename.endswith('.py') or filename.endswith('.pyc'):
            client.unload_extension(f'cogs.{filename[:-3]}')
            client.load_extension(f'cogs.{filename[:-3]}')
            with open("cogstatus.json", 'r') as f:
              cog = json.load(f)
              cog[str(filename[:-3])] = "loaded"
            with open('cogstatus.json', 'w') as f:
              json.dump(cog, f, indent=4)
        embed = discord.Embed(
          title = "✅ Reload Cog",
          description = "Successfully reloaded all extensions",
          color = 0x5f10a3,
          timestamp = datetime.datetime.utcnow()
        )
        embed.set_author(name = "Cog Manager")
        msg = await ctx.send(embed = embed)
        await msg.add_reaction("⚙️")
    
      else:
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")
        embed = discord.Embed(
          title = "✅ Reload Cog",
          description = f"Successfully reloaded extension {extension}",
          color = 0x5f10a3,
          timestamp = datetime.datetime.utcnow()
        )
        embed.set_author(name = "Cog Manager")
        with open("cogstatus.json", 'r') as f:
          cog = json.load(f)
        cog[str(extension)] = "loaded"
        with open('cogstatus.json', 'w') as f:
          json.dump(cog, f, indent=4)
        msg = await ctx.send(embed = embed)
        await msg.add_reaction("⚙️")
    
    else:
      embed = ErrorEmbed.error("Permission Error", "You are not the bot developer, and you don't have the permission of **Administrator**.")
      await ctx.send(embed=embed)

  except:
    ErrorEmbed.error("Cog Reload Error", "Either something is wrong with the cog code or the cog is already loaded/unloaded.")

#Load all cogs on startup
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')
    with open("cogstatus.json", 'r') as f:
      cog = json.load(f)
      cog[str(filename[:-3])] = "loaded"
    with open('cogstatus.json', 'w') as f:
      json.dump(cog, f, indent=4)

bot_server()
client.run(os.getenv('TOKEN'))