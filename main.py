from epicstore_api import EpicGamesStoreAPI, OfferData
import discord
import settings
from discord import app_commands
from discord.ext import tasks, commands
import requests
import json
from urllib.request import urlopen
import calendar
import asyncio
from datetime import datetime, time as dt_time
from time import strftime, localtime
import time
import pathlib

logger = settings.logging.getLogger("bot")


def run():
    intents = discord.Intents.default()
    intents.messages = True
    intents.reactions = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"User:{bot.user}")
        bot.loop.create_task(scheduled_command())
        try:
            synced = await bot.tree.sync()
            print(f'Synced {len(synced)} commands(s)')
        # for item in titles['data']['Catalog']['searchStore']['elements']:
        #    name = item['title']
        #    price = item['price']['totalPrice']['fmtPrice']['discountPrice']
        #    key_images = item['keyImages']
        #    image_url = None
        #    for image in key_images:
        #        if image.get('type') == 'OfferImageWide':
        #            image_url = image.get('url')
        #    if price == "0" and name != "PAYDAY 2":
        #        print(name)

        except Exception as e:
            print(e)

    api = EpicGamesStoreAPI()

    response = requests.get(
        "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions").text
    titles = json.loads(response)

    async def scheduled_command():
        while True:
            f = open("lastexecute.txt", "r")
            timediff = int(f.read())
            f.close()
            time_now = int(time.time())
            target_time = dt_time(hour=16, minute=0, second=0)
            target_time_now = datetime.now().time()
            if time_now >= int(timediff) + 604740 and target_time_now >= target_time:
                channel = bot.get_channel(795428143107801098)
                await channel.send("<@&847939354978811924>")
                for item in titles['data']['Catalog']['searchStore']['elements']:
                    name = item['title']
                    price = item['price']['totalPrice']['fmtPrice']['discountPrice']
                    key_images = item['keyImages']
                    url = item['urlSlug']
                    oldprice = item['price']['totalPrice']['fmtPrice']['originalPrice']
                    offer = item['price']['lineOffers']
                    link = 'https://store.epicgames.com/en-US/p/'+url
                    for image in key_images:
                        if image.get('type') == 'OfferImageWide':
                            image_url = image.get('url')
                    for k in offer:
                        rules = k["appliedRules"]
                        for x in rules:
                            date = x["endDate"]
                    t = datetime(
                        int(date[0:4]), int(date[5:7]), int(date[8:10]), int(date[11:13]), int(date[14:16]))
                    count = str(calendar.timegm(t.timetuple()))
                    embed = discord.Embed(
                        color=discord.Color.green())
                    embed.add_field(name=name, value="~~"+oldprice+"~~ **FREE**" +
                                    "\n Ends <t:"+count+":R> \n[Claim Game]("+link+") ")
                    embed.set_image(url=image_url)
                    embed.set_footer(text="Bot by Her0")
                    embed.set_author(name="Epic Games Store",
                                     icon_url="https://i.imgur.com/ANplrW5.png", url="https://store.epicgames.com/en-US/free-games")
                    if price == "0" and name != "PAYDAY 2":
                        messageembed = await channel.send(embed=embed)
                        await messageembed.add_reaction("🔥")
                        await messageembed.add_reaction("🗑️")
                f = open("lastexecute.txt", "w")
                f.write(str(time_now))
                f.close()
            await asyncio.sleep(60)

    @bot.tree.command(name='epic', description="Current Free games on the Epic Games Store")
    async def epic(interaction):
        try:
            await interaction.response.send_message("Here you go ;)", ephemeral=True)
            for item in titles['data']['Catalog']['searchStore']['elements']:
                name = item['title']
                price = item['price']['totalPrice']['fmtPrice']['discountPrice']
                key_images = item['keyImages']
                url = item['urlSlug']
                oldprice = item['price']['totalPrice']['fmtPrice']['originalPrice']
                offer = item['price']['lineOffers']
                link = 'https://store.epicgames.com/en-US/p/'+url
                for image in key_images:
                    if image.get('type') == 'OfferImageWide':
                        image_url = image.get('url')
                for k in offer:
                    rules = k["appliedRules"]
                    for x in rules:
                        date = x["endDate"]
                t = datetime(
                    int(date[0:4]), int(date[5:7]), int(date[8:10]), int(date[11:13]), int(date[14:16]))
                count = str(calendar.timegm(t.timetuple()))
                embed = discord.Embed(
                    color=discord.Color.green())
                embed.add_field(name=name, value="~~"+oldprice+"~~ **FREE**" +
                                "\n Ends <t:"+count+":R> \n[Claim Game]("+link+") ")
                embed.set_image(url=image_url)
                embed.set_footer(text="Bot by Her0")
                embed.set_author(name="Epic Games Store",
                                 icon_url="https://i.imgur.com/ANplrW5.png", url="https://store.epicgames.com/en-US/free-games")
                if price == "0" and name != "PAYDAY 2":
                    messageembed = await interaction.channel.send(embed=embed)
                    await messageembed.add_reaction("🔥")
                    await messageembed.add_reaction("🗑️")

        except Exception as e:
            print(e)

    @bot.tree.command(name='nextepic', description="Next Free games on the Epic Games Store")
    async def nextepic(interaction):
        try:
            await interaction.response.send_message("Here you go ;)", ephemeral=True)
            for item in titles['data']['Catalog']['searchStore']['elements']:
                name = item['title']
                price = item['price']['totalPrice']['fmtPrice']['discountPrice']
                discount = item['price']['totalPrice']['discount']
                time_now = int(time.time())
                key_images = item['keyImages']
                url = item['urlSlug']
                oldprice = item['price']['totalPrice']['fmtPrice']['originalPrice']
                offer = item['promotions']['upcomingPromotionalOffers']
                link = 'https://store.epicgames.com/en-US/p/'+url
                for image in key_images:
                    if image.get('type') == 'OfferImageWide':
                        image_url = image.get('url')
                for k in offer:
                    rules = k["promotionalOffers"]
                    for x in rules:
                        startDate = x["startDate"]
                        endDate = x["endDate"]
                t = datetime(
                    int(startDate[0:4]), int(startDate[5:7]), int(startDate[8:10]), int(startDate[11:13]), int(startDate[14:16]))
                count = str(calendar.timegm(t.timetuple()))
                embed = discord.Embed(
                    color=discord.Color.dark_gray())
                embed.add_field(name=name, value="Currently: "+oldprice+" **SOON TO BE FREE**" +
                                "\n Starts <t:"+count+":R> \n[Link to game]("+link+") ")
                embed.set_image(url=image_url)
                embed.set_footer(
                    text="Bot by Her0 - This comand is still a WIP")
                embed.set_author(name="Epic Games Store",
                                 icon_url="https://i.imgur.com/ANplrW5.png", url="https://store.epicgames.com/en-US/free-games")
                if int(count) >= int(time_now) and name != "PAYDAY 2" and discount == 0:
                    await interaction.response(embed=embed)
                else:
                    None

        except Exception as e:
            print(e)

    @bot.tree.command(name='epicadmin', description="Announcement command for admins")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @app_commands.default_permissions(administrator=True)
    async def epicadmin(interaction, role: discord.Role):
        try:
            await interaction.response.send_message("Here you go ;)", ephemeral=True)
            if role.mention == "<@&794755529234579516>":
                everyonemention = "@everyone"
                await interaction.channel.send(everyonemention)
            else:
                await interaction.channel.send(role.mention)

            for item in titles['data']['Catalog']['searchStore']['elements']:
                name = item['title']
                price = item['price']['totalPrice']['fmtPrice']['discountPrice']
                key_images = item['keyImages']
                url = item['urlSlug']
                oldprice = item['price']['totalPrice']['fmtPrice']['originalPrice']
                offer = item['price']['lineOffers']
                link = 'https://store.epicgames.com/en-US/p/'+url
                for image in key_images:
                    if image.get('type') == 'OfferImageWide':
                        image_url = image.get('url')
                for k in offer:
                    rules = k["appliedRules"]
                    for x in rules:
                        date = x["endDate"]
                t = datetime(
                    int(date[0:4]), int(date[5:7]), int(date[8:10]), int(date[11:13]), int(date[14:16]))
                count = str(calendar.timegm(t.timetuple()))
                embed = discord.Embed(
                    color=discord.Color.green())
                embed.add_field(name=name, value="~~"+oldprice+"~~ **FREE**" +
                                "\n Ends <t:"+count+":R> \n[Claim Game]("+link+") ")
                embed.set_image(url=image_url)
                embed.set_footer(text="Bot by Her0")
                embed.set_author(name="Epic Games Store",
                                 icon_url="https://i.imgur.com/ANplrW5.png", url="https://store.epicgames.com/en-US/free-games")
                if price == "0" and name != "PAYDAY 2":
                    messageembed = await interaction.channel.send(embed=embed)
                    await messageembed.add_reaction("🔥")
                    await messageembed.add_reaction("🗑️")

        except Exception as e:
            print(e)

    @bot.event
    async def on_message(message):
        await bot.process_commands(message)

    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

    @bot.event
    async def on_application_command_error(interaction, error):
        if isinstance(error, commands.CommandOnCooldown):
            await interaction.response.send_message(error)
        else:
            raise error


if __name__ == '__main__':
    run()


# @bot.tree.command(name="Alert", description="enables alerts as well as which group to @", )
# @bot.tree.choice(Alert="")


# STEAM BELOW
# @bot.tree.command(name='steam', description="Current Free games/DLCs on Steam")
# async def steam(interaction):
#    try:
#
#        embed = discord.Embed(
#            color=discord.Color.green())
#        embed.add_field(name="", value="~~""~~ **FREE**" +
#                        "\n Ends <t:"":R> \n[Claim Game]("") ")
#        embed.set_image(url="")
#        embed.set_footer(text="Service by Her0")
#        embed.set_author(name="Steam",
#                         icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/768px-Steam_icon_logo.svg.png", url="https://freetokeep.gg/")
#        await interaction.channel.send(embed=embed)
#    except Exception as e:
#        print(e)
# async def schedule_message():
#    now = datetime.datetime.now()
#    then = now+datetime.timedelta(days=1)
#    then.replace(hour=16, minute=19)
#    wait_time = (then-now).total_seconds()
#    asyncio.sleep(wait_time)
