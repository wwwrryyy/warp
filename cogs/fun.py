from discord.ext import commands
import discord
import random
import datetime
from errorembed import ErrorEmbed
import urllib.request
import json
import time
import math
import os
import asyncio

class Fun(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.msg_id = 0

  def clean_jokes(self, jokes):
    return "\n".join(jokes.split("\n"))

  def get_obj(self):
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
    return obj
  
  @commands.command(aliases = ['jokes'])
  async def joke(self, ctx):
          """Get a random joke from a joke api.  NSFW jokes filtered."""

          obj = self.get_obj()
          
          if obj["flags"]["nsfw"] or obj["flags"]["racist"] or obj["flags"]["sexist"] or obj["flags"]["explicit"] == "true":
            embed = ErrorEmbed.error("NSFW Joke", "Sorry, but a  joke was flagged as NSFW.  Do you want a new joke? (y/n)")
            embed.set_footer(text="Auto-retry is still work-in-progress!  Please be patient. <3")
            await ctx.send(embed=embed)

            def check(m):
              return m.author == ctx.author and m.channel == ctx.channel

            try:
              msg_content = await self.client.wait_for('message', timeout = 60.0, check = check)
            except asyncio.TimeoutError:
              embed = ErrorEmbed.error("Timeout Error", "You didn\'t answer in time, please be quicker next time!")
              await ctx.send(embed=embed)
              return
            else:
              if msg_content.content.lower() == "y":
                await self.joke(ctx)
              else:
                return
                
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

              nsfw = 0

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

              nsfw = 0

  @commands.command(aliases=['meme', 'subreddit', 'fetchmeme', 'fm', 'gimme', 'gimmedatmeme', 'gimmememe', 'gimeeameme', 'memez', 'memes'])
  async def post(self, ctx, subreddit=None):
    """Fetch a meme/post from the specified subreddit and display all the information in a nice, formatted embed."""
    if subreddit == None:
      embed = ErrorEmbed.error("Misisng Command Arguments", "You need to specify a subreddit to fetch a meme from.")
      await ctx.send(embed=embed)

    else:
      try:
        url = f"https://meme-api.herokuapp.com/gimme/{subreddit}"
        data = urllib.request.urlopen(url).read().decode()
        obj = json.loads(data)
        title = (obj["title"])
        postlink = (obj["postLink"])
        url = (obj["preview"][len(obj["preview"])-1])
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

      except:
        embed = ErrorEmbed.error("Post Fetch Error", "Either that subreddit doesnt exist, or there are no posts with images on that subreddit.")
        await ctx.send(embed=embed)

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

  @commands.command(aliases=['randomword', 'rw', 'randword'])
  async def word(self, ctx, count=1):
    """Get a random word."""
    if count > 1:
      embed = ErrorEmbed.error("Invalid Arguments", "I can't process more than one word!")
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(
        title = "Random Word",
        description = "Provided by https://random-word-api.herokuapp.com",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )

      url = f"https://random-word-api.herokuapp.com/word?number={count}"
      data = urllib.request.urlopen(url).read().decode()
      obj = json.loads(data)
      embed.add_field(name = "Your Word", value = f"[{obj[0]}](https://www.dictionary.com/browse/{obj[0]}?s=t)")
      msg = await ctx.send(embed=embed)
      await msg.add_reaction("🤓")

  @commands.command(hidden=True)
  async def colorspin(self, ctx):
    self.msg_id = 0
    emojis = ["🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫"]

    i = 0

    embed = discord.Embed(
      title = "COLORSPIN",
      description = f"{emojis[0 + i]} {emojis[1 + i]} {emojis[2 + i]} {emojis[3 + i]} {emojis[4 + i]} {emojis[5 + i]} {emojis[6 + i]} {emojis[7 + i]}"
    )
    embed.set_footer(text="Just delete this embed to stop the colorspin ;)")
    msg = await ctx.send(embed=embed)
    time.sleep(0.5)
    self.msg_id = msg.id

    for i in range(100):
      i += 1
      embed = discord.Embed(
      title = "COLORSPIN",
      description = f"{emojis[0 + i]} {emojis[1 + i]} {emojis[2 + i]} {emojis[3 + i]} {emojis[4 + i]} {emojis[5 + i]} {emojis[6 + i]} {emojis[7 + i]}"
      )
      embed.set_footer(text="Just delete this embed to stop the colorspin ;)")
      await msg.edit(embed=embed)
      time.sleep(0.5)

  @commands.command(aliases=['lennyface', 'lennies', 'lenniez'])
  async def lenny(self, ctx, num_of_lenniez=1):
    """get some lenniez"""
    from lenny import lenny
    num_of_lenniez = int(num_of_lenniez) 
    if num_of_lenniez > 50:
      embed = ErrorEmbed.error("Invalid Command Arguments", "You can fetch no more than 50 lennies.")
      await ctx.send(embed=embed)
    else: 
      embed = discord.Embed(
        title = f"{num_of_lenniez} lenniez for you :^)",
        description = "why tf are you even wasting your time seriously",
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      for i in range(num_of_lenniez):
        embed.add_field(name = "a lenny", value = lenny())

      await ctx.send(embed=embed)

  @commands.command(name="8ball", aliases=['8b'])
  async def _8ball(self, ctx, *, question=None):
    """Play a game of 8-ball."""
    responses8ball = ['It is certain.', 
                      'It is decidedly so.', 
                      'Without a doubt.', 
                      'Yes - definitely.', 
                      'You may rely on it.', 
                      'As I see it, yes.', 
                      'Most likely.', 
                      'Outlook good.', 
                      'Yes.', 
                      'Signs point to yes.', 
                      'Reply hazy, try again.', 
                      'Ask again later.', 
                      'Better not tell you now.', 
                      'Cannot predict now.', 
                      'Concentrate and ask again.', 
                      'Dont count on it.', 
                      'My reply is no.', 
                      'My sources say no.', 
                      'Outlook not so good.', 
                      'Very doubtful.']
    if question == None:
      embed = ErrorEmbed.error("Missing Command Arguments", "You need to ask a question!")
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(
        title = question,
        description = random.choice(responses8ball),
        color = 0x5f10a3,
        timestamp = datetime.datetime.utcnow()
      )
      await ctx.send(embed=embed)

  @commands.command(aliases=['owoify'])
  async def owo(self, ctx, *, text=None):
    """owoify some text OwO"""
    if text == None:
      await ctx.send("mad owo\nyou need to provide the owoinator with some text :(")
    
    else:
      from textchange import text_to_owo

      owoified_text = text_to_owo(text)

      await ctx.send(owoified_text)

def setup(client):
  client.add_cog(Fun(client))