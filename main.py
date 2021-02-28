import discord
from discord.ext import commands
from server import bot_server
from errorembed import ErrorEmbed
from successembed import SuccessEmbed
from helpcmd import Helpcmd
import os
import asyncio
import json

# Get Server Prefix
def get_prefix(client, message):
  with open("prefixes.json", 'r') as f:
    prefixes = json.load(f)
  return prefixes[str(message.guild.id)]

# Define Client
client = commands.Bot(command_prefix = get_prefix)

# Loading/Unloading Cogs
@client.command()
async def load(ctx, extension):
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
          color = discord.Color.green()
        )
        embed.set_author(name = "Cog Manager")
        await ctx.send(embed=embed)
      else:
        client.load_extension(f"cogs.{extension}")
        embed = discord.Embed(
          title = " ✅ Load Cog",
          description = f"Successfully loaded extension {extension}",
          color = discord.Color.green()
        )
        embed.set_author(name = "Cog Manager")
        with open("cogstatus.json", 'r') as f:
          cog = json.load(f)
        cog[str(extension)] = "loaded"
        with open('cogstatus.json', 'w') as f:
          json.dump(cog, f, indent=4)
        await ctx.send(embed = embed)

    else:
      print(ctx.author.id)
      embed = ErrorEmbed.error("Permission Error", "You are not the bot developer, and you don't have the permission of **Administrator**.")
      await ctx.send(embed=embed)
  
  except:
    ErrorEmbed.error("Cog Load Error", "Either something is wrong with the cog code or the cog is already loaded.")

@client.command()
async def unload(ctx, extension):
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
          color = discord.Color.green()
        )
        embed.set_author(name = "Cog Manager")
        await ctx.send(embed=embed)

      else:
        client.unload_extension(f"cogs.{extension}")
        embed = discord.Embed(
          title = "✅ Unload Cog",
          description = f"Successfully unloaded extension {extension}",
          color = discord.Color.green()
        )
        embed.set_author(name = "Cog Manager")
        with open("cogstatus.json", 'r') as f:
          cog = json.load(f)
        cog[str(extension)] = "unloaded"
        with open('cogstatus.json', 'w') as f:
          json.dump(cog, f, indent=4)
        await ctx.send(embed = embed)
    
    else:
      embed = ErrorEmbed.error("Permission Error", "You are not the bot developer, and you don't have the permission of **Administrator**.")
      await ctx.send(embed=embed)

  except:
    ErrorEmbed.error("Cog Unload Error", "Either something is wrong with the cog code or the cog is already unloaded.")
  

@client.command()
async def reload(ctx, extension):
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
          color = discord.Color.green()
        )
        embed.set_author(name = "Cog Manager")
        await ctx.send(embed=embed)
    
      else:
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")
        embed = discord.Embed(
          title = "✅ Reload Cog",
          description = f"Successfully reloaded extension {extension}",
        color = discord.Color.green()
        )
        embed.set_author(name = "Cog Manager")
        with open("cogstatus.json", 'r') as f:
          cog = json.load(f)
        cog[str(extension)] = "loaded"
        with open('cogstatus.json', 'w') as f:
          json.dump(cog, f, indent=4)
        await ctx.send(embed = embed)
    
    else:
      embed = ErrorEmbed.error("Permission Error", "You are not the bot developer, and you don't have the permission of **Administrator**.")
      await ctx.send(embed=embed)

  except:
    ErrorEmbed.error("Cog Reload Error", "Either something is wrong with the cog code or the cog is already loaded/unloaded.")

#Load all cogs on startup
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')

bot_server()
client.run(os.getenv('TOKEN'))