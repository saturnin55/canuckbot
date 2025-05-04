"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.2.0
"""

import json
import logging
import os
import platform
import random
import sys

import aiosqlite
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv
from DiscordBot.DiscordBot import DiscordBot
from DiscordBot.LoggingFormatter import LoggingFormatter

from database import DatabaseManager

load_dotenv()

if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)
        config["invite_link"] = os.getenv("INVITE_LINK")

"""	
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents


Default Intents:
intents.bans = False
intents.dm_messages = False
intents.dm_reactions = False
intents.dm_typing = False
intents.emojis = True
intents.emojis_and_stickers = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_scheduled_events = False
intents.guild_typing = False
intents.guilds = True
intents.integrations = True
intents.invites = False
intents.messages = True # `message_content` is required to get the content of the messages
intents.reactions = True
intents.typing = False
intents.voice_states = False
intents.webhooks = True

Privileged Intents (Needs to be enabled on developer portal of Discord), please use them only if you need them:
intents.members = False
intents.message_content = False
intents.presences = False
"""

intents = discord.Intents.default()
intents.presences = False
intents.members = False
intents.message_content = True


"""
Uncomment this if you want to use prefix (normal) commands.
It is recommended to use slash commands and therefore not use prefix commands.

If you want to use prefix commands, make sure to also enable the intent below in the Discord developer portal.
"""
# intents.message_content = True

# Setup both of the loggers

logger = logging.getLogger("discord_bot")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())
# File handler
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

os.environ["PREFIX"] = config["prefix"]
config["cogs_dir"] = f"{os.path.realpath(os.path.dirname(__file__))}/cogs/"
config["db_dir"] = f"{os.path.realpath(os.path.dirname(__file__))}/database/"
bot = DiscordBot(intents, logger, config)

# bot = DiscordBot(owner_id = os.getenv("OWNER"))
bot.run(os.getenv("TOKEN"))
