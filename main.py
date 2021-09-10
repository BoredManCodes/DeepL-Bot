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


@bot.event
async def on_command_error(ctx, error):
    print("Permission Error")
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Only Admins can run that command. Please beg for the role in #general')

# lock the bot from doing any translating
# @bot.command(name='lock', help='Locks the bot from responding to any commands', pass_context=True)
# @commands.has_role('admin')
# async def lock(ctx):
#     if not bot.lock:
#         print("LOCKED")
#         await ctx.send(embed=discord.Embed(
#         title=':lock: Bot locked',
#         description='I am now locked and won\'t reply to commands',
#         colour=discord.Color.dark_red()
#             ))
#         bot.lock = True
#     else:
#         print("UNLOCKED")
#         await ctx.send(embed=discord.Embed(
#         title=':unlock: Bot unlocked',
#         description='I am now unlocked and will reply to commands',
#         colour=discord.Color.green()
#             ))
#         bot.lock = False



@bot.command(name='eng', help='Translates text to english. Usage: lang!eng <message>.', pass_context=True)
async def eng(ctx, message):
    if not bot.lock:
        await ctx.send('Translating.... Please wait', delete_after=5)
        text_to_translate = message
        driver_path = './chromedriver'
        driver = webdriver.Chrome(driver_path)
        deepl_url = 'https://www.deepl.com/translator/en'
        driver.get(deepl_url)

        input_css = 'div.lmt__inner_textarea_container textarea'
        input_area = driver.find_element_by_css_selector(input_css)
        input_area.clear()
        input_area.send_keys(text_to_translate)
        time.sleep(5)
        output_button_xpath = '/html/body/div[2]/div[1]/div[4]/div[4]/div[3]/div[1]/div[2]/div[1]/button'
        output_button = driver.find_element_by_xpath(output_button_xpath)
        output_button.click()
        time.sleep(0)
        english_button_xpath = '/html/body/div[2]/div[1]/div[4]/div[4]/div[3]/div[1]/div[2]/div[1]/div[2]/button[6]'
        english_button = driver.find_element_by_xpath(english_button_xpath)
        english_button.click()
        time.sleep(5)
        button_css = ' div.lmt__target_toolbar__copy button'
        button = driver.find_element_by_css_selector(button_css)
        button.click()
        content = clipboard.paste()
        driver.quit()

        print('_' * 50)
        print('Original    :', text_to_translate)
        print('Translation :', content)
        print('_' * 50)
        await ctx.send(embed=discord.Embed(
        title='Translated to English',
        description=content,
        colour=discord.Color.green()
            ))
    else:
        await ctx.send(embed=discord.Embed(
        title=':lock: Server locked',
        description='An admin has locked me from responding to commands \nI\'m probably being updated or I\'m borked',
        colour=discord.Color.dark_red()
            ))
    await ctx.message.delete()


bot.run(TOKEN)