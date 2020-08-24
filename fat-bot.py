#!/usr/bin/env python3

import config
import discord
import discord.utils as utils
import traceback
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
    await start_up()


guest_1 = any
guest_2 = any
guest_3 = any
guest_4 = any
guest_5 = any
guest_6 = any
final_guest = any
channel_ids = list


async def start_up():
    global channel_ids
    global guest_1, guest_2, guest_3, guest_4, guest_5, guest_6, final_guest
    the_guild: discord.Guild = bot.get_guild(398543362476605441)
    guest_1 = the_guild.get_role(744702068010516611)
    guest_2 = the_guild.get_role(744702073508986900)
    guest_3 = the_guild.get_role(744702079091736686)
    guest_4 = the_guild.get_role(744702082690580490)
    guest_5 = the_guild.get_role(744702087476281374)
    final_guest = the_guild.get_role(732451832768626829)


################################################################################
## Bot commands
################################################################################

##############################
# Author: Tim | w4rum
# Editor: Matt | Mahtoid
# DateCreated: 11/13/2019
# Purpose: DM all members of the specified role with the specified message
###############################
# Author: bigmax1994
# DateCreated: 02/02/2020
# Purpose: Added a feature to DM individual Members
###############################
@bot.command()
async def dm(ctx):
    '''
    Usage:
    ~dm @ROLE/MEMBER [MORE @ROLES/MEMBERS...] -- MESSAGE

    Sends a direct message to all members of the specified roles, not including
    duplicates.
    The double dash (`--`) between the role listing and the message is
    mandatory.
    The roles are seperated by a single space each and must be actual role
    mentions, not just strings.
    '''
    await _dm_generic(ctx, online_only=False)

@bot.command(aliases=["dmo"])
async def dm_online(ctx):
    '''
    Like the dm command but will only message users that are online (and not
    invisible).
    '''
    await _dm_generic(ctx, online_only=True)

async def _dm_generic(ctx, *, online_only):
    '''
    See ``dm``.
    '''

    if ctx.channel.id not in BOT_DM_CHANNELS:
        raise ChannelPermissionMissing()

    # split argument string into roles and message
    args = ctx.message.content.partition(ctx.invoked_with + " ")[2]
    recipient_part, _, message = args.partition("--")
    recipient_part = recipient_part.strip()
    message = message.lstrip()

    if (len(message) == 0):
        raise commands.BadArgument()

    # extract roles and Members and collect recipients
    recipients = set()
    for recipient in recipient_part.split(" "):
        if recipient == "":
            continue

        try:
            conv = commands.RoleConverter()
            recipient = await conv.convert(ctx, recipient)
            recipients |= set(recipient.members)
        except commands.BadArgument:
            #This gets triggered when there is no Role for the string 'recipients'
            member_converter = commands.MemberConverter()
            recipient = await member_converter.convert(ctx, recipient)
            recipients.add(recipient)

    sent = 0
    offline = 0
    blocked = 0

    for member in recipients:
        if online_only and member.status == discord.Status.offline:
            offline += 1
            continue
        try:
            await member.send(message)
            sent += 1
        except discord.errors.Forbidden:
            blocked += 1
            await ctx.send(f"{member.mention} did not receive the message "
                           f"(bot was blocked).")
    message = (f"Message sending complete.\n"
               f"> Sent to a total of {sent} people\n")
    if offline > 0 or blocked > 0:
        message += (f"> {offline+blocked} people did not receive a message\n"
                    f"> - {offline} offline\n"
                    f"> - {blocked} blocked")
    await ctx.send(message)


@dm.error
@dm_online.error
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

    traceback.print_exception(type(error), error, error.__traceback__)
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

    guild = bot.get_guild(payload.guild_id)

    if payload.member == guild.me or payload.channel_id not in config.START_CHANNELS:
        return
    if payload.channel_id == config.START_CHANNELS[0]:
        await payload.member.add_roles(guest_1)
    elif payload.channel_id == config.START_CHANNELS[1]:
        await payload.member.add_roles(guest_2)
        await payload.member.remove_roles(guest_1)
    elif payload.channel_id == config.START_CHANNELS[2]:
        await payload.member.add_roles(guest_3)
        await payload.member.remove_roles(guest_2)
    elif payload.channel_id == config.START_CHANNELS[3]:
        await payload.member.add_roles(guest_4)
        await payload.member.remove_roles(guest_3)
    elif payload.channel_id == config.START_CHANNELS[4]:
        await payload.member.add_roles(guest_5)
        await payload.member.remove_roles(guest_4)
    elif payload.channel_id == config.START_CHANNELS[5]:
        await payload.member.add_roles(final_guest)
        await payload.member.remove_roles(guest_5)

@bot.event
async def on_raw_reaction_remove(payload):
    await handle_reaction(payload, False)

async def handle_reaction(payload, emoji_was_added):
    channel = bot.get_channel(payload.channel_id)
    if channel.id not in BOT_ROLE_CHANNELS:
        return

    message = await channel.fetch_message(payload.message_id)
    guild = bot.get_guild(payload.guild_id)

    role, divider = await translate_emoji_role(guild, message, payload.emoji)
    if role== None:
        return

    member = await guild.fetch_member(payload.user_id)
    if emoji_was_added:
        await member.add_roles(role, divider)
    else:
        await member.remove_roles(role)
        if divider not in\
                await get_necessary_dividers_of_member(guild, member, [role]):
            await member.remove_roles(divider)

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
        role = translations[emoji]
        divider = await get_divider_for_role(guild, role)
        return (role, divider)
    else:
        return (None, None)

async def get_divider_for_role(guild, role):
    divider_prefix = b"\xe2\x81\xa3" # fancy centering spaces

    # make sure the divider itself does not induce any divider-dependencies
    if role.name.encode().startswith(divider_prefix):
        return None

    # iterate backwards through the roles and get the divider directly above
    # the specified role
    encountered = False
    for cur_role in guild.roles:
        if cur_role.name.encode().startswith(divider_prefix) and encountered:
            return cur_role
        if cur_role == role:
            encountered = True

    return None

async def get_necessary_dividers_of_member(guild, member, ignorelist):
    dividers = set()
    for role in member.roles:
        if role in ignorelist:
            continue
        div = await get_divider_for_role(guild, role)
        dividers.add(div)

    dividers.remove(None)

    return dividers

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
