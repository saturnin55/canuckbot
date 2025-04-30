from pydantic import BaseModel
from typing import Optional

class CanuckBotBase(BaseModel):
    obj: Optional[int] = None

    def __init__(self, bot):
        self.bot = bot
        self.database = bot.database

    def print(self):
        for key, value in self.model_dump().items():
            print(f"{key}: {value}")
