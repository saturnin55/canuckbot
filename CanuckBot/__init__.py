import inspect
from typing import Any, Optional, get_type_hints, Type
from discord.ext.commands import Bot, Context
from pydantic import BaseModel, PrivateAttr, TypeAdapter, root_validator, HttpUrl
from database import DatabaseManager
from Discord.DiscordBot import DiscordBot
from CanuckBot.types import TimeZone, Handle, UnixTimestamp, HexColor
from Discord.types import DiscordChannelId, DiscordCategoryId, DiscordRoleId, DiscordUserId, SnowflakeId, DiscordChannelName
from Discord import Discord 


class CanuckBotBase(BaseModel):
    _bot: DiscordBot = PrivateAttr()
    _type_hints_cache = {}
    _adapters_cache = {}
    _discord_cache = PrivateAttr()

    # Pydantic will automatically call this method, but you still need custom behavior
    # Override __init__ and call super().__init__ to ensure correct field initialization
    def __init__(self, bot: DiscordBot, **kwargs):
        super().__init__(**kwargs)  # Pydantic initializes the fields
        self._bot = bot

        cls = self.__class__

        # Only initialize caches if this class hasn't already
        if cls not in self._type_hints_cache:
            # Merge hints from MRO
            full_hints = {}
            for base in cls.__mro__:
                if base is object:
                    continue
                try:
                    base_hints = get_type_hints(base)
                    for field, hint in base_hints.items():
                        # Only add fields that don't start with '_'
                        if not field.startswith('_'):
                            full_hints[field] = hint
                except Exception:
                    pass  # In case any base class has invalid or missing annotations

            self._type_hints_cache[cls] = full_hints

            # Precompute TypeAdapters
            for field, expected_type in full_hints.items():
                self._adapters_cache[(cls, field)] = TypeAdapter(expected_type)

    def print(self):
        for key, value in self.model_dump().items():
            print(f"{key}: {value}")

    # Optionally, you can add a root_validator if you need any additional validation
    @root_validator(pre=True)
    def check_fields(cls, values):
        # Add custom validation if needed
        return values

    def get_type(self, field: str) -> Optional[Type[Any]]:
        return self._type_hints_cache.get(self.__class__, {}).get(field)

    def cast_value(self, field: str, value: Any) -> Any:
        adapter = self._adapters_cache.get((self.__class__, field))
        if adapter:
            return adapter.validate_python(value)
        return None

    def is_type(self, field: str, expected_type: Type[Any]) -> bool:
        actual_type = self.get_type(field)
        return isinstance(actual_type, type) and issubclass(actual_type, expected_type)

#    def get_type(self, field):
#        hints = get_type_hints(self.__class__)
#        expected_type = hints.get(field)
#
#        if expected_type:
#            return expected_type
#        else:
#            # fixme
#            return None
#
#    def cast_value(self, field, value):
#        cast_value = None
#
#        # fixme: "cache" this data
#        hints = get_type_hints(self.__class__)
#        expected_type = hints.get(field)
#
#        if expected_type:
#            cast_value = TypeAdapter(expected_type).validate_python(value)
#        else:
#            # fixme
#            pass

        return cast_value

    async def get_attrval_str(self, context: Context, field: str = None) -> str | None:

        data = {}

        if field.startswith('_'):
            return None

                # types: int, str, UnixTimestamp, TimeZone, dict, List, DiscordUserId, DiscordChannelId, DiscordRoleId, DiscordCategoryId, HexColor, Handle, User_Level, Competition_Type, Match_Status

        # Get instance attributes directly from the instance's dictionary
        attributes = vars(self)

        #print(f"Attributes: {attributes}")
        #print(f"Field passed: {field}")

        # Check if the field is in attributes
        if field in attributes:
            try:
                value = getattr(self, field)
                # Handle the different types (DiscordChannelId, TimeZone, etc.)
                data = await self.handle_value_type(context, field, value)
                return data
            except Exception as e:
                print(f"Error retrieving attribute '{field}': {e}")
                pass

        return None

    async def handle_value_type(self, context: Context, field: str, value) -> str:
        """Helper function to handle different value types."""
        if field.endswith('channel_id'):
            return f"<#{value}>"
        elif field.endswith('role_id'):
            role = await Discord.get_role(context, int(value))
            return f"{role.name}"
        elif field.endswith('user_id') or fields.endswith('_by'):
            user  = await Discord.get_user(context, int(value))
            return f"{user.display_name}"
        elif field.endswith('category_id'):
            category  = await Discord.get_category(context, int(value))
            return f"{category.name}"
        elif field == "color" or field.endswith('_color'):
            return f"{value}"
        elif isinstance(value, int):
            return f"{str(value)}"
        elif isinstance(value, TimeZone):
            return f"{str(value.tz)}"
        elif isinstance(value, HttpUrl):
            return f"{str(value)}"
        elif isinstance(value, HexColor):
            return f"{str(value)}"
        elif isinstance(value, str):
            return f"{value}"
        else:
            return f"|{str(value)}|"

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
