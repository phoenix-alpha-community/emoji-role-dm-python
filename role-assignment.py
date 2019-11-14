# IMPORT
from config import *

# FUNCTION
def role_assignment():
	# CLASS
	class Data:
		def __init__(self, channel, message, reactions):
			self.channel = channel
			self.message = message
			self.reactions = reactions

	# IMPORT
	from discord.utils import get
	import discord

	# VARIABLES
	side_game = Data(side_game_channel, side_game_message, side_game_reactions)

	hobbies = Data(hobbies_channel, hobbies_message, hobbies_reactions)

	client = discord.Client()

	# CODE
	@client.event
	async def on_reaction_add(reaction, user):
		if reaction.message.channel == side_game.channel:
			if reaction.message.id == side_game.message:
				i = 0
				for emoji in side_game.reactions:
					if emoji == reaction:
						member = await reaction.message.guild.fetch_member(user.id)
						if not member:
							return
						role = get(reaction.message.guild.roles, name=side_game_reactions[reaction])
						await member.add_roles(role)
					else:
						i += 1

		elif reaction.message.channel == hobbies.channel:
			if reaction.message.id == hobbies.message:
				pass
