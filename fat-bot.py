#!/usr/bin/env python3

import discord
import discord.utils as utils
import typing
import re
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

##############################
# Authors: just a normal guy, Tim | w4rum
# Editor: Matt | Mahtoid
# DateCreated: 11/14/2019
# Purpose: Add or remove a specific role from a user when they react with a
#          specific emoji to a role-assignment-message
###############################
@bot.event
async def on_raw_reaction_add(payload):
    await handle_reaction(payload, True)

@bot.event
async def on_raw_reaction_remove(payload):
    await handle_reaction(payload, False)

async def handle_reaction(payload, emoji_was_added):
    channel = bot.get_channel(payload.channel_id)
    if channel.name not in BOT_ROLE_CHANNEL:
        return

    message = await channel.fetch_message(payload.message_id)
    guild = bot.get_guild(payload.guild_id)
    role = await translate_emoji_role(guild, message, payload.emoji)
    if role == None:
        return
    member = await guild.fetch_member(payload.user_id)
    if emoji_was_added:
        await member.add_roles(role)
    else:
        await member.remove_roles(role)

async def translate_emoji_role(guild, message, emoji):
    emoji = str(emoji)

    # get all emoji-to-role translations by parsing the message
    translations = {}
    pattern = r">* *([^ \n]+) [^\n]*-[^\n]*<@&([0-9]+)>"
    for match in re.finditer(pattern, message.content):
        expected_emoji, role_id = match.group(1,2)
        expected_emoji = str(expected_emoji) # this will ensure custom
                                             # emojis can also be checked via
                                             # string comparison
        role = utils.get(guild.roles, id=int(role_id))
        translations[expected_emoji] = role

    if emoji in translations:
        return translations[emoji]
    else:
        return None

# Debug function
#@bot.event
#async def on_message(message):
#    print(message.content.encode())


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
