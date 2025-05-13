from discord.ext import commands
from discord.ext.commands import Context
from database.db_utils import is_user_manager
from CanuckBot.types import User_Level
from database import DatabaseManager


def is_superadmin():
    @commands.check
    async def predicate(ctx: commands.Context):
        cog = ctx.command.cog
        if not cog or not hasattr(cog, 'bot'):
            raise commands.CheckFailure("This command must be part of a Cog with a 'bot' attribute.")

        db = cog.bot.database
        if not await is_user_manager(db, ctx.author.id, User_Level.Superadmin):
            raise commands.MissingPermissions(["CanuckBot Superadmin Manager"])
        return True

    return predicate

def is_full_manager():
    @commands.check
    async def predicate(ctx: commands.Context):
        cog = ctx.command.cog
        if not cog or not hasattr(cog, 'bot'):
            raise commands.CheckFailure("This command must be part of a Cog with a 'bot' attribute.")

        db = cog.bot.database
        if not await is_user_manager(db, ctx.author.id, User_Level.Full):
            raise commands.MissingPermissions(["CanuckBot Full Manager"])
        return True

    return predicate

def is_comp_manager():
    @commands.check
    async def predicate(ctx: commands.Context):
        cog = ctx.command.cog
        if not cog or not hasattr(cog, 'bot'):
            raise commands.CheckFailure("This command must be part of a Cog with a 'bot' attribute.")

        db = cog.bot.database
        if not await is_user_manager(db, ctx.author.id, User_Level.Comp):
            raise commands.MissingPermissions(["CanuckBot Comp Manager"])
        return True

    return predicate

def is_trusted_user():
    @commands.check
    async def predicate(ctx: commands.Context):
        cog = ctx.command.cog
        if not cog or not hasattr(cog, 'bot'):
            raise commands.CheckFailure("This command must be part of a Cog with a 'bot' attribute.")

        db = cog.bot.database
        if not await is_user_manager(db, ctx.author.id, User_Level.Trusted):
            raise commands.MissingPermissions(["CanuckBot Trusted User"])
        return True

    return predicate
