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

################################################################################
## Bot commands
################################################################################

##############################
# Author: Tim | w4rum
# DateCreated: 11/13/2019
# Purpose: DM all members of the specified roles with the specified message
###############################
@bot.command()
async def dm(ctx, *args):
    # Check arugment structure
    if len(args) < 2:
        await send_usage_help(ctx, "dm", "ROLE [MORE ROLES...] MESSAGE")

    message = args[-1]
    roles = args[:-1]

    # Check for roles with invalid format
    # The Discord client translates role mentions into "<@&ID>",
    # with ID being numerical
    invalid_roles = \
        list(filter(lambda s: re.match(r"<@&[0-9]+>", s) == None, roles))

    if len(invalid_roles) > 0:
        await send_error(ctx, "Invalid roles" \
                + " (make sure you actually meantion them with @Role):\n" \
                + ", ".join(invalid_roles))
        return

################################################################################
## Utility functions
################################################################################

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
