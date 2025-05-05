from typing import Any, Optional, get_type_hints

from discord.ext.commands import Bot, Context
from pydantic import BaseModel, PrivateAttr, TypeAdapter, root_validator

from database import DatabaseManager

# from bot import DiscordBot
from DiscordBot.DiscordBot import DiscordBot


class CanuckBotBase(BaseModel):
    _bot: DiscordBot

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

    def get_property_str(self, field: str = None) -> dict:
        if field.startswith('_'):
            return None

        attr = getattr(type(self), field, None)

        if isinstance(attr, property):
            try:
                value = getattr(self, attr_name)
                #fixme deal with possible types
            except Exception as e:
                #fixme
                pass

        return None

    def get_properties_str(self) -> dict:

        data = {}

        for attr_name in dir(self):
            # Filter out private/protected attributes and methods
            if attr_name.startswith('_'):
                continue

            attr = getattr(type(self), attr_name, None)

            if isinstance(attr, property):
                try:
                    value = getattr(self, attr_name)
                    #fixme deal with possible types
                    # types: int, str, UnixTimestamp, TimeZone, dict, List, DiscordUserId, DiscordChannelId, DiscordRoleId, DiscordCategoryId, HexColor, Handle, User_Level, Competition_Type, Match_Status

                    data[field] = value
                except Exception as e:
                    #fixme
                    pass
        return data
