#!/usr/bin/env python3

import discord
from discord.ext import commands
from config import * # imports token, description etc.

bot = commands.Bot(command_prefix=BOT_CMD_PREFIX, description=BOT_DESCRIPTION)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def dm(ctx, *args):
    if len(args) < 2:
        await ctx.send("Usage: `~dm ROLE [MORE ROLES...] MESSAGE`")

    message = args[-1]
    roles = args[:-1]

bot.run(BOT_TOKEN)
