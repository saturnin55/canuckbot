import os
import sqlite3
from typing import Optional, Union
import discord
from discord.ext import commands
from discord.ext.commands import Context

class Color:
    Success = int(0x28a745)
    Warning = int(0xffa500)
    Error = int(0xE02B2B)
    Neutral = int(0xffffff)

class LogTarget:
    LOGGER_ONLY = 1
    WEBHOOK_ONLY = 2
    BOTH = 3

class Discord:

    @staticmethod
    async def join_role(guild: discord.Guild, user_id: int, role_identifier: Union[int, str], reason: Optional[str] = None) -> bool:
        """
        Adds a role to a user by role name or ID.

        Args:
            guild (discord.Guild): The guild where the role and user exist.
            user_id (int): The user's Discord ID.
            role_identifier (Union[int, str]): The role ID or role name.

        Returns:
            bool: True if the role was added, False otherwise.
        """
        try:
            member: discord.Member = await guild.fetch_member(user_id)
        except (discord.NotFound, discord.HTTPException):
            return False

        # Find the role by ID or name
        if isinstance(role_identifier, int):
            role = guild.get_role(role_identifier)
        else:
            role = discord.utils.get(guild.roles, name=role_identifier)

        if role is None:
            return False

        if role in member.roles:
            return False  # Already has the role

        try:
            await member.add_roles(role, reason=reason[:512])
            return True
        except discord.Forbidden:
            return False  # Missing permissions
        except discord.HTTPException:
            return False  # Discord API error


    @staticmethod
    async def is_member_of_role(guild: discord.Guild, user_id: int, role_identifier: Union[int, str]) -> bool:
        """
        Checks if a member has a specific role by name or ID.

        Args:
            guild (discord.Guild): The guild to search in.
            user_id (int): The Discord user ID of the member.
            role_identifier (Union[int, str]): The role ID (int) or name (str).

        Returns:
            bool: True if the user has the role, False otherwise.
        """
        try:
            member: discord.Member = await guild.fetch_member(user_id)
        except discord.NotFound:
            return False
        except discord.HTTPException:
            return False

        # Determine the role by name or ID
        if isinstance(role_identifier, int):
            role = guild.get_role(role_identifier)
        else:
            role = discord.utils.get(guild.roles, name=role_identifier)

        if role is None:
            return False

        return role in member.roles


    @staticmethod
    async def leave_role(guild: discord.Guild, user_id: int, role_identifier: Union[int, str], reason: Optional[str] = None) -> bool:
        """
        Removes a role from a user by role name or ID.

        Args:
            guild (discord.Guild): The guild where the role and user exist.
            user_id (int): The user's Discord ID.
            role_identifier (Union[int, str]): The role ID or role name.

        Returns:
            bool: True if role was removed, False if not (e.g., role/user not found).
        """
        try:
            member: discord.Member = await guild.fetch_member(user_id)
        except (discord.NotFound, discord.HTTPException):
            return False

        # Find the role by ID or name
        if isinstance(role_identifier, int):
            role = guild.get_role(role_identifier)
        else:
            role = discord.utils.get(guild.roles, name=role_identifier)

        if role is None:
            return False

        if role not in member.roles:
            return False  # Role already not assigned

        try:
            await member.remove_roles(role, reason=reason[:512])
            return True
        except discord.Forbidden:
            return False  # Missing permissions
        except discord.HTTPException:
            return False  # Discord API error


    @staticmethod
    async def delete_role(context: commands.Context, role_id: int, *, reason: Optional[str] = None) -> bool:
        """
        Deletes a role from the guild by its ID.

        Args:
            guild (discord.Guild): The guild to delete the role from.
            role_id (int): The ID of the role to delete.
            reason (Optional[str]): Reason for audit logs.

        Returns:
            bool: True if deleted successfully, False otherwise.
        """

        guild: discord.Guild = context.guild

        role: Optional[discord.Role] = guild.get_role(role_id)
        if role is None:
            # Role with ID {role_id} not found.
            return False

        try:
            await role.delete(reason=reason)
            return True
        except discord.Forbidden:
            #print("Missing permissions to delete the role.")
            return False
        except discord.HTTPException as e:
            #print(f"Failed to delete role: {e}")
            return False


    @staticmethod
    async def create_role(context: Context, name: str, reason:str = None) -> bool | Optional[discord.Role]:

        guild: discord.Guild = context.guild

        try:
            new_role: discord.Role = await guild.create_role(
                name=name,
                reason=reason
            )
            #await context.send(f"✅ Role `{new_role.name}` created successfully!")
            return new_role

        except discord.Forbidden:
            raise ValueError("Bot missing permissions to create roles.")
        except discord.HTTPException as e:
            raise ValueError("Bot failed to create roles.")

        return False


    @staticmethod
    def role_exists(context: commands.Context, identifier: Union[str, int]) -> Union[discord.Role, bool]:
        """
        Checks if a role exists in the guild by name (case-insensitive) or ID.

        Args:
            guild (discord.Guild): The guild to search in.
            identifier (Union[str, int]): Role name or ID.

        Returns:
            discord.Role | False: The matching role if found, else False.
        """

        guild = context.guild

        if isinstance(identifier, int):
            role = guild.get_role(identifier)
            return role if role is not None else False

        name = identifier.lower()
        for role in guild.roles:
            if role.name.lower() == name:
                return role

        return False


    @staticmethod
    async def get_role(ctx: commands.Context, role_id: int) -> Optional[discord.Role]:
        """
        Gets a role by ID using cache only (API fetch is not available for roles).

        Returns:
            Optional[discord.Role]: Role object or None if not found.
        """
        if ctx.guild is None:
            return None

        return ctx.guild.get_role(role_id)

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
    async def get_message(ctx: commands.Context, channel: discord.TextChannel, msg_id: int) -> Optional[discord.Message]:
        """
        Fetches a message by ID from a specific text channel using the API.

        Returns:
            Optional[discord.Message]: The message object or None.
        """
        try:
            message =  await channel.fetch_message(msg_id)
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

    @staticmethod
    async def send_error(context: commands.Context, message:str = None, ephemeral: Optional[bool] = False):

        await Discord.send_message(context, message, Color.Error, ephemeral)


    async def send_success(context: commands.Context, message:str = None, ephemeral: Optional[bool] = False):

        await Discord.send_message(context, message, Color.Success, ephemeral)


    async def send_warning(context: commands.Context, message:str = None, ephemeral: Optional[bool] = False):

        await Discord.send_message(context, message, Color.Warning, ephemeral)


    @staticmethod
    async def send_message(context: commands.Context, message:str = None, color:int = Color.Neutral, ephemeral: Optional[bool] = False):

        print(message)
        if message:
            embed = discord.Embed(description=message, color=color)

            if not context.interaction:
                content=context.author.mention
                try:
                    await context.reply(embed=embed)
                except discord.Forbidden:
                    channel = context.guild.get_channel(int(Discord.get_cmds_channel_id()))
                    if channel:
                        await channel.send(content=content, embed=embed)
            else:
                kwargs = {"embed": embed}
                if ephemeral:
                    kwargs["ephemeral"] = ephemeral

                try:
                    await context.interaction.followup.send(**kwargs)
                except:
                    channel = context.guild.get_channel(int(Discord.get_cmds_channel_id()))
                    if channel:
                        await channel.send(content=content, embed=embed)

        return


    @staticmethod
    def get_config_item(field:str = None):
        if not field:
            return None

        db_path = os.getenv("DB_PATH")
        if not db_path:
            raise ValueError("Environment variable DB_PATH is not set")

        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM config WHERE field = ?", (str(field),))
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            conn.close()

    @staticmethod
    def get_cmds_channel_id() -> int:
        return int(Discord.get_config_item('cmds_channel_id'))


    @staticmethod
    def get_log_level() -> int:
        return int(Discord.get_config_item('log_level'))
