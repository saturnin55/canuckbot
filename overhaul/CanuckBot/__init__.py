from typing import Optional

from discord.ext.commands import Bot
from pydantic import BaseModel

from database import DatabaseManager


class CanuckBotBase(BaseModel):
    obj: Optional[int] = None

    def __init__(self, bot: Bot):
        self.bot = bot
        self.database: DatabaseManager = bot.database

    def print(self):
        for key, value in self.model_dump().items():
            print(f"{key}: {value}")
