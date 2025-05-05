from discord.ext import commands
from discord.ext.commands import Context
from database.db_utils import is_user_manager
from CanuckBot.types import User_Level
from database import DatabaseManager


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

def is_trusted_manager():
    @commands.check
    async def predicate(ctx: commands.Context):
        cog = ctx.command.cog
        if not cog or not hasattr(cog, 'bot'):
            raise commands.CheckFailure("This command must be part of a Cog with a 'bot' attribute.")

        db = cog.bot.database
        if not await is_user_manager(db, ctx.author.id, User_Level.Trusted):
            raise commands.MissingPermissions(["CanuckBot Trusted Manager"])
        return True

    return predicate
'''
def is_full_manager(db: DatabaseManager = None):
    async def predicate(ctx):
        if not is_user_manager(db, ctx.author.id, User_Level.Full):
            raise commands.MissingPermissions(["CanuckBot Full Manager"])
        else:
            return True

    return commands.check(predicate)

def is_superadmin(db: DatabaseManager = None):
    async def predicate(ctx):
        if not is_user_manager(db, ctx.author.id, User_Level.Superadmin):
            raise commands.MissingPermissions(["CanuckBot Superadmin Manager"])
        else:
            return True

    return commands.check(predicate)

def is_trusted_manager(db: DatabaseManager = None):
    async def predicate(ctx):
        if not is_user_manager(db, ctx.author.id, User_Level.Trusted):
            raise commands.MissingPermissions(["CanuckBot Trusted Manager"])
        else:
            return True

    return commands.check(predicate)
'''
