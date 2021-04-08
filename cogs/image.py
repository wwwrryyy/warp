from discord.ext import commands
import discord
import datetime
import random
from errorembed import ErrorEmbed

class Image(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.kill_images = ['https://i.pinimg.com/originals/2b/68/86/2b6886154e707d70332e57ab088a6480.gif', 'https://i.pinimg.com/originals/29/5e/25/295e25834466ab74a5f4e758ca0484e4.gif', 'https://steamuserimages-a.akamaihd.net/ugc/923667919237640390/FCC50A2FD00D1E8AAE547128ED49314F7322B592/', 'https://i.pinimg.com/originals/4c/f4/8f/4cf48f76f04034c065d9411fe787cbc5.gif']
    self.anime_cat_girls = ['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0VwR5EjNvL9lWg87MprdLa7e_N6wbxyMcGAvlJPMawvNW0ls:https://images-na.ssl-images-amazon.com/images/I/41eehlrUIHL._SX384_BO1,204,203,200_.jpg&usqp=CAU', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRjG0hJjgYR9Lgisc-bUB4mWNMr6dXwcZqkl8rP_cEmQc3M04le:https://i.pinimg.com/originals/4d/48/8c/4d488c4c59cf11485d36c6d242d28db1.jpg&usqp=CAU', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSpUljqB_wcV-yQeWzmCHhF7bLPrPqWCDgSGKQSgpzAHjr8EbFq:https://wallpaperaccess.com/full/4765327.jpg&usqp=CAU', 'https://cdn.weeb.sh/images/HJoRMOcNM.jpeg', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQE99RVeRNXermAF8jOKmx_MMDuavRcZvkD7xOvyWlgvQ9VY-yl:https://www.pngitem.com/pimgs/m/292-2924035_transparent-neko-girl-png-cute-anime-cat-girl.png&usqp=CAU', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTm0l4rLBE8DxPOWiCfMKaVcRNM7AFSPXeoihnVY3g24ljBM84:https://i.pinimg.com/originals/a6/71/bb/a671bb111707792baf9312477dbf2ad7.jpg&usqp=CAU', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR9jBvEwBd5kJSeCMy0eYQue3XyGDaD8qPu1FhRtongdZvIu0zU:https://www.kindpng.com/picc/m/78-782427_anime-cat-girl-kawaii-png-download-anime-girl.png&usqp=CAU']

    self.anime_dog_boys = ['https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRmdBm0dsP7a7yuM6qeJqLw3hncHFB_H1cuhczeWJwu6XaFew:https://dthezntil550i.cloudfront.net/fb/latest/fb1811101959489930007744631/f9a5118e-e103-4ad7-b5a9-587c963f138c.png&usqp=CAU', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPMluIHNok6V3fWb-dtGobEoDqqlMlLpaLlXS_QxXgzwCZDF4:https://i.pinimg.com/736x/a1/6c/3e/a16c3eac43ea5c39516817137b4b9dc6.jpg&usqp=CAU', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQrof0DCq6BwT3KACMTABSoeBM2DY_-5sYcn7bh4Wg8_ggTvqk:https://i.pinimg.com/236x/f8/06/e2/f806e2ee00d2a05a18245b84d61400ac.jpg&usqp=CAU', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQEVVgrls_-xcPAlOw741FtUBJnLjRvD5wd6uBy5PzyPvPvZ8So:https://tse2.mm.bing.net/th%3Fid%3DOIP.fNCLodbYuB-eoWfLQ8UbvAHaJo%26w%3D190%26h%3D247%26c%3D8%26o%3D5%26pid%3D1.7&usqp=CAU', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTUrGUewy1KbeP2Yx2pvXGyJGci2knkIlKc3tR-Bt_8ZGhuHvA:https://static.wikia.nocookie.net/squid-girl-fanart/images/3/3e/Ql12o5ff43f01.jpg/revision/latest/scale-to-width-down/340%3Fcb%3D20180903234044&usqp=CAU', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRM-iX1mrX8kNhCWzswJaBylEIio7bzNpAyoGN3B_I8x06uqdER:https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/581d80d7-f51d-445c-a608-54e878b06e69/d80cbni-0f2c468a-dee8-4172-9c1b-a5dd23f07d1c.jpg%3Ftoken%3DeyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvNTgxZDgwZDctZjUxZC00NDVjLWE2MDgtNTRlODc4YjA2ZTY5XC9kODBjYm5pLTBmMmM0NjhhLWRlZTgtNDE3Mi05YzFiLWE1ZGQyM2YwN2QxYy5qcGcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.tUWhrgYvI-tXiPrr6fCKEZ2kLG7LyyUkV8u9sDQVEuw&usqp=CAU', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWEMHBo7Z0NRUAxkivz0p20EK0YS54vBxeXfvPWbtT9SGoBvPD:clipart-library.com/new_gallery/193-1938920_chibi-dog-animeboy-boy-anime-cute-colorful-handpainted.png&usqp=CAU', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSDNg18MzpjgYD4QaqORRmiz2-VDVVNiF4SeW5eKSU2blhEF1s:https://static3.wallpapers-anime.com/upload/20190215/5786/D/2/E/D2EmEF.jpg&usqp=CAU']

  @commands.command()
  async def kill(self, ctx, member : discord.Member = None):
    """get a random cringe anime combat scene lmao"""
    if member == None:
      embed = discord.Embed(
        title = "You died!",
        color = 0x86242a,
        timestamp = datetime.datetime.utcnow()
      )
      embed.set_image(url = random.choice(self.kill_images))
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(
        title = f"{ctx.author.mention} killed {member.mention}!",
        color = 0x86242a,
        timestamp = datetime.datetime.utcnow()
      )
      embed.set_image(url = random.choice(self.kill_images))
      await ctx.send(embed=embed)

  @commands.command(aliases=['cat'])
  async def catgirl(self, ctx):
      """get an anime cat girl"""
      embed = discord.Embed(
        title = "heres a cat girl",
        color = 0x86242a,
        timestamp = datetime.datetime.utcnow()
      )
      embed.set_image(url = random.choice(self.anime_cat_girls))
      await ctx.send(embed=embed)

  @commands.command(aliases=['dog'])
  async def dogboy(self, ctx):
      """get an anime dog boy"""
      embed = discord.Embed(
        title = "heres a dog boy",
        color = 0x86242a,
        timestamp = datetime.datetime.utcnow()
      )
      embed.set_image(url = random.choice(self.anime_dog_boys))
      await ctx.send(embed=embed)

  @commands.command(aliases=['dankmemer', 'danky', 'dank'])
  async def pepe(self, ctx, number=1):
    """pepe is taking over the world lmfao"""
    if number > 5:
      embed = ErrorEmbed.error("aagh", "im gonna get kicked for spam you can only request up to five pepes")
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(
        title = "dank memer",
        description = "dank memer",
        color = discord.Color.green(),
        timestamp = datetime.datetime.utcnow()
      )
      embed.set_author(name="dank memer", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7qQgqQdrtHy3Y1vpGfPPFKPbNVsz9j8bxBMJaIEALvujppLc:https://pbs.twimg.com/profile_images/888343365758050310/PwbZzYlR_400x400.jpg&usqp=CAU", url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7qQgqQdrtHy3Y1vpGfPPFKPbNVsz9j8bxBMJaIEALvujppLc:https://pbs.twimg.com/profile_images/888343365758050310/PwbZzYlR_400x400.jpg&usqp=CAU")
      embed.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7qQgqQdrtHy3Y1vpGfPPFKPbNVsz9j8bxBMJaIEALvujppLc:https://pbs.twimg.com/profile_images/888343365758050310/PwbZzYlR_400x400.jpg&usqp=CAU")
      embed.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7qQgqQdrtHy3Y1vpGfPPFKPbNVsz9j8bxBMJaIEALvujppLc:https://pbs.twimg.com/profile_images/888343365758050310/PwbZzYlR_400x400.jpg&usqp=CAU")
      embed.set_footer(text="dank memer", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7qQgqQdrtHy3Y1vpGfPPFKPbNVsz9j8bxBMJaIEALvujppLc:https://pbs.twimg.com/profile_images/888343365758050310/PwbZzYlR_400x400.jpg&usqp=CAU")
      i = 0
      while i < (number):
        await ctx.send(embed=embed)
        i += 1

def setup(client):
  client.add_cog(Image(client))