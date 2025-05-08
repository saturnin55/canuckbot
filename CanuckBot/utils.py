import hashlib
import requests
from io import BytesIO
from CanuckBot.Cache import Cache
from colorthief import ColorThief
from database import DatabaseManager

def md5_hash(text: str):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

async def get_dominant_color_from_url(db: DatabaseManager = None, image_url: str = None) -> int:

    if not db or not image_url:
        return 0xffffff

    key = md5_hash(image_url)

    cache = Cache(db)
    color = await cache.retrieve(key)

    if color:
        #print(f"{image_url}|{key}|cached")
        return int(color)

    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise error for bad responses
        image_file = BytesIO(response.content)

        color_thief = ColorThief(image_file)
        r, g, b = color_thief.get_color(quality=1)

        color = (r << 16) + (g << 8) + b
        
        await cache.store(key, str(color))
        #print(f"{image_url}|{key}|fetched")

        return color

    except Exception as e:
        return 0xffffff
