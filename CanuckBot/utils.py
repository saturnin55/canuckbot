import re
import hashlib
import requests
from io import BytesIO
from CanuckBot.Cache import Cache
from CanuckBot.types import HANDLE_PATTERN
from colorthief import ColorThief
from database import DatabaseManager
from discord.ext.commands import Context
from Discord.DiscordBot import DiscordBot
from typing import List
from CanuckBot.Config import Config

def md5_hash(text: str):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def _is_near_white_or_black(rgb: tuple, white_threshold: int = 240, black_threshold: int = 15) -> bool:
    r, g, b = rgb
    # White-ish if all components are high
    if r >= white_threshold and g >= white_threshold and b >= white_threshold:
        return True
    # Black-ish if all components are low
    if r <= black_threshold and g <= black_threshold and b <= black_threshold:
        return True
    return False

async def get_dominant_color_from_url(db: DatabaseManager = None, image_url: str = None) -> int:
    if not db or not image_url:
        return 0xffffff

    key = md5_hash(image_url)

    cache = Cache(db)
    color = await cache.retrieve(key)

    if color:
        return int(color)

    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image_file = BytesIO(response.content)

        color_thief = ColorThief(image_file)
        palette = color_thief.get_palette(color_count=6, quality=1)

        # Find the first non-white-ish color in the palette
        for r, g, b in palette:
            if not _is_near_white_or_black((r, g, b)):
                color = (r << 16) + (g << 8) + b
                await cache.store(key, str(color))
                return color

        # If all colors are white-ish, fallback
        return 0xffffff

    except Exception:
        return 0xffffff


def is_valid_handle(s):
    return re.match(HANDLE_PATTERN, s) is not None


async def validate_invoking_channel(bot:DiscordBot = None, context:Context = None, more_channels: List[int] = None) -> bool:

    config = await Config.create(bot)

    allowed_channels = []
    allowed_channels.append(config.cmds_channel_id)
    if more_channels:
        allowed_channels.extend(more_channels)

    if context.channel.id in allowed_channels:
        return True
    else:
        return False


# from an internval in the form of 3,55-8,10 ; return a list of integer
def parse_number_string(s: str) -> list[int]:
    result = set()
    parts = s.replace(" ", "").split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            result.update(range(min(start, end), max(start, end) + 1))
        else:
            result.add(int(part))
    return sorted(result)

