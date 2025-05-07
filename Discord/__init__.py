from typing import Optional
import discord
from discord.ext import commands

class Discord:

    @staticmethod
    async def get_role(ctx: commands.Context, role_id: int) -> Optional[discord.Role]:
        """
        Gets a role by ID using cache only (API fetch is not available for roles).

        Returns:
            Optional[discord.Role]: Role object or None if not found or on error.
        """
        if ctx.guild is None:
            return None
        try:
            role = ctx.guild.get_role(role_id)
            if isinstance(role, discord.Role):
                return role
        except Exception:
            pass

        return None

    @staticmethod
    async def get_channel(ctx: commands.Context, channel_id: int) -> Optional[discord.abc.GuildChannel]:
        """
        Gets a channel by ID using cache first, falling back to API fetch.

        Returns:
            Optional[discord.abc.GuildChannel]: The channel object or None.
        """
        if ctx.guild is None:
            return None

        channel = ctx.guild.get_channel(channel_id)
        if channel is not None:
            return channel

        try:
            channel = await ctx.guild.fetch_channel(channel_id)
            if isinstance(channel, discord.GuildChannel):
                return channel
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            pass

        return None

    @staticmethod
    async def get_category(ctx: commands.Context, category_id: int) -> Optional[discord.CategoryChannel]:
        """
        Gets a category channel by ID using cache first, falling back to API fetch.

        Returns:
            Optional[discord.CategoryChannel]: The category channel or None.
        """
        if ctx.guild is None:
            return None

        channel = ctx.guild.get_channel(category_id)
        if isinstance(channel, discord.CategoryChannel):
            return channel

        try:
            channel = await ctx.guild.fetch_channel(category_id)
            if isinstance(channel, discord.CategoryChannel):
                return channel
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            pass

        return None


    @staticmethod
    async def get_message(ctx: commands.Context, channel: discord.TextChannel, message_id: int) -> Optional[discord.Message]:
        """
        Fetches a message by ID from a specific text channel using the API.

        Returns:
            Optional[discord.Message]: The message object or None.
        """
        try:
            message =  await channel.fetch_message(message_id)
            if isinstance(message, discord.Message):
                return message
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            pass

        return None

    @staticmethod
    async def get_guild(ctx: commands.Context, guild_id: int) -> Optional[discord.Guild]:
        """
        Gets a guild by ID using the bot's cache only.

        Returns:
            Optional[discord.Guild]: The guild object or None.
        """
        bot = ctx.bot
        if bot is None:
            return None

        guild = bot.get_guild(guild_id)
        if isinstance(guild, discord.Guild):
            return guild

        return None


    @staticmethod
    async def get_member(ctx: commands.Context, member_id: int) -> Optional[discord.Member]:
        """
        Fetches a member by ID using the cache first, falling back to API fetch if not found.

        Returns:
            Optional[discord.Member]: The member object or None.
        """
        if ctx.guild is None:
            return None

        member = ctx.guild.get_member(member_id)
        if member is not None:
            return member

        try:
            member = await ctx.guild.fetch_member(member_id)
            if isinstance(member, discord.Member):
                return member
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            pass

        return None

    @staticmethod
    async def get_user(ctx: commands.Context, user_id: int) -> Optional[discord.User]:
        """
        Fetches a user globally by ID, first checking the cache, then falling back to API fetch.

        Returns:
            Optional[discord.User]: The user object or None.
        """
        user = ctx.bot.get_user(user_id)
        if user is not None:
            return user
        try:
            user = await ctx.bot.fetch_user(user_id)
            if isinstance(user, discord.User):
                return user
        except (discord.NotFound, discord.Forbidden, discord.HTTPException):
            pass

        return None


    @staticmethod
    async def get_user_or_member(ctx: commands.Context, user_id: int) -> Optional[discord.abc.User]:
        """
        Attempts to get a user object by ID. First tries to fetch the user from the guild's members (if in cache),
        falling back to a global user lookup if not found.

        Returns:
            Optional[discord.abc.User]: The user object (either Member or User) or None if not found.
        """
        # First, try to fetch the user as a member of the guild
        member = await Discord.get_member(ctx, user_id)
        if member:
            return member

        # If not found as a member, try to fetch the user globally
        try:
            user = await Discord.get_user(ctx, user_id)
            if user is not None:
                return user
        except:
            pass

        return None
