"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.2.0
"""

import logging
import os
import platform
import random

import aiosqlite
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context

from database import DatabaseManager

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


class DiscordBot(commands.Bot):
    def __init__(
        self, intents: discord.Intents, logger: logging.Logger, config: dict
    ) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or(config["prefix"]),
            intents=intents,
            help_command=None,
        )
        """
        This creates custom bot variables so that we can access these variables in cogs more easily.

        For example, The config is available using the following code:
        - self.config # In this class
        - bot.config # In this file
        - self.bot.config # In cogs
        """
        self.logger = logger
        self.config = config
        self.database = None

    async def init_db(self) -> None:
        async with aiosqlite.connect(f"{self.config['db_dir']}/database.db") as db:
            with open(f"{self.config['db_dir']}/schema.sql") as file:
                await db.executescript(file.read())
            await db.commit()
        pass

    async def load_cogs(self) -> None:
        """
        The code in this function is executed whenever the bot will start.
        """
        for file in os.listdir(self.config["cogs_dir"]):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    self.logger.info(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(
                        f"Failed to load extension {extension}\n{exception}"
                    )

    @tasks.loop(minutes=5.0)
    async def status_task(self) -> None:
        """
        Setup the game status task of the bot.
        """
        # put this stuff in the database
        statuses = [
            "Alphonso Davies leave defenders in 2019!",
            "Jonathan David make goalkeepers cry!",
            "Tajon Buchanan send fullbacks to retirement!",
            "the USA wonder why Canada is better now!",
            "the CONCACAF refs ruin another match!",
            "Alphonso race a cheetah (and win)!",
            "Canada send Mexico to their winter coats!",
            "David outscore every ‘bigger’ nation!",
            "the USA call Canada ‘just lucky’ again!",
            "Borjan’s sweatpants win another game!",
            "Buchanan break ankles for fun!",
            "Davies make defenders question their life choices!",
            "Canada teach CONCACAF about real football!",
            "Costa Rica wonder when Canada got good!",
            "Davies turn a game into a track meet!",
            "Borjan stop shots like it’s his day job!",
            "the USA fans cope in real time!",
            "Canada silence the Azteca crowd!",
            "Mexico blame the altitude instead!",
            "Canadian players dominate in Europe!",
            "the USA claim dual-nationals as their own!",
            "David casually outscore CONCACAF legends!",
            "Canada own the ‘Kings of CONCACAF’ title!",
            "USA fans google ‘Canada’s soccer history’!",
            "Panama ask if it’s too late to switch regions!",
            "Canada break FIFA rankings again!",
            "Davies make defenders look like training cones!",
            "Borjan win games in sweatpants!",
            "the USA call it ‘a fluke’ for the 5th time!",
            "Buchanan do stepovers for fun!",
            "David ghost past defenses like a ninja!",
            "Mexico wonder what happened in 2021!",
            "Alphonso outrun Wi-Fi signals!",
            "USA fans realize Canada has real talent!",
            "Larin celebrate with a casual shrug!",
            "Canada become the true giants of CONCACAF!",
            "Canada qualify while others struggle!",
            "Davies make 99 pace look slow!",
            "Borjan collect another clean sheet!",
            "the USA wonder why their golden generation isn’t winning!",
            "Canada turn ‘underdog’ into ‘top dog’!",
            "David steal another Golden Boot race!",
            "Canada’s midfield run laps around the opposition!",
            "Davies delete fullbacks from existence!",
            "CONCACAF defenders have nightmares about Canada!",
            "the USA wish they had Alphonso Davies!",
            "David and Buchanan make defenders retire!",
            "Canada dunk on ‘bigger’ nations!",
            "the world finally respect Canadian soccer!",
            "Borjan’s sweatpants become legendary!",
            "Jesse Marsch turn Canada into a pressing machine!",
            "Eustáquio make midfield look easy!",
            "Larin casually score on every CONCACAF keeper!",
            "Johnston slide tackle his way through history!",
            "Jesse Marsch outcoach his former employers!",
            "Eustáquio ping 40-yard passes for fun!",
            "Larin become Canada's all-time top scorer!",
            "Johnston defend like his life depends on it!",
            "Jesse Marsch yell in three languages at once!",
            "Eustáquio be the midfield general we needed!",
            "Larin ghost into the box (again)!",
            "Johnston leave wingers in his back pocket!",
            "Eustáquio run the midfield like a CEO!",
            "Larin score while looking half-asleep!",
            "Johnston prove fullbacks can be cool!",
        ]

        await self.change_presence(
            activity=discord.Activity(
                name=random.choice(statuses), type=discord.ActivityType.watching
            )
        )

    @status_task.before_loop
    async def before_status_task(self) -> None:
        """
        Before starting the status changing task, we make sure the bot is ready
        """
        await self.wait_until_ready()

    async def setup_hook(self) -> None:
        """
        This will just be executed when the bot starts the first time.
        """
        assert self.user, "ERR in bot.py setup_hook(): self.user not available."
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(
            f"Running on: {platform.system()} {platform.release()} ({os.name})"
        )
        self.logger.info("-------------------")
        await self.init_db()
        await self.load_cogs()
        self.status_task.start()
        self.database = DatabaseManager(
            connection=await aiosqlite.connect(f"{self.config['db_dir']}/database.db")
        )

    async def on_message(self, message: discord.Message) -> None:
        """
        The code in this event is executed every time someone sends a message, with or without the prefix

        :param message: The message that was sent.
        """
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)

    async def on_command_completion(self, context: Context) -> None:
        """
        The code in this event is executed every time a normal command has been *successfully* executed.

        :param context: The context of the command that has been executed.
        """
        assert context.command, (
            "ERR in bot.py on_command_completion(): context.command not available."
        )
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        if context.guild is not None:
            self.logger.info(
                f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
            )
        else:
            self.logger.info(
                f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
            )

    async def on_command_error(self, context: Context, error) -> None:
        """
        The code in this event is executed every time a normal valid command catches an error.

        :param context: The context of the normal command that failed executing.
        :param error: The error that has been faced.
        """
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24

            parts = []
            if round(hours) > 0:
                parts.append(f"{round(hours)} hours")
            if round(minutes) > 0:
                parts.append(f"{round(minutes)} minutes")
            if round(seconds) > 0:
                parts.append(f"{round(seconds)} seconds")

            embed = discord.Embed(
                description=f"**Please slow down** - You can use this command again in {' '.join(parts)}.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                description="You are not the owner of the bot!", color=0xE02B2B
            )
            await context.send(embed=embed)
            if context.guild:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the guild {context.guild.name} (ID: {context.guild.id}), but the user is not an owner of the bot."
                )
            else:
                self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the bot's DMs, but the user is not an owner of the bot."
                )
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to execute this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description="I am missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to fully perform this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Error!",
                # We need to capitalize because the command arguments have no capital letter in the code and they are the first word in the error message.
                description=str(error).capitalize(),
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        else:
            raise error
