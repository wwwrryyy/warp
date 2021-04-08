from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.utils import get
from errorembed import ErrorEmbed
from discord import Embed
import discord
import json
from typing import Optional
import datetime
from discord.ext import commands
from utilities.utility import Pag

def get_prefix(ctx):
  with open("prefixes.json", 'r') as f:
    prefixes = json.load(f)
  return prefixes[str(ctx.guild.id)]

def syntax(command):
  cmd_and_aliases = "|".join([str(command), *command.aliases])
  params = []

  for key, value in command.params.items():
    if key not in ("self", "ctx"):
      params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

  params = " ".join(params)

  return f"```{cmd_and_aliases} {params}```"

class Help(Cog):
  def __init__(self, client):
    self.client = client
    self.client.remove_command("help")
    self.cmds_per_page = 6

  async def cmd_help(self, ctx, command):
      embed = Embed(
        title = f"Help with `{command}`",
        description = syntax(command),
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      embed.add_field(name="Command Description", value = command.help)
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("👀")

  async def return_filtered_commands(self, walkable, ctx):
    filtered = []

    for c in walkable.walk_commands():
      try:
        if c.hidden:
          continue

        elif c.parent:
          continue

        await c.can_run(ctx)
        filtered.append(c)
      except commands.CommandError:
        continue

    return self.return_sorted_commands(filtered)

  def return_sorted_commands(self, commandList):
    return sorted(commandList, key=lambda x: x.name)

  def get_command_signature(self, command: commands.Command, ctx: commands.Context):
    aliases = "|".join(command.aliases)
    cmd_invoke = f"[{command.name}|{aliases}]" if command.aliases else command.name

    full_invoke = command.qualified_name.replace(command.name, "")

    signature = f"{ctx.prefix}{full_invoke}{cmd_invoke} {command.signature}"

    return signature

  async def setup_help_pag(self, ctx, entity=None, title=None):
    entity = entity or self.client
    title = title or self.client.description

    pages = []

    if isinstance(entity, commands.Command):
      filtered_commands = (
        list(set(entity.all_commands.values()))
        if hasattr(entity, "all_commands")
        else []
      )
      filtered_commands.insert(0, entity)

    else:
      filtered_commands = await self.return_filtered_commands(entity, ctx)

    for i in range(0, len(filtered_commands), self.cmds_per_page):
      next_commands = filtered_commands[i : i + self.cmds_per_page]
      commands_entry = ""

      for cmd in next_commands:
        desc = cmd.short_doc or cmd.description
        signature = self.get_command_signature(cmd, ctx)
        subcommand = "Has subcommands" if hasattr(cmd, "all_commands") else ""

        commands_entry += (
          f"• **__{cmd.name}__**\n```\n{signature}\n```\n{desc}\n"
          if isinstance(entity, commands.Command)
          else f"• **__{cmd.name}__**\n{desc}\n    {subcommand}\n"
        )

      pages.append(commands_entry)

    await Pag(title = title, color = 0x5f10a3, entries = pages, length = 1).start(ctx)

  @command(aliases=['commands', 'cmd', 'command', 'cmds', 'cmdlist', 'commandlist'])
  async def help(self, ctx, *, entity=None):
    """Shows a neat, paginated embed for all of the bot commands.  Updates automatically.  Getting help for a specific cog requires the name of the class, not the name of the file."""
    if not entity:
      await self.setup_help_pag(ctx)
    else:
      cog = self.client.get_cog(entity)

      if cog:
        await self.setup_help_pag(ctx, cog, f"**{cog.qualified_name}**'s Commands")
      else:
        command = self.client.get_command(entity)
        if command:
          await self.setup_help_pag(ctx, command, command.name)

        else:
          embed = ErrorEmbed.error("Invalid Command Arguments", "That command/cog doesn't exist!")
          await ctx.send(embed=embed)

  @command(hiddem=True)
  async def helpold(self, ctx, cmd: Optional[str]):
    """Shows the help embed.  Requires a command to be passed in to get help on that command."""
    if cmd is None:
      with open("commands.txt", "r") as f:
        lines = f.readlines()

      embed = discord.Embed(
        title = "Command list for Ultimate Embed Bot",
        description = f"**{lines[0]}**\n{lines[1]}\n**{lines[2]}**\n{lines[3]}\n**{lines[4]}**\n{lines[5]}\n**{lines[6]}**\n{lines[7]}\n\nType **{get_prefix(ctx)}help <command>** or **{get_prefix(ctx)}commands <command>** for more info on a command.",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      embed.set_footer(text=f"Consider doing {ctx.prefix}commands to see a neater, paginated version of them?")
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("👀")
    else:
      if (command := get(self.client.commands, name=cmd)):
        await self.cmd_help(ctx, command)

      elif cmd.lower() == "cog" or "extension" or "extensions":
        embed = discord.Embed(
          title = "Cog list for Ultimate Embed Bot",
          description = f"**Coglist, Colorcalc, Colorlist, CooldownCommands, Counting, Embed, Events, Fun, Help, Invite, Logout, OnThisDay, Ping, Poll, ServerStats, Utils**\n\nType **{get_prefix(ctx)}commands <cog>** for more info on a cog.",
          color = 0x5f10a3,
          timestamp = datetime.datetime.utcnow()
        )
        embed.set_footer(text=f"Consider doing {ctx.prefix}commands to see a neater, paginated version of them?")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("👀")

      else:
        embed = ErrorEmbed.error("Invalid Command", "That command doesn't exist!  Make sure you are not specifying the aliases of the command, because the command won't register them as allowed arguments.")
        embed.add_field(name = "**Syntax help**", value = "<> (Required argument) | [] (Optional argument)  Aliases are separated by a **|**")
        await ctx.send(embed=embed)
  
  @command()
  async def info(self, ctx):
    """The information embed that shows links to the Ultimate Embed Bot Quickstart Guide."""
    embed = discord.Embed(
      title = "Embed Bot Quickstart Guide",
      description = f"To get a full guide on {self.client.user.mention}, click on the link below!",
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )
    embed.add_field(name = "Quickstart Guide (Google Doc)", value="https://docs.google.com/document/d/15baZOP4Ed_qkOGApHGX8h8IUdQPcqpPfjGnChtykBwQ/edit?usp=sharing", inline=False)
    embed.add_field(name = "Quickstart Guide (PDF Download)", value="https://drive.google.com/file/d/1qf3SAd_Io5oA5Gx2nSmoImqLYEVXrwNG/view", inline=False)
    msg = await ctx.send(embed=embed)
    try:
      await ctx.author.send(embed=embed)
    except:
      pass
    await msg.add_reaction("🏁")
  
  @command(aliases = ['website', 'site'])
  async def support(self, ctx):
    """Gives the link to the bot website."""
    embed = discord.Embed(
      title = "Ultimate Embed Bot Support",
      description = "Here are links to the bot website, status page, and support server!",
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )
    embed.add_field(name = "Website", value = "https://embedbot.weebly.com/", inline = False)
    embed.add_field(name = "Status Page", value = "https://embedbot.gq", inline=False)
    embed.add_field(name = "Support Server", value = "https://discord.gg/chTd8uXRrE", inline=False)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👀")
    try:
      msg = await ctx.author.send(embed=embed)
      await msg.add_reaction("👀")
    except:
      pass

def setup(client):
  client.add_cog(Help(client))