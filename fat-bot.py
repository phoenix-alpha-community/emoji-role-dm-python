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
@commands.has_role(BOT_DM_REQUIRED_ROLE)
async def dm(ctx):
    if str(ctx.channel) != BOT_DM_CHANNEL:
        raise ChannelPermissionMissing()

    # split argument string into roles and message
    args = ctx.message.content.partition("dm ")[2]
    role_part, _, message = args.partition("--")
    role_part = role_part.strip()
    message = message.lstrip()
    if (len(message) == 0):
        raise commands.BadArgument()

    # extract roles and collect recipients
    recipients = set()
    for role in role_part.split(" "):
        conv = commands.RoleConverter()
        role = await conv.convert(ctx, role)
        recipients |= set(role.members)

    sent_members = []

    for member in recipients:
        try:
            await member.send(message)
            sent_members.append(member)
        except discord.errors.Forbidden:
            await ctx.send(member.mention + " did not receive the message.")
    await ctx.send("Messages sent successfully. Sent to a total of %i people." \
                   % len(sent_members))


@dm.error
async def dm_error(ctx, error):
    error_handlers = {

        commands.BadArgument: lambda:
            send_usage_help(ctx, "dm", "ROLE [MORE ROLES...] -- MESSAGE"),

        commands.MissingRole: lambda:
            ctx.send("Insufficient rank permissions."),

        ChannelPermissionMissing: lambda:
            ctx.send("Insufficient channel permissions."
                     + " The bot is in the wrong channel.")
    }

    for error_type, handler in error_handlers.items():
        if isinstance(error, error_type):
            await handler()
            return

    await send_error_unknown(ctx)


################################################################################
## Utility functions and classes
################################################################################

##############################
# Author: Tim | w4rum
# DateCreated: 11/14/2019
# Purpose: Error class used when a command is issued in the wrong channel
###############################
class ChannelPermissionMissing(commands.CommandError): pass


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
