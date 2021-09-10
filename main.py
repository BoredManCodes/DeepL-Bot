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
@bot.command(name='lock', help='Locks the bot from responding to any commands')
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



@bot.command(name='eng', help='Translates text to english. Usage: eng!<message>.')
async def eng(ctx, message):
    if not bot.lock:
        await ctx.send(embed=discord.Embed(
        title='Translated to English',
        description='Content goes here',
        colour=discord.Color.green()
            ))
    else:
        await ctx.send(embed=discord.Embed(
        title=':lock: Server locked',
        description='An admin has locked me from responding to commands \nI\'m probably being updated or I\'m borked',
        colour=discord.Color.dark_red()
            ))

bot.run(TOKEN)