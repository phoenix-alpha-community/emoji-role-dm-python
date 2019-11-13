#!/usr/bin/env python3

import discord
import re
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

    # Filter roles with invalid format
    # The Discord client translates role mentions into "<@&ID>",
    # with ID being numerical
    invalid_roles = \
        list(filter(lambda s: re.match(r"<@&[0-9]+>", s) == None, roles))

    if len(invalid_roles) > 0:
        await send_error(ctx, "Invalid roles" \
                + " (make sure you actually meantion them with @Role):\n" \
                + ", ".join(invalid_roles))
        return

def send_error(ctx, text):
    return ctx.send("[ERROR] " + text)

bot.run(BOT_TOKEN)
