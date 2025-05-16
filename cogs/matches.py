import time
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from typing import Any
import CanuckBot
from CanuckBot.Info import Info
from CanuckBot.Config import Config
from CanuckBot.types import Competition_Type, Handle, TimeZone, Match_Status, Competition_Type
from CanuckBot.Team import Team, TEAM_FIELDS_INFO, TEAM_FIELDS_EDITABLE
from CanuckBot.Competition import Competition, COMPETITION_FIELDS_INFO, COMPETITION_FIELDS_EDITABLE
from CanuckBot.Match import Match, MATCH_FIELDS_INFO, MATCH_FIELDS_EDITABLE
from decorators.checks import is_superadmin, is_full_manager, is_comp_manager, is_trusted_user
from database.db_utils import is_user_manager
from Discord.types import Snowflake
from Discord.LoggingFormatter import LoggingFormatter
from Discord.DiscordBot import DiscordBot
from Discord import Discord
from CanuckBot.utils import get_dominant_color_from_url, is_valid_handle, validate_invoking_channel


class MatchCog(commands.Cog, name="match"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_group(
        name="match",
        description="Manage matches.",
    )
    @commands.has_permissions(manage_messages=True)
    async def match(self, context: Context) -> None:
        if not context.interaction:
            await Discord.send_error(context, "Usage: `/match`")


    @match.command(
        name="info",
        description="Display information about match options.",
    )
    @is_full_manager()
    @app_commands.describe(
    )
    async def match_info(self, context: Context) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/match info`")
            return

        await context.interaction.response.defer(ephemeral=True)

        try:
            match = await Match.create(self.bot)

            embed = discord.Embed(color=int(0x28a745))

            attributes = vars(comp)

            for attr in attributes:
                if attr not in MATCH_FIELDS_INFO:
                    continue

                objinfo = await Info.create(self.bot, "match", attr)
                if objinfo.info == "":
                    info = "n/a"
                else:
                    info = objinfo.info

                embed.add_field(name=attr, value=info, inline=False)

            await context.interaction.followup.send(content="**CanuckBot match info**", embed=embed)
        except Exception as e:
                await Discord.send_error(f"There was an error trying to get info from the database: {e}")


    @match.command(
        name="setinfo",
        description="Set information about a configuration parameter.",
    )
    @is_superadmin()
    @app_commands.describe(
        field="The field to set info on.",
    )
    async def match_setinfo(
        self, context: Context, field: MATCH_FIELDS_INFO, info_text: str = None
    ) -> bool:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/match setinfo`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(f"You cannot use this command in this channel. Go to <#{cmds_channel}>" )
            return

        objinfo = await Info.create(self.bot, "match", field.value)

        match = await Match.create(self.bot)

        try:
            getattr(match, field.value)
        except AttributeError as e:
            await Discord.send_error(f"match.{field.value} is not defined.")
            return

        if await objinfo.set(info_text):
            await Discord.send_success(f"match.{field.value} updated : `{info_text}`")
        else:
            await Discord.send_error(f"Couldn't update match.{field.value}")


    @match.command(
        name="add",
        description="Add a new CanuckBot match.",
    )
    @is_superadmin()
    @app_commands.describe(
        name="The name of the competition.",
        shortname="The shortname of the ocmpetition",
    )
    async def match_add(self, context: Context, name: str = None, shortname: str = None, comp_type: Competition_Type = Competition_Type.Men, is_international: bool = False) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/match add`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(f"You cannot use this command in this channel. Go to <#{cmds_channel}>" )
            return

        if name is None or shortname is None:
            await Discord.send_error(f"Missing parameters!")
            return

        invoking_user = context.interaction.user

        if not is_valid_handle(shortname):
            await Discord.send_error(f"`{shortname}` is not a valid shortname!")
            return

        c = Competition(self.bot)

        await c.load_by_shortname(shortname)
        if c.is_loaded():
            await Discord.send_error(f"`{c.shortname}` ({c.name}) already exists!")
            return

        config = Config(self.bot)
        self.bot.config = await config.list()

        assert self.bot.database, "ERR Competition.add(): database not available."

        try:
            c.competition_id = None
            c.name = name
            c.shortname = shortname
            c.logo_url = config.default_logo_url
            c.competition_type = comp_type.value
            c.is_monitored = False
            c.is_international = is_international
            c.optout_role_id = 0
            c.category_id = config.default_category_id
            c.hours_before_kickoff = config.default_add_hours_before
            c.hours_after_kickoff = config.default_del_hours_after
            c.created_at = int(time.time()) # now
            c.created_by = int(invoking_user.id)

            ret = await c.add()

            if ret:
                await Discord.send_success(f"Competition `{c.shortname}` (`{c.competition_id}`) created!")
            else:
                await Discord.send_error(f"A problem occured while creating the competition!")

            return
        except Exception as e:
            await Discord.send_error(f"A problem occured while creating the competition: `{e}`")
            return


    @match.command(
        name="edit",
        description="Edit a CanuckBot match.",
    )
    @is_comp_manager()
    @app_commands.describe(
        key="Id of the match.",
        field="Field to edit.",
        value="Value to set."
    )
    async def match_edit(self, context: Context, key: str = None, field: MATCH_FIELDS_EDITABLE = None, value: str = None) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/match edit`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(f"You cannot use this command in this channel. Go to <#{cmds_channel}>" )
            return

        invoking_user = context.interaction.user

        try:
            match = Match(self.bot)

            await match.get(int(key))
            if not match.is_loaded():
                await Discord.send_warning(f"Match `{key}` doesn't exist!")
                return

            if not field.name or not value:
                await Discord.send_error(f"Missing parameters to edit match `{key}`!")
                return

            if not await match.update(field.name, value):
                await Discord.send_error(f"There was an error trying to update match `{key}`!")
                return
                
            await Discord.send_success(f"Match `{match.match_id}` updated: `{field.name}` = `{value}`")
        except Exception as e:
            await Discord.send_error(f"A problem occured while updating match: `{key}`: `{e}`")
            return


    @match.command(
        name="del",
        description="Remove a match.",
    )
    @is_superadmin()
    @app_commands.describe(
        key="The match_id of the match to delete.",
    )
    async def match_del(self, context: Context, key: str = None) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/match del`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(f"You cannot use this command in this channel. Go to <#{cmds_channel}>" )
            return

        invoking_user = context.interaction.user

        if key is None:
            await Discord.send_error(f"Missing parameters!")
            return

        invoking_user = context.interaction.user

        try:
            match = Match(self.bot)

            await match.get(int(key))
            if not comp.is_loaded():
                await Discord.send_warning(f"Match `{key}` doesn't exist!")
                return

            match_id = match.match_id
            if await match.remove():
                await Discord.send_success(f"Match `{competition_id}` deleted!")
            else:
                await Discord.send_error(f"A problem occured while deleting the match!")
        except Exception as e:
            await Discord.send_error(f"A problem occured while deleting the match: {e}")
            return


    @match.command(
        name="search",
        description="Search CanuckBot matches.",
    )
    async def comp_search(self, context: Context):

        """
        if not await validate_invoking_channel(self.bot, context):
            await context.send(f"You cannot use this command in this channel.", ephemeral=True)
            return

        if context.interaction:
            await context.interaction.response.defer(ephemeral=True)
        else:
            await context.send(f"ERR: Use `/match` slash command", ephemeral=True)
            return
        if context.interaction:
            await context.interaction.response.defer(ephemeral=True)

        m = Match(self.bot)
        matches = await m.search()

        table ="```\n"
        table += f"   {'id':>3} {'shortname':<10} {'name'}\n"
        table += f"{'-'*43}\n"

        for item in competitions:
            if item['is_monitored']:
                is_monitored = "\U0001F7E9"
            else:
                is_monitored = "\U0001F7E7"
            table += f"{is_monitored} {item['competition_id']:>3} {item['shortname']:<10} {item['name']}\n"

        table += "```\n-# Use `/comp show id|shortname` for more details on a competition."

        await context.interaction.followup.send(f"{table}", ephemeral=True)
        """


    @match.command(
        name="match",
        description="Show details of a CanuckBot match.",
    )
    async def match_show(self, context: Context, key: str = None) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/match show`")
            return

        await context.interaction.response.defer(ephemeral=False)

        try:
            match = Match(self.bot)
            await comp.get(int(key))

            if not match.is_loaded():
                await Discord.send_warning(f"Match `{key}` doesn't exist!")
                return
        
            assert self.bot.database, "ERR Match.add(): database not available."

            creator = await Discord.get_user_or_member(context, int(match.created_by))
            creatorname = getattr(creator, 'display_name', creator.name)

            formatted_created_at = match.created_at.strftime("%A, %B %d, %Y %I:%M %p")

            if match.lastmodified_by:
                lastmodified_by = await Discord.get_user_or_member(context, int(match.lastmodified_by))
                lastmodified_byname = getattr(lastmodified_by, 'display_name', lastmodified_by.name)

            if match.lastmodified_at:
                formatted_lastmodfied_at = match.lastmodified_at.strftime("%A, %B %d, %Y %I:%M %p")
            
            #fixme get competition logo
            #color = await get_dominant_color_from_url(self.bot.database, str(match.logo_url))

            embed = discord.Embed(color=color)
            #embed.set_thumbnail(url=comp.logo_url)

            if match.lastmodified_by:
                embed.set_footer(text=f"Created by {creatorname} - {formatted_created_at}\nLast modified by {lastmodified_byname} - {formatted_lastmodified_at}\n/match info for details.")
            else:
                embed.set_footer(text=f"Created by {creatorname} - {formatted_created_at}\n/match info for details.")

            """
            embed.add_field(name="Competition ID", value=comp.competition_id, inline=False)
            embed.add_field(name="Name", value=comp.name, inline=False)
            embed.add_field(name="Shortname", value=comp.shortname, inline=False)
            embed.add_field(name="Competition Type", value=comp.competition_type.value, inline=False)
            embed.add_field(name="Monitored", value=str(comp.is_monitored), inline=False)
            embed.add_field(name="International", value=str(comp.is_international), inline=False)

            if not comp.optout_role_id:
                embed.add_field(name="Optout Role", value="—", inline=False)
            else:
                optout_role = await Discord.get_role(context, int(comp.optout_role_id))
                if not optout_role:
                    embed.add_field(name="Optout Role", value="—", inline=False)
                else:
                    embed.add_field(name="Optout Role", value=optout_role.mention, inline=False)

            if not comp.category_id:
                embed.add_field(name="Category", value="—", inline=False)
            else:
                category = await Discord.get_category(context, int(comp.category_id))
                if not category:
                    embed.add_field(name="Category", value="—", inline=False)
                else:
                    embed.add_field(name="Category", value=f"{category.id} [{category.name}]", inline=False)

            embed.add_field(name="Hours before kickoff", value=str(comp.hours_before_kickoff), inline=False)
            embed.add_field(name="Hours after kickoff", value=str(comp.hours_after_kickoff), inline=False)

            await context.interaction.followup.send(content="**Competition**", embed=embed)
            """
        except Exception as e:
            await Discord.send_error(f"A problem occured retrieving the match: {e}")
            return

async def setup(bot) -> None:
    await bot.add_cog(MatchCog(bot))
