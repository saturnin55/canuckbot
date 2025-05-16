import logging
from discord import Member, User
from discord.ext.commands import Context

class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)

    @staticmethod
    def format_invoked_slash_cmd(cmd: str, context: Context) -> str:
        if context.interaction:
            channel = context.interaction.channel.name
            channel_id = context.interaction.channel.id
        elif context.channel:   
            channel = context.channel.name
            channel_id = context.channel.id
        else:
            channel = "DM"
            channel_id = "-"

        if context.kwargs:
            args = " ".join(f"{k}='{v}'" for k, v in context.kwargs.items() if v is not None)
            cmd = f"{cmd} {args}"

        return f"{LoggingFormatter.blue}{LoggingFormatter.bold}{cmd}{LoggingFormatter.reset} by {LoggingFormatter.green}{context.author}{LoggingFormatter.reset} (ID: {context.author.id}) in #{channel} (ID: {channel_id})"
