from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import discord
import random
import datetime
from errorembed import ErrorEmbed
import urllib.request
from utilities.utility import Pag
import json
import time
import math
import os

class Fun(commands.Cog):
  def __init__(self, client):
    self.client = client

  def clean_jokes(self, jokes):
    return "\n".join(jokes.split("\n"))

  @commands.command(aliases = ['addjoke', 'aj', 'add'])
  @cooldown(1, 43200, BucketType.user)
  async def submitjoke(self, ctx, *, joke=None):
      """Add a joke to the joke repository exclusive to this bot.  Only people with the permission of **Manage Messages** associated with their role can add jokes, and the cooldown is 12 hours to avoid spam."""
      if ctx.author.guild_permissions.manage_messages:
        if joke == None:
          embed = ErrorEmbed.error("Missing Command Arguments", "You have to provide a joke to add!")
          await ctx.send(embed=embed)
          return
        else:
          with open("jokes.txt", "a") as f:
            f.writelines(f"{joke}\n")
          f.close()
          embed = discord.Embed(
            title = "Add Joke Successful",
            description = f"Joke added: {joke}",
            color = 0x5f10a3,
            timestamp = datetime.datetime.utcnow()
          )
          await ctx.message.delete()
          msg = await ctx.send(embed=embed)
          await msg.add_reaction("🤣")
      else:
        embed = ErrorEmbed.error("Missing Permissions", "You can't add jokes! You must have the permission of **Manage Messages** to add jokes.")
        await ctx.send(embed=embed)
        return

  @commands.command(aliases = ['jokes'])
  async def joke(self, ctx, method=None, *, joke_line=None):
    """Specify a method (either list, or get).  If no method is stated, you will get a random joke from a free joke api.  For "get", specify the number of the line of the joke you want to get. "list" doesnt require any arguments after that and returns a **REALLY** messy paginated version of all the jokes, so paginating all jokes is still WIP."""
    if method==None:
        import requests
        import json
        url = "https://jokeapi-v2.p.rapidapi.com/joke/Any"
        headers = {
            'x-rapidapi-key': os.getenv('JOKE-API-KEY'),
            'x-rapidapi-host': "jokeapi-v2.p.rapidapi.com"
            }
        raw = requests.request("GET", url, headers=headers)
        response = raw.text
        obj = json.loads(response)
        if obj["flags"]["nsfw"] or obj["flags"]["racist"] or obj["flags"]["sexist"] or obj["flags"]["explicit"] == "true":
          embed = ErrorEmbed.error("Flagged Jokes", "Sorry, a joke flagged as **nsfw** or **racist** or **sexist** or **explicit** was returned, so we couldn't show it.  Please try again.")
          await ctx.send(embed=embed)
        else:
          if obj["type"] == "single":
            embed = discord.Embed(
              title = "Joke Type: Single",
              description = obj["joke"],
              color = 0x5f10a3,
              timestamp = datetime.datetime.utcnow()
            )
            embed.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)
            embed.set_author(name = "This joke was provided by JokeApi v2 😘", url = "https://rapidapi.com/Sv443/api/jokeapi-v2", icon_url = "https://www.google.com/url?sa=i&url=https%3A%2F%2Femojiisland.com%2Fproducts%2Fkiss-with-heart-iphone-emoji-jpg&psig=AOvVaw2QKksyqp-o5_ZWsg2-xfOm&ust=1615172297228000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCNDB9umXne8CFQAAAAAdAAAAABAD")

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("🤣")

          elif obj["type"] == "twopart":
            embed = discord.Embed(
              title = "Joke Type: Two-part",
              description = f"Setup: {obj['setup']}\nPunchline: {obj['delivery']}",
              color = 0x5f10a3,
              timestamp = datetime.datetime.utcnow()
            )
            embed.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)
            embed.set_author(name = "This joke was provided by JokeApi v2 😘", url = "https://rapidapi.com/Sv443/api/jokeapi-v2", icon_url = "https://www.google.com/url?sa=i&url=https%3A%2F%2Femojiisland.com%2Fproducts%2Fkiss-with-heart-iphone-emoji-jpg&psig=AOvVaw2QKksyqp-o5_ZWsg2-xfOm&ust=1615172297228000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCNDB9umXne8CFQAAAAAdAAAAABAD")

            msg = await ctx.send(embed=embed)
            await msg.add_reaction("🤣")
    
    elif method.lower() == "get":
      with open("jokes.txt", "r") as f:
        jokes = f.readlines()
      try:
        joke_line = int(joke_line)
        gotjoke = jokes[joke_line-1]
        embed = discord.Embed(
          title = "Retrieved Joke",
          description = gotjoke,
          color = 0x5f10a3,
          timestamp = datetime.datetime.utcnow()
        )
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🤣")

      except:
        embed = ErrorEmbed.error("Invalid Command Arguments", f"You have to provide a **number** that is in the range of 1 to {len(jokes)}")
        await ctx.send(embed=embed)
        return

    elif method.lower() == "list":
      with open("jokes.txt", "r") as f:
        jokes = f.readlines()
        pager = Pag(
          timeout = 1000,
          entries = [jokes[i: i + 5] for i in range(0, len(jokes), 5)],
          length=1,
          color = 0x5f10a3,
        )
        await pager.start(ctx)

    else:
      embed = ErrorEmbed.error("Invalid Arguments", "Please check to make sure you are using valid arguments.")
      await ctx.send(embed=embed)

  @commands.command()
  async def meme(self, ctx, subreddit=None):
    """Fetch a meme/post from the specified subreddit and display all the information in a nice, formatted embed."""
    if subreddit == None:
      embed = ErrorEmbed.error("Misisng Command Arguments", "You need to specify a subreddit to fetch a meme from.")
      await ctx.send(embed=embed)

    else:
      url = f"https://meme-api.herokuapp.com/gimme/{subreddit}"
      data = urllib.request.urlopen(url).read().decode()
      obj = json.loads(data)
      title = (obj["title"])
      postlink = (obj["postLink"])
      url = (obj["preview"][1])
      author = (obj["author"])
      upvotes = (obj["ups"])
      embed = discord.Embed(
        title = title,
        description = f"[**Post link**]({postlink})\n[**Author Profile**](https://www.reddit.com/u/{author})",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      embed.set_image(url=url)
      embed.set_author(name=f"r/{subreddit}", url = f"https://www.reddit.com/r/{subreddit}", icon_url = "https://external-preview.redd.it/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png?auto=webp&s=38648ef0dc2c3fce76d5e1d8639234d8da0152b2")
      bullet = " • "
      embed.set_footer(text=f"👍 {upvotes} {bullet} u/{author}")
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("🤣")

  @commands.command(aliases=['slotmachine', 'sm'])
  async def slots(self, ctx):
    """A fun slots simulator. This game does not win the user currency."""

    emojis = ["🎁", "🎉", "🎀", "🧧", "🎊", "🏆", "💵"]

    bet_amount = random.randrange(1000, 5000)

    spinning = discord.Embed(
      title = f"Spinning ${bet_amount}...",
    )

    embed = discord.Embed(
      title = "Slots Game!",
      description = "`🚫` `🚫` `🚫`",
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )
    delthis = await ctx.send(embed = spinning)
    time.sleep(3)
    await delthis.delete()
    slot = await ctx.send(embed=embed)
    time.sleep(1)

    emoji1 = random.choice(emojis)
    
    embed = discord.Embed(
      title = "Slots Game!",
      description = f"`{emoji1}` `🚫` `🚫`",
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )

    await slot.edit(embed=embed)

    time.sleep(1)

    emoji2 = random.choice(emojis)
    
    embed = discord.Embed(
      title = "Slots Game!",
      description = f"`{emoji1}` `{emoji2}` `🚫`",
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )

    await slot.edit(embed=embed)

    time.sleep(1)

    emoji3 = random.choice(emojis)
    
    embed = discord.Embed(
      title = "Slots Game!",
      description = f"`{emoji1}` `{emoji2}` `{emoji3}`",
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )

    await slot.edit(embed=embed)

    time.sleep(1)

    if emoji1 == emoji2 or emoji1 == emoji3 or emoji2 == emoji3 or emoji2 == emoji3:
      embed = discord.Embed(
        title = "🏆 Slots Game! 🏆",
        description = f"{emoji1} {emoji2} {emoji3}",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      embed.add_field(name = "Winnings!", value = f"You bet ${bet_amount} and won ${bet_amount * 3} (Net gain: ${bet_amount * 2})")
      await slot.edit(embed=embed)
      await slot.add_reaction("🏆")
    
    elif (emoji1 == emoji2 == emoji3):
      won = (bet_amount * 5) + (math.ceil(1000000) / bet_amount)
      embed = discord.Embed(
        title = "🏆 Slots Game! 🏆",
        description = f"`{emoji1}` `{emoji2}` `{emoji3}`",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      embed.add_field(name = "Winnings", value = f"You won the **JACKPOT**! That means you won ${won}!")
      await slot.edit(embed=embed)
      await slot.add_reaction("🏆")

    else:
      embed = discord.Embed(
        title = "😞 Slots Game! 😞",
        description = f"`{emoji1}` `{emoji2}` `{emoji3}`",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      embed.add_field(name = "You lost!", value = "You didn't get any matching icons.")
      await slot.edit(embed=embed)
      await slot.add_reaction("😞")

def setup(client):
  client.add_cog(Fun(client))