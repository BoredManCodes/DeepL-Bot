##################################################
#                                                #
#             DeepL Translate Bot                #
#                                                #
#       Hacked together by BoredManPlays         #
#                                                #
##################################################


import os
import discord
from discord.ext import commands
from decouple import config
import clipboard
from selenium import webdriver
import time


# let's learn how to read from .env files
TOKEN = config("TOKEN")
bot = commands.Bot(command_prefix='lang!')
bot.lock = False
bot.debug = False

@bot.event
async def on_command_error(ctx, error):
    print(error)
    await ctx.send('<@324504908013240330>')
    await ctx.send(embed=discord.Embed(
        title='We ran into an error',
        description=error,
        colour=discord.Color.red()
    ))
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Only Admins can run that command. Please beg for the role in #general')

# lock the bot from doing any translating
@bot.command(name='lock', help='Locks the bot from responding to any commands', pass_context=True)
@commands.has_role('admin')
async def lock(ctx):
    if not bot.lock:
        print("LOCKED")
        await ctx.send(embed=discord.Embed(
        title=':lock: Bot locked',
        description='I am now locked and won\'t reply to commands',
        colour=discord.Color.dark_red()
            ))
        bot.lock = True
    else:
        print("UNLOCKED")
        await ctx.send(embed=discord.Embed(
        title=':unlock: Bot unlocked',
        description='I am now unlocked and will reply to commands',
        colour=discord.Color.green()
            ))
        bot.lock = False

@bot.command(name='debug', help='Enables debug mode', pass_context=True)
@commands.has_role('admin')
async def debug(ctx):
    if not bot.debug:
        bot.debug = True
        await ctx.send('Debug enabled', delete_after=4)

    else:
        bot.debug = False
        await ctx.send('Debug enabled', delete_after=4)


@bot.command(name='eng', help='Translates text to english. Usage: lang!eng <message>.', pass_context=True)
async def eng(ctx, *, message):
    if not bot.lock:
        await ctx.send('Translating.... Please wait', delete_after=4)
        text_to_translate = message
        driver_path = './chromedriver'
        driver = webdriver.Chrome(driver_path)
        deepl_url = 'https://www.deepl.com/translator/en'
        driver.get(deepl_url)

        input_css = 'div.lmt__inner_textarea_container textarea'
        input_area = driver.find_element_by_css_selector(input_css)
        input_area.clear()
        input_area.send_keys(text_to_translate)
        time.sleep(10)
        output_button_xpath = '/html/body/div[2]/div[1]/div[4]/div[4]/div[3]/div[1]/div[2]/div[1]/button'
        output_button = driver.find_element_by_xpath(output_button_xpath)
        output_button.click()
        time.sleep(6)
        english_button_xpath = '/html/body/div[2]/div[1]/div[4]/div[4]/div[3]/div[3]/div[7]/div[1]/button[6]'
        english_button = driver.find_element_by_xpath(english_button_xpath)
        english_button.click()
        time.sleep(3)
        copy_button_css = 'div.lmt__target_toolbar__copy button'
        copy_button = driver.find_element_by_css_selector(copy_button_css)
        copy_button.click()
        content = clipboard.paste()
        input_lang_xpath = '/html/body/div[2]/div[1]/div[4]/div[4]/div[1]/div[1]/div/button/span/strong'
        input_lang = driver.find_element_by_xpath(input_lang_xpath).text
        driver.quit()

        dashes = '_' * 50
        original ='Original    :', text_to_translate
        translation = 'Translation :', content
        detected_lang = 'Detected Language :', input_lang
        if debug:
            await ctx.send(dashes)
            await ctx.send(original)
            await ctx.send(translation)
            await ctx.send(dashes)
            await ctx.send(detected_lang)

        print(dashes)
        print(original)
        print(translation)
        print(dashes)
        print(detected_lang)
        formatted_content = str(content).capitalize()
        embed_title = "Translated to English from " + input_lang
        formatted_embed_title = str(embed_title).strip("()\'\",\',\'")
        await ctx.send(embed=discord.Embed(
        title=formatted_content,
        description=formatted_embed_title,
        colour=discord.Color.green()
            ))
    else:
        await ctx.send(embed=discord.Embed(
        title=':lock: Bot locked',
        description='An admin has locked me from responding to commands \nI\'m probably being updated or I\'m borked',
        colour=discord.Color.red()
            ))
    await ctx.message.delete()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)