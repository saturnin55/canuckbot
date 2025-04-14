from discord.ext import commands
from database.db_utils import is_user_manager

def is_manager():
    async def predicate(ctx):
        if not is_user_manager(ctx.author.id):
            raise commands.MissingPermissions(["CanuckBot Manager"])
        else:
            return True
    return commands.check(predicate)


