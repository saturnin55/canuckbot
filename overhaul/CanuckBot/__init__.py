from typing import Optional
from discord.ext.commands import Bot
from pydantic import BaseModel, root_validator
from database import DatabaseManager

class CanuckBotBase(BaseModel):
    obj: Optional[int] = None

    # Pydantic will automatically call this method, but you still need custom behavior
    # Override __init__ and call super().__init__ to ensure correct field initialization
    def __init__(self, bot: Bot, **kwargs):
        super().__init__(**kwargs)  # Pydantic initializes the fields
        self.bot = bot
        self.database: DatabaseManager = bot.database

    def print(self):
        for key, value in self.model_dump().items():
            print(f"{key}: {value}")

    # Optionally, you can add a root_validator if you need any additional validation
    @root_validator(pre=True)
    def check_fields(cls, values):
        # Add custom validation if needed
        return values

