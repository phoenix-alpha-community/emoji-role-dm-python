#!/usr/bin/env python3

import discord
import typing
from discord.ext import commands
from config import *  # imports token, description etc.

bot = commands.Bot(command_prefix=BOT_CMD_PREFIX, description=BOT_DESCRIPTION)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


################################################################################
## Bot commands
################################################################################

##############################
# Author: Tim | w4rum
# Editor: Matt | Mahtoid
# DateCreated: 11/13/2019
# Purpose: DM all members of the specified role with the specified message
###############################

@bot.command()
@commands.has_role('GEN')
async def dm(ctx, role: discord.Role):
    if BOT_DM_CHANNEL == str(ctx.channel):
        message = ctx.message.content.partition(">")[2].lstrip()

        sent_members = []

        for member in role.members:
            try:
                await member.send(message)
                sent_members.append(member)
            except discord.errors.Forbidden:
                await ctx.send(member.mention + " did not receive the message.")
        await ctx.send("Messages sent successfully. Sent to a total of " + str(len(sent_members)) + " people.")


@dm.error
async def dm_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await send_usage_help(ctx, "dm", "ROLE MESSAGE")
    if isinstance(error, commands.MissingRole):
        await ctx.send("Insufficient rank permissions.")
    if BOT_DM_CHANNEL != str(ctx.channel):
        await ctx.send("Insufficient channel permissions.")


################################################################################
## Utility functions
################################################################################

##############################
# Author: Tim | w4rum
# DateCreated: 11/13/2019
# Purpose: Send an error message to the current chat
###############################
def send_error_unknown(ctx):
    return send_error(ctx, "Unknown error. Tell someone from the programming" \
                      + " team to check the logs.")


##############################
# Author: Tim | w4rum
# DateCreated: 11/13/2019
# Purpose: Send an error message to the current chat
###############################
def send_error(ctx, text):
    return ctx.send("[ERROR] " + text)


##############################
# Author: Tim | w4rum
# DateCreated: 11/13/2019
# Purpose: Send a usage help to the current chat
###############################
def send_usage_help(ctx, function_name, argument_structure):
    return ctx.send("Usage: `%s%s %s`" \
                    % (BOT_CMD_PREFIX, function_name, argument_structure))


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
