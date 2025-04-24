import typing
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context
from datetime import datetime
import CanuckBot
from CanuckBot.Info import Info
from CanuckBot.Competition import Competition
from CanuckBot.constants import *
from decorators.checks import is_manager


class CompCog(commands.Cog, name="comp"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_group(
        name="comp",
        description="Manage competitions.",
    )
    @commands.has_permissions(manage_messages=True)
    async def comp(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Please specify a subcommand.\n\n**Subcommands:**\n`list` - List all competitions.\n`show` - Show the details of a competition.\nedit - Edit a competition\ndel - Remove a competition\nadd - Add a competition\nupcoming - Show upcoming matches of a competition", color=0xE02B2B,
            )
        await context.send(embed=embed)

    @comp.command(
        name="list",
        description="List all competitions.",
    )
    @is_manager()
    @app_commands.describe(
    )
    async def comp_list(self, context: Context) -> None:
        pass

    @comp.command(
        name="show",
        description="Show the details of a competition.",
    )
    @is_manager()
    @app_commands.describe(
        key="The competition to get info on (id_comp or handle).",
    )
    async def comp_show(self, context: Context, key: str = None) -> None:
        print("a1")
        comp = await Competition.create(self.bot, key)
        print("a2")
        if not comp.get('id_competition'):
            await context.send(f"ERR: couldn't find a matching competition.")
            return

        print("a3")
        # print(comp.data)
        embed = discord.Embed(title="Competition", color=discord.Color.blue())
        buffer = ""
        for f in comp.FIELDS:
            t = comp.FIELDS[f]['type']
            _type = comp.get_field_type(key)
            value = comp.get(f)

            if _type == TYPE_DISCORD_CHANNELID:
                channel = await CanuckBot.get_discord_channel(self.bot, value)
                v = CanuckBot.pp_discord_channel(channel)
            elif _type == TYPE_DISCORD_USERID:
                category = await CanuckBot.get_discord_user(context, self.bot, value)
                v = CanuckBot.pp_discord_user(category)
            elif _type == TYPE_DISCORD_CATEGORYID:
                category = await CanuckBot.get_discord_category(context, self.bot, value)
                v = CanuckBot.pp_discord_category(category)
            elif _type == TYPE_DISCORD_ROLEID:
                role = await CanuckBot.get_discord_role(context, self.bot, value)
                v = CanuckBot.pp_discord_role(role)
            elif _type == TYPE_COLOR:
                v = CanuckBot.pp_hex_color(value)
            elif _type == TYPE_URL:
                v = CanuckBot.pp_url(value)
            elif _type == TYPE_TIMESTAMP:
                v = CanuckBot.pp_timestamp(value)
            elif _type == TYPE_BOOL:
                v = CanuckBot.pp_bool(value)
            elif _type == TYPE_INT:
                v = CanuckBot.pp_int(value)
            elif _type == TYPE_STRING:
                v = CanuckBot.pp_string(value)
            else:
                v = value

            buffer += f"```{f:<15} : {v}```"

        # await context.send(embed=embed)
        await context.send(f"{buffer}")

    @comp.command(
        name="edit",
        description="Edit a competition.",
    )
    @is_manager()
    # @app_commands.describe(
    # )
    async def comp_edit(self, context: Context, key: str = None, field: str = None, value: str = None):
        pass


async def setup(bot) -> None:
    await bot.add_cog(CompCog(bot))
