import discord
from discord.ext import commands
import datetime
import urllib.request
import json
import random
from errorembed import ErrorEmbed

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
  async def onthisday(self, ctx, month = get_month(), day = get_day()):
    """This command returns a random event, birth, and death on the day provided.  If a day is not provided, it will return events for **NOT** today, because the datetime library is being stupid rn."""
    month = int(month)
    day = int(day)
    
    try:
      url = f"http://history.muffinlabs.com/date/{month}/{day}"
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

    except:
      embed = ErrorEmbed.error("Invalid Command Arguments", f"Your given day `{day}` for month `{month}` is not a valid day for that month!")
      await ctx.send(embed=embed)

def setup(client):
  client.add_cog(OnThisDay(client))