#!/usr/bin/env python3

import discord
import typing
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
# Purpose: DM all members of the specified role with the specified message
###############################
@bot.command()
async def dm(ctx, role: discord.Role):
    # extract raw text message including whitespaces from context
    message = ctx.message.content.partition(">")[2].lstrip()
    author  = ctx.message.author

    prefix = """\
```
========================================
= Sender: %s
= Recipient role: %s
========================================
```\
""" % (author.nick or author, role.name)

    suffix = """\
```
========================================
```\
"""

    for member in role.members:
        dm_channel = member.dm_channel
        if (dm_channel == None):
            await member.create_dm()
            dm_channel = member.dm_channel
        await dm_channel.send(prefix + message + suffix)

<<<<<<< HEAD
=======
    await ctx.send("Messages sent successfully. Sent to a total of %i people." \
                   % len(role.members))

@dm.error
async def dm_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await send_usage_help(ctx, "dm", "ROLE MESSAGE")
    else:
        await send_error_unknown(ctx)
        raise error

>>>>>>> 00e5fb5b0aef6750544a925583008f4609857787
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
