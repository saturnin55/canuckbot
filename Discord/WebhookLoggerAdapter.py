import logging
import aiohttp
from Discord import LogTarget
from discord.ext.commands import Context
import discord
from datetime import datetime
from zoneinfo import ZoneInfo
from Discord.LoggingFormatter import LoggingFormatter

class WebhookLoggerAdapter:
    def __init__(self, logger: logging.Logger, webhook_url: str = None):
        self.logger = logger
        self.webhook_url = webhook_url

    async def _send_webhook(self, embed: discord.Embed = None):
        if not self.webhook_url or not embed:
            return

        local_zone = ZoneInfo("America/Toronto")  # Replace with your local zone
        local_time = datetime.now(local_zone)
        embed.set_footer(text=f"{local_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

        _embed = embed.to_dict()

        data = {}
        if _embed:
            data["embeds"] = [_embed]
            # Optionally include content along with embed
        else:
            # Nothing to send
            return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=data) as resp:
                    if resp.status >= 400:
                        self.logger.warning(f"Webhook failed: {resp.status} {await resp.text()}")
        except Exception as e:
            self.logger.warning(f"Exception during webhook send: {e}")


    async def cmds(self, cmd: str, context: Context, target:LogTarget = LogTarget.LOGGER_ONLY, **kwargs):
        
        if self.logger.getEffectiveLevel() > logging.INFO:
            return

        if target in [LogTarget.LOGGER_ONLY, LogTarget.BOTH]:
            self.logger.info(LoggingFormatter.format_invoked_slash_cmd(f"{cmd}", context))

        if target in [LogTarget.WEBHOOK_ONLY, LogTarget.BOTH]:
            if context.interaction:
                channel = f"#{context.interaction.channel.name}"
                channel_id = context.interaction.channel.id
            elif context.channel:
                channel = f"#{context.channel.name}"
                channel_id = context.channel.id
            else:
                channel = "DM"
                channel_id = "-"

            if context.kwargs:
                args = " ".join(f"{k}='{v}'" for k, v in context.kwargs.items() if v is not None)
                cmd = f"{cmd} {args}"
            
            embed = discord.Embed(color=int(0x4CAF50))
            embed.set_author(name=f"{context.author.name} [{context.author.id}]", icon_url=context.author.avatar.url)
            embed.add_field(name="", value=cmd, inline=False)
            embed.add_field(name="", value=f"{channel} [{channel_id}]", inline=False)

            await self._send_webhook(embed)


    async def info(self, message: str, *args, target:LogTarget = LogTarget.LOGGER_ONLY, **kwargs):
        if target in [LogTarget.LOGGER_ONLY, LogTarget.BOTH]:
            self.logger.info(message, *args, **kwargs)

        if target in [LogTarget.WEBHOOK_ONLY, LogTarget.BOTH]:
            embed = discord.Embed(color=int(0x4CAF50), description=message)
            await self._send_webhook(embed)


    async def error(self, message: str, *args, target:LogTarget = LogTarget.LOGGER_ONLY, **kwargs):

        if self.logger.getEffectiveLevel() > logging.ERROR:
            return

        if target in [LogTarget.LOGGER_ONLY, LogTarget.BOTH]:
            self.logger.error(message, *args, **kwargs)

        if target in [LogTarget.WEBHOOK_ONLY, LogTarget.BOTH]:
            embed = discord.Embed(color=int(0xF44336), description=message)
            await self._send_webhook(embed)


    async def warning(self, message: str, *args, target:LogTarget = LogTarget.LOGGER_ONLY, **kwargs):

        if self.logger.getEffectiveLevel() > logging.WARNING:
            return

        if target in [LogTarget.LOGGER_ONLY, LogTarget.BOTH]:
            self.logger.warning(message, *args, **kwargs)

        if target in [LogTarget.WEBHOOK_ONLY, LogTarget.BOTH]:
            embed = discord.Embed(color=int(0xFFC107), description=message)
            await self._send_webhook(embed)


    async def debug(self, message: str, *args, target:LogTarget = LogTarget.LOGGER_ONLY, **kwargs):

        if self.logger.getEffectiveLevel() > logging.DEBUG:
            return

        if target in [LogTarget.LOGGER_ONLY, LogTarget.BOTH]:
            self.logger.debug(message, *args, **kwargs)

        if target in [LogTarget.WEBHOOK_ONLY, LogTarget.BOTH]:
            embed = discord.Embed(color=int(0x9E9E9E), description=message)
            await self._send_webhook(embed)


    async def critical(self, message: str, *args, target:LogTarget = LogTarget.LOGGER_ONLY, **kwargs):

        if self.logger.getEffectiveLevel() > logging.CRITICAL:
            return

        if target in [LogTarget.LOGGER_ONLY, LogTarget.BOTH]:
            self.logger.critical(message, *args, **kwargs)

        if target in [LogTarget.WEBHOOK_ONLY, LogTarget.BOTH]:
            embed = discord.Embed(color=int(0xD50000), description=message)
            await self._send_webhook(embed)


    # Delegate useful logger methods
    def setLevel(self, level):
        self.logger.setLevel(level)

    def addHandler(self, handler):
        self.logger.addHandler(handler)

    def removeHandler(self, handler):
        self.logger.removeHandler(handler)

    def getEffectiveLevel(self):
        return self.logger.getEffectiveLevel()

    def isEnabledFor(self, level):
        return self.logger.isEnabledFor(level)

