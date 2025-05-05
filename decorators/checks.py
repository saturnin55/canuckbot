from discord.ext import commands
from database.db_utils import is_user_manager
from CanuckBot.types import User_Level


def is_full_manager():
    async def predicate(ctx):
        if not is_user_manager(ctx.author.id, User_Level.Full):
            raise commands.MissingPermissions(["CanuckBot Full Manager"])
        else:
            return True

    return commands.check(predicate)

def is_superadmin():
    async def predicate(ctx):
        if not is_user_manager(ctx.author.id, User_Level.Superadmin):
            raise commands.MissingPermissions(["CanuckBot Superadmin Manager"])
        else:
            return True

    return commands.check(predicate)

def is_trusted_manager():
    async def predicate(ctx):
        if not is_user_manager(ctx.author.id, User_Level.Trusted):
            raise commands.MissingPermissions(["CanuckBot Trusted Manager"])
        else:
            return True

    return commands.check(predicate)
