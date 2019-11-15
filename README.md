# Installation
1. Install dependencies
2. Copy `config-sample.py` to `config.py`
3. Open `config.py` and change the required settings

## Dependencies
- [discord.py](https://github.com/Rapptz/discord.py)

You can install these via `pip install -r requirements.txt`

NOTE: You might get an error about not having `qdarkstyle<2.7` installed.
You can ignore that.

# Usage
To start, run `python3 fat-bot.py`.

To stop, hit `CTRL+C`.

# Command info

### DM command
```
~dm @ROLE [MORE @ROLES...] -- MESSAGE
```
Sends a direct message to all members of the specified roles, not including
duplicates.
The double dash (`--`) between the role listing and the message is mandatory.
The roles are seperated by a single space each and must be actual role
mentions, not just strings.


### Emoji command
The bot will handle reactions added to / removed from role-assignment-messages
(RAM).
Every message included in one of the channels listed under `BOT_ROLE_CHANNEL`
in `config.py` is interpreted as a RAM.
RAMs may have arbitrary content but emoji-to-role mappings must be seperate
lines with the following format:
```
> EMOJI...-...@ROLE
```
With `EMOJI` being a reaction emoji, `@ROLE` being a role mention and `...`
being any stream of characters except for a linebreak or role mention.
The quote character (`>`) and the single dash (`-`) are mandatory.

Example:
```
**Side-Game Channel Signups**

> :muscle: #gym-goals - @FaT Bot Testing Role

> :yahyeet:      garbage bla -foo@Test role
```

