import re
import time
import discord
import validators
from datetime import datetime
from discord.ext.commands import Context
from Discord.DiscordBot import DiscordBot
from database import DatabaseManager
from CanuckBot.types import DiscordCategoryId, SnowflakeId
from typing import Any
from Discord.DiscordCache import DiscordCache

#@staticmethod
#async def get_discord_role(ctx: Context, bot: DiscordBot, roleid: DiscordRoleId) -> discord.Role | None:

@staticmethod
async def get_discord_category(ctx: Context, bot: DiscordBot, categoryid: DiscordCategoryId) -> discord.CategoryChannel | None:
    categoryid = int(categoryid)


    # check if we have a valid entry in the cache
    cache = DiscordCache(bot.database, bot.cache["cache_expire_offset"])
    cacheobj = cache.retrieve(SnowflakeId(categoryid))
    if cacheobj:
        return cacheobj["name"]
    else:
        # else we fetch it via discord api
        category = discord.utils.get(context.guild.categories, id=categoryid)

        if not category:
            try:
                # Fetch from API if not in cache
                category = await context.guild.fetch_channel(categoryid)
                if not isinstance(category, discord.CategoryChannel):
                    #fixme
                    #await ctx.send(f"ERR[not_a_category: {categoryid}]")
                    return None
            except discord.NotFound:
                #fixme
                #await ctx.send(f"ERR[not_found: {categoryid}]")
                return None
            except discord.Forbidden:
                #fixme
                #await ctx.send(f"ERR[Forbidden: {categoryid}]")
                return None

        cache.store(SnowflakeId(categoryid), category.name)

        return category.name
