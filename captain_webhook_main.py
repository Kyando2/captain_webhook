# python 3.7
import discord  # version 1.3.2
from discord.ext.commands import Bot
from discord.ext.commands import CommandNotFound
from discord.ext.commands import has_permissions
import json
import functools
from wiktionaryparser import WiktionaryParser
import PyDictionary
import random
from discord.ext import tasks
from Libraries.paginator import Pages
from Libraries.pirate_lib import get_topic
import operator
from Libraries.pirate_lib import write_file
from Libraries.pirate_lib import pull_flag
from Libraries.pirate_lib import read_file
from Libraries.pirate_lib import get_nominee
from Libraries.pirate_lib import add_nominee
from Libraries.pirate_lib import append_topic
from Libraries.pirate_lib import _resolve_member_id
from Libraries.pirate_lib import pirate_error
from config.config import get_config
import time
import argparse
import shlex
import traceback
parser = WiktionaryParser()
epoch = time.time()
config = get_config()
last_topic = -1
# client.remove_command(help)
list_numbers_banned = []
client = config.client
initial_extensions = ['cogs.moderation', 'cogs.voice_cog', 'cogs.points_cog', 'cogs.miscellaneous', 'cogs.elections']


if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    config.guild = client.get_guild(700665943835148330)
    award_vc_points.start()


@tasks.loop(seconds=300)
async def award_vc_points():
    for member in config.guild.members:
        if member.voice is not None:
            if str(member.id) not in read_file("user_data.Json"):
                write_file('data/user_data.Json', {'voice_points': 0, 'text_points': 0, 'cooldown': time.time()},
                           str(member.id))
            else:
                user_data = read_file('user_data.Json')[str(member.id)]
                user_data['voice_points'] += 5
                write_file('user_data.Json', user_data, str(member.id))


@client.event
async def on_message(message):
    if message.channel.id == 701922472538144778 and str.lower(message.content).startswith("suggestion: "):
        write_file("data/suggestions.Json", message.content)
        await message.channel.send("Suggestion saved.")
        channel = client.get_channel(703480588430082110)
        text = message.content.replace("Suggestion: ", "", 1)
        await channel.send("**Suggestion: **" + text.replace("suggestion: ", "", 1) + "\n")
    await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    discord_error = discord.ext.commands.errors
    isinstance_dict = {
        discord_error.MissingPermissions: "Missing permissions to perform that action!",
        discord_error.CommandInvokeError: "There was an error executing that command!",
        discord_error.BadArgument: "One or more arguments are invalid",
    }
    for key in isinstance_dict.keys():
        if isinstance(error, key):
            await ctx.send(isinstance_dict[key])
        print(error)


client.run(config.token)



