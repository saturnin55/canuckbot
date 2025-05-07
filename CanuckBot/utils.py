import re
from datetime import datetime
from discord.ext.commands import Context, Bot

import discord
import validators

#from CanuckBot import ctx
from CanuckBot.constants import (
    TYPE_BOOL,
    TYPE_COLOR,
    TYPE_DISCORD_CATEGORYID,
    TYPE_DISCORD_CHANNELID,
    TYPE_DISCORD_MESSAGEID,
    TYPE_DISCORD_ROLEID,
    TYPE_DISCORD_USERID,
    TYPE_INT,
    TYPE_STRING,
    TYPE_TIMESTAMP,
    TYPE_URL,
)


def timestamp2str(t, format="%Y-%m-%d %H:%M"):
    return datetime.fromtimestamp(t).strftime(format)


def key_value_exists(data_list, key, value):
    """
    Checks if a specific key-value pair exists in the list of dictionaries.

    :param data_list: List of dictionaries.
    :param key: The key to search for.
    :param value: The value to match.
    :return: True if found, otherwise False.
    """
    return any(entry.get(key) == value for entry in data_list)


def is_valid_type(_type, value) -> bool:
    if _type == TYPE_INT:
        return is_integer(value) or value is None
    elif _type == TYPE_STRING:
        return is_string(value)
    elif _type == TYPE_BOOL:
        return is_bool(value)
    elif _type == TYPE_TIMESTAMP:
        return is_timestamp(value) or value is None
    elif _type == TYPE_URL:
        return is_url(value) or value is None
    elif _type in [
        TYPE_DISCORD_USERID,
        TYPE_DISCORD_CHANNELID,
        TYPE_DISCORD_CATEGORYID,
        TYPE_DISCORD_ROLEID,
        TYPE_DISCORD_MESSAGEID,
    ]:
        return is_snowflakeid(value) or value is None
    elif _type == TYPE_COLOR:
        return is_hex_color(value) or value is None
    else:
        return False

    return False


def is_hex_color(value):
    return isinstance(value, str) and bool(re.fullmatch(r"0x[0-9A-Fa-f]{6}", value))


def is_url(value):
    if value is None:
        return True
    else:
        return validators.url(value)


def is_timestamp(value):
    if not isinstance(value, int):  # Ensure it's an integer
        return False

    # Define reasonable Unix timestamp range (1970 to 2100)
    min_timestamp = 0  # 1970-01-01 00:00:00 UTC
    max_timestamp = 4102444800  # 2100-01-01 00:00:00 UTC

    return min_timestamp <= value <= max_timestamp


def is_bool(value):
    return type(value) is bool or value in [0, 1]


def is_integer(value):
    print(type(value))
    return type(value) is int


def is_string(value):
    return isinstance(value, str)


def is_snowflakeid(value):
    return isinstance(value, int) and 17 <= len(str(value)) <= 19


def get_field_value(_type, value) -> int | str | bool:
    if _type == TYPE_INT:
        return int(value)
    elif _type == TYPE_STRING:
        return str(value)
    elif _type == TYPE_BOOL:
        return bool(value)
    elif _type == TYPE_TIMESTAMP:
        return int(value)
    elif _type == TYPE_URL:
        return str(value)
    elif _type in [
        TYPE_DISCORD_USERID,
        TYPE_DISCORD_CHANNELID,
        TYPE_DISCORD_CATEGORYID,
        TYPE_DISCORD_ROLEID,
        TYPE_DISCORD_MESSAGEID,
    ]:
        return int(extract_snowflake(value))
    elif _type == TYPE_COLOR:
        return str(value)
    else:
        return False


def regex_is_integer(value: str) -> bool:
    pattern = r"^\d+$"
    return re.match(pattern, value) is not None


def pp_discord_channel(channel) -> str:
    if channel is None:
        return "—"
    else:
        return f"<#{channel.id}>"


def pp_discord_category(category) -> str:
    if category is None:
        return "—"
    else:
        return f"*{category.name}*"


def pp_hex_color(color) -> str:
    if color is None:
        return "—"
    else:
        return f"{color}"


def pp_discord_role(role) -> str:
    print(f"yoooo |{role}|")
    if role is None:
        return "—"
    else:
        return f"<@&{role.id}>"


def pp_discord_user(user) -> str:
    if user is None:
        return "—"
    else:
        return f"<@{user.id}>"


def pp_bool(value) -> str:
    if value:
        return "yes"
    else:
        return "no"


def pp_url(url) -> str:
    if url is None:
        return "—"
    else:
        return f"<{url}>"


def pp_timestamp(t) -> str:
    if t is None:
        return "—"
    else:
        return timestamp2str(int(t))


def pp_int(value) -> str:
    if value is None:
        return "—"
    else:
        return value


def pp_string(value) -> str:
    if value is None:
        return "—"
    else:
        return value


def extract_snowflake(mention: str) -> str:
    if mention.startswith("<@&") and mention.endswith(">"):
        return mention[3:-1]
    elif mention.startswith("<@") and mention.endswith(">"):
        return mention[2:-1]
    elif mention.startswith("<#") and mention.endswith(">"):
        return mention[2:-1]
    return mention


def get_type_name(c):
    if c == TYPE_INT:
        return "int"
    elif c == TYPE_BOOL:
        return "bool"
    elif c == TYPE_STRING:
        return "string"
    elif c == TYPE_TIMESTAMP:
        return "timestamp"
    elif c == TYPE_URL:
        return "url"
    elif c == TYPE_DISCORD_USERID:
        return "userid"
    elif c == TYPE_DISCORD_CHANNELID:
        return "channelid"
    elif c == TYPE_DISCORD_CATEGORYID:
        return "categoryid"
    elif c == TYPE_DISCORD_ROLEID:
        return "roleid"
    elif c == TYPE_DISCORD_MESSAGEID:
        return "messageid"
    elif c == TYPE_COLOR:
        return "color"
    else:
        return f"unknown ({c})"
