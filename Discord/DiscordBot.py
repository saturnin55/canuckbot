"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.2.0
"""

import time
import logging
import os
import platform
import random

import aiosqlite
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context

from database import DatabaseManager
from Discord.LoggingFormatter import LoggingFormatter
from Discord.WebhookLoggerAdapter import WebhookLoggerAdapter
from Discord import LogTarget

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
        self, intents: discord.Intents, logger: WebhookLoggerAdapter, config: dict
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

        self.cleanup_task = tasks.loop(minutes=9999.0)(self._cleanup_task)
        self.status_task = tasks.loop(minutes=9999.0)(self._status_task)
        self.match_task = tasks.loop(minutes=9999.0)(self._match_task)

        @self.status_task.before_loop
        async def before_status_task() -> None:
            """
            Before starting the status changing task, we make sure the bot is ready
            """
            await self.wait_until_ready()

        @self.cleanup_task.before_loop
        async def before_cleanup_task() -> None:
            """
            Before starting the cleanup changing task, we make sure the bot is ready
            """
            await self.wait_until_ready()

        @self.match_task.before_loop
        async def before_match_task() -> None:
            """
            Before starting the match changing task, we make sure the bot is ready
            """
            await self.wait_until_ready()


    async def init_db(self, db_file: str = None) -> None:
        os.environ["DB_PATH"] = f"{self.config['db_dir']}/database.db"
        return

    async def load_cogs(self) -> None:

        self.cleanup_task.start()
        self.status_task.start()
        self.match_task.start()

        """
        The code in this function is executed whenever the bot will start.
        """
        for file in os.listdir(self.config["cogs_dir"]):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    await self.logger.debug(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    await self.logger.error(
                        f"Failed to load extension {extension}\n{exception}", target=LogTarget.BOTH
                    )
        await self.logger.info(f"{self.user.name} started!", target=LogTarget.BOTH)

    async def _cleanup_task(self) -> None:
        """
        Clean the canuckbot cache
        """
        await self.database.delete("DELETE FROM canuckbot_cache WHERE expiration < CURRENT_TIMESTAMP")
        await self.logger.debug("Cleanup tasks executed.", target=LogTarget.BOTH)


    async def _status_task(self) -> None:
        """
        Setup the game status task of the bot.
        """
        # select a random bot status from the database
        row = await self.database.get_one("SELECT status FROM bot_statuses ORDER BY RANDOM() LIMIT 1", []);
        status = row["status"]
 
        await self.change_presence(
            activity=discord.Activity(
                name=status, type=discord.ActivityType.watching
            )
        )
        await self.logger.debug(f"{self.user.name} status changed to : `{status}`", target=LogTarget.BOTH)

    async def _match_task(self) -> None:
        """
        Setup matches and channels
        """
        await self.logger.debug(f"Match tasks executed", target=LogTarget.BOTH)
        pass

    async def setup_hook(self) -> None:
        """
        This will just be executed when the bot starts the first time.
        """
        assert self.user, "ERR in bot.py setup_hook(): self.user not available."
        await self.logger.info(f"Logged in as {self.user.name}")
        await self.logger.info(f"discord.py API version: {discord.__version__}")
        await self.logger.info(f"Python version: {platform.python_version()}")
        await self.logger.info(
            f"Running on: {platform.system()} {platform.release()} ({os.name})"
        )
        await self.logger.info("-------------------")
        await self.init_db(f"{self.config['db_dir']}/database.db")
        await self.load_cogs()
        self.database = DatabaseManager(
            connection=await aiosqlite.connect(f"{self.config['db_dir']}/database.db")
        )

        rows = await self.database.select("SELECT field, value FROM config WHERE field like 'interval_%'")
        if not rows or len(rows) < 3:
            #fixme
            pass
        else:
            for row in rows:
                self.config[row['field']] = float(row['value'])
 
        if not self.cleanup_task.is_running():
            self.cleanup_task.start()
        self.cleanup_task.change_interval(minutes=float(self.config['interval_cleanup_task']))

        if not self.status_task.is_running():
            self.status_task.start()
        self.status_task.change_interval(minutes=float(self.config['interval_status_task']))

        if not self.match_task.is_running():
            self.match_task.start()
        self.match_task.change_interval(minutes=float(self.config['interval_match_task']))

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
        if context.interaction:
            data = context.interaction.data
            name = data.get("name")
            options = data.get("options", [])

            def format_options(opts):
                return " ".join(
                    f"{opt['name']}:{opt['value']}" if "value" in opt else opt["name"]
                    for opt in opts
                )

            args_str = format_options(options)
            _cmd = f"/{name} {args_str}"
        else:
            _cmd = context.message.content
            
        if context.guild is not None:
            await self.logger.cmds(_cmd, context, target=LogTarget.BOTH)
        else:
            await self.logger.cmds(_cmd, context, target=LogTarget.BOTH)

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
                await self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the guild {context.guild.name} (ID: {context.guild.id}), but the user is not an owner of the bot.", target=LogTarget.BOTH
                )
            else:
                await self.logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the bot's DMs, but the user is not an owner of the bot.", target=LogTarget.BOTH
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
