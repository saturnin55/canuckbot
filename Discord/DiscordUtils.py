import re
import json
import time
import discord
import validators
from datetime import datetime
from discord.ext.commands import Context
from Discord.DiscordBot import DiscordBot
from database import DatabaseManager
from CanuckBot.types import DiscordCategoryId, SnowflakeId, DiscordRoleId, DiscordUserId, DiscordChannelId
from typing import Any
from Discord.DiscordCache import DiscordCache

#@staticmethod
#async def get_discord_role(ctx: Context, bot: DiscordBot, roleid: DiscordRoleId) -> discord.Role | None:


class DiscordUtils:

    @staticmethod
    async def get_channel(context: Context, bot: DiscordBot, userid: DiscordChannelId) -> str | None:
        channelid = int(channelid)

        # check if we have a valid entry in the cache
        cache = DiscordCache(bot.database, bot.config["cache_expire_offset"])
        cacheobj = await cache.retrieve(SnowflakeId(userid))
        if cacheobj:
            return json.loads(cacheobj["data"])
        else:
            # else we fetch it via discord api

            channel = bot.get_channel(channel_id)  # Try to get the channel from cache
            if not channel:
                try:
                    # Fetch from API if not in cache
                    channel = await bot.fetch_channel(channel_id)
                except discord.NotFound:
                    return None  # Channel does not exist
                except discord.Forbidden:
                    #return "Permission Denied"  # Bot lacks permissions
                    return None  # Channel does not exist

                data = { "object": "channel",
                        "id": channel.id,
                        "name": channel.name,
                        "guild_id": channel.guild.id,
                        "guild_name": channel.guild.name,
                        "mention": channel.mention }
                await cache.store(SnowflakeId(channelid), json.dumps(data))
        
                return data
        return None


    @staticmethod
    async def get_user(context: Context, bot: DiscordBot, userid: DiscordUserId) -> str | None:
        userid = int(userid)

        # check if we have a valid entry in the cache
        cache = DiscordCache(bot.database, bot.config["cache_expire_offset"])
        cacheobj = await cache.retrieve(SnowflakeId(userid))
        if cacheobj:
            return json.loads(cacheobj["data"])
        else:
            # else we fetch it via discord api
            try:
                user = ctx.guild.get_member(userid) or await bot.fetch_user(userid)
            except:
                return None

            if not user:
                return None
    
            data = { "object": "user",
                    "id": user.id,
                    "name": user.name,
                    "discriminator": user.discriminator,
                    "display_name": user.display_name,
                    "global_name": user.global_name,
                    "avatar_url": user.avatar.url.name,
                    "mention": user.mention,
                    "bot": user.bot
                     }
            await cache.store(SnowflakeId(userid), json.dumps(data))
        
            return data
        return None

    @staticmethod
    async def get_role(context: Context, bot: DiscordBot, roleid: DiscordRoleId) -> str | None:
        roleid = int(roleid)

        # check if we have a valid entry in the cache
        cache = DiscordCache(bot.database, bot.config["cache_expire_offset"])
        cacheobj = await cache.retrieve(SnowflakeId(roleid))
        if cacheobj:
            return json.loads(cacheobj["data"])
        else:
            # else we fetch it via discord api
            role = context.guild.get_role(roleid)
            if not role:
                # If not in cache, fetch roles from API
                try:
                    roles = await context.guild.fetch_roles()  # Fetch all roles
                    role = discord.utils.get(roles, id=roleid)  # Find role in fetched list
                except discord.HTTPException as e:
                    #fixme
                    #print(f"Failed to fetch role : {e}")
                    return None  # Return None if role fetch fails

            data = { "object": "role",
                    "id": role.id,
                    "name": role.name,
                    "guild_id": role.guild.id,
                    "color": str(role.color),
                    "mention": role.mention
                     }
            await cache.store(SnowflakeId(roleid), json.dumps(data))

            return data
        return None
        

    @staticmethod
    async def get_category(context: Context, bot: DiscordBot, categoryid: DiscordCategoryId) -> str | None:
        categoryid = int(categoryid)


        # check if we have a valid entry in the cache
        cache = DiscordCache(bot.database, bot.config["cache_expire_offset"])
        cacheobj = await cache.retrieve(SnowflakeId(categoryid))
        if cacheobj:
            return json.loads(cacheobj["data"])
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

            data = { "object": "category",
                    "id": category.id,
                    "name": category.name,
                    "guild_id": category.guild.id,
                    "guild_name": category.guild.name,
                    "mention": category.mention }
            await cache.store(SnowflakeId(categoryid), json.dumps(data))

            return data
        return None
