from typing import Any, Optional, get_type_hints

from discord.ext.commands import Bot, Context
from pydantic import BaseModel, PrivateAttr, TypeAdapter, root_validator

# from bot import DiscordBot
from database import DatabaseManager


class CanuckBotBase(BaseModel):
    _bot: Any

    # Pydantic will automatically call this method, but you still need custom behavior
    # Override __init__ and call super().__init__ to ensure correct field initialization
    def __init__(self, bot, **kwargs):
        super().__init__(**kwargs)  # Pydantic initializes the fields
        self._bot = bot

    def print(self):
        for key, value in self.model_dump().items():
            print(f"{key}: {value}")

    # Optionally, you can add a root_validator if you need any additional validation
    @root_validator(pre=True)
    def check_fields(cls, values):
        # Add custom validation if needed
        return values

    def get_type(self, field):
        hints = get_type_hints(self.__class__)
        expected_type = hints.get(field)

        if expected_type:
            return expected_type
        else:
            # fixme
            return None

    def cast_value(self, field, value):
        cast_value = None

        # fixme: "cache" this data
        hints = get_type_hints(self.__class__)
        expected_type = hints.get(field)

        if expected_type:
            cast_value = TypeAdapter(expected_type).validate_python(value)
        else:
            # fixme
            pass

        return cast_value
