import discord
from discord.ext import commands
import datetime
import urllib.request
import json
import random
import os

class OnThisDay(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  def get_day():
    from datetime import date

    today = date.today()

    day = today.strftime("%d/%m/%y")[:2]
    return day

  def get_month():
    from datetime import date

    today = date.today()

    month = today.strftime("%d/%m/%y")[3:5]
    return month


  @commands.command(aliases = ['otd', 'thisday', 'dayinhistory', 'todayinhistory', 'fact', 'todaysfact', 'factstoday'])
  async def onthisday(self, ctx, day=get_day(), month=get_month()):
    """This command returns a random event, birth, and death on the day provided.  If a day is not provided, it will return events for **NOT** today, because the datetime library is being stupid rn."""
    url = f"http://history.muffinlabs.com/date/{day}/{month}"
    data = urllib.request.urlopen(url).read().decode()
    obj = json.loads(data)

    choice1 = random.choice(obj["data"]["Events"])
    choice2 = random.choice(obj["data"]["Births"])
    choice3 = random.choice(obj["data"]["Deaths"])

    choice1year = choice1["year"]
    choice2year = choice2["year"]
    choice3year = choice3["year"]

    choice1text = choice1["text"]
    choice2text = choice2["text"]
    choice3text = choice3["text"]


    embed = discord.Embed(
      title = obj["date"],
      description = obj["url"],
      color = 0x5f10a3,
      timestamp = datetime.datetime.utcnow()
    )
    embed.add_field(name="Random Event", value = f"Year: {choice1year}\nEvent: {choice1text}", inline=False)

    embed.add_field(name="Random Birth", value = f"Year: {choice2year}\nBirth: {choice2text}", inline=False)

    embed.add_field(name="Random Death", value = f"Year: {choice3year}\nDeath: {choice3text}", inline=False)

    embed.set_author(name = "Provided by the Today in History API", url = "https://history.muffinlabs.com/#api")
    embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🤓")

def setup(client):
  client.add_cog(OnThisDay(client))