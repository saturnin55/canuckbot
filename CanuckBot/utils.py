import requests
from io import BytesIO
from colorthief import ColorThief

def get_dominant_color_from_url(image_url: str) -> int:
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise error for bad responses
        image_file = BytesIO(response.content)

        color_thief = ColorThief(image_file)
        r, g, b = color_thief.get_color(quality=1)
        return (r << 16) + (g << 8) + b
    except Exception as e:
        return 0xffffff
