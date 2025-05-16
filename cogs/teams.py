import time
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from typing import Any
import CanuckBot
from CanuckBot.Info import Info
from CanuckBot.Config import Config
from CanuckBot.types import User_Level
from CanuckBot.Team import Team, TEAM_FIELDS_INFO, TEAM_FIELDS_EDITABLE
from decorators.checks import is_superadmin, is_full_manager, is_comp_manager, is_trusted_user
from database.db_utils import is_user_manager
from Discord.types import Snowflake
from Discord.LoggingFormatter import LoggingFormatter
from Discord.DiscordBot import DiscordBot
from Discord import Discord
from CanuckBot.utils import get_dominant_color_from_url, is_valid_handle, validate_invoking_channel


class TeamCog(commands.Cog, name="teams"):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot

    @commands.hybrid_group(
        name="team",
        description="Manage CanuckBot teams.",
    )
    @commands.has_permissions(manage_messages=True)
    async def team(self, context: Context) -> None:
        if not context.interaction:
            await Discord.send_error(context, "Usage: `/team`")


    @team.command(
        name="add",
        description="Add a new CanuckBot team.",
    )
    @is_superadmin()
    @app_commands.describe(
        name="The name of the team.",
        shortname="The shortname of the team",
    )
    async def team_add(self, context: Context, name: str = None, shortname: str = None) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/team add`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(context, f"You cannot use this command in <#{context.channel.id}>. Go to <#{cmds_channel}>" )
            return

        if name is None or shortname is None:
            await Discord.send_error(f"Missing parameters!")
            return

        invoking_user = context.interaction.user

        if not is_valid_handle(shortname):
            await Discord.send_error(f"`{shortname}` is not a valid shortname!")
            return

        t = Team(self.bot)

        await t.load_by_shortname(shortname)
        if t.is_loaded():
            await Discord.send_warning(f"`{t.shortname}` ({t.name}) already exists!")
            return

        config = Config(self.bot)
        self.bot.config = await config.list()


        try:
            t.team_id = None
            t.name = name
            t.shortname = shortname
            t.tz = config.default_tz
            t.created_at = int(time.time()) # now
            t.created_by = int(invoking_user.id)

            ret = await t.add()

            if ret:
                await Discord.send_success(f"Team `{t.shortname}` (`{t.team_id}`) created!")
            else:
                await Discord.send_error(f"A problem occured while creating the team!")

            return 
        except Exception as e:
            await Discord.send_error(f"A problem occured while creating the team: {e}")
            return


    @team.command(
        name="del",
        description="Remove a team.",
    )
    @is_superadmin()
    @app_commands.describe(
        key="The team_id or shortname of the team to delete.",
    )
    async def team_del(self, context: Context, key: str = None) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/team del`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(context, f"You cannot use this command in <#{context.channel.id}>. Go to <#{cmds_channel}>" )
            return

        if key is None:
            await Discord.send_error(f"Missing parameters!")
            return

        invoking_user = context.interaction.user

        try:
            t = Team(self.bot)

            await t.load_by_key(key)
            if not t.is_loaded():
                await Discord.send_warning(f"Team `{key}` doesn't exist!")
                return

            team_id = t.team_id
            shortname = t.shortname
            if await t.remove():
                await Discord.send_success(f"Team `{shortname}` (`{team_id}`) deleted!")
            else:
                await Discord.send_error(f"A problem occured while deleting the team!")
        except Exception as e:
            await Discord.send_error(f"A problem occured while deleting the team: {e}")
            return

        


    @team.command(
        name="info",
        description="Display information about team options.",
    )
    @is_full_manager()
    @app_commands.describe(
    )
    async def team_info(self, context: Context) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/team info`")
            return

        await context.interaction.response.defer(ephemeral=True)

        try:
            team = await Team.create(self.bot)

            embed = discord.Embed(color=int(0x28a745))

            attributes = vars(team)

            for attr in attributes:
                if attr not in TEAM_FIELDS_INFO:
                    continue

                objinfo = await Info.create(self.bot, "team", attr)
                if objinfo.info == "":
                    info = "n/a"
                else:
                    info = objinfo.info

                embed.add_field(name=attr, value=info, inline=False)

                await context.interaction.followup.send(content="**CanuckBot team info**", embed=embed)
        except:
                await Discord.send_error("There was an error trying to get info from the database.")

    @team.command(
        name="setinfo",
        description="Set information about a configuration parameter.",
    )
    @is_superadmin()
    @app_commands.describe(
        field="The field to set info on.",
    )
    async def team_setinfo(
        self, context: Context, field: TEAM_FIELDS_INFO, info_text: str = None) -> bool:
        objinfo = await Info.create(self.bot, "team", field.value)

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/team setinfo`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(context, f"You cannot use this command in <#{context.channel.id}>. Go to <#{cmds_channel}>" )
            return

        team = await Team.create(self.bot)
        try:
            getattr(team, field.value)
        except AttributeError as e:
            await Discord.send_error(f"team.{field.value} is not defined.")
            return

        if await objinfo.set(info_text):
            await Discord.send_success(f"team.{field.value} updated : `{info_text}`")
        else:
            await Discord.send_error(f"Couldn't update team.{field.value}")

    @team.command(
        name="show",
        description="Show info for a team.",
    )
    @app_commands.describe(
        key="The team id or shortname."
    )
    async def team_show(self, context: Context, key: str = None) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/team show`")
            return

        await context.interaction.response.defer(ephemeral=True)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(context, f"You cannot use this command in <#{context.channel.id}>. Go to <#{cmds_channel}>" )
            return

        try:
            team = await Team.create(self.bot)

            await team.load_by_key(key)

            if not team.is_loaded():
                await Discord.send_error(f"Team id/shortname `{key}` doesn't exist!")
                return

            if team.lastmodified_by:
                lastmodified_by = await Discord.get_user_or_member(context, int(team.lastmodified_by))
                lastmodified_byname = getattr(lastmodified_by, 'display_name', lastmodified_by.name)

            if team.lastmodified_at:
                formatted_lastmodfied_at = team.lastmodified_at.strftime("%A, %B %d, %Y %I:%M %p")

            creator = await Discord.get_user_or_member(context, int(team.created_by))
            creatorname = getattr(creator, 'display_name', creator.name)
            formatted_created_at = team.created_at.strftime("%A, %B %d, %Y %I:%M %p")


            embed = discord.Embed(color=int(0x28a745))

            if team.lastmodified_by:
                embed.set_footer(text=f"Created by {creatorname} - {formatted_created_at}\nLast modified by {lastmodified_byname} - {formatted_lastmodified_at}")
            else:
                embed.set_footer(text=f"Created by {creatorname} - {formatted_created_at}")

            embed.add_field(name="Team ID", value=team.team_id, inline=False)
            embed.add_field(name="Name", value=team.name, inline=False)
            embed.add_field(name="Shortname", value=team.shortname, inline=False)
            if not team.tz:
                embed.add_field(name="Timezone", value="none", inline=False)
            else:
                embed.add_field(name="Timezone", value=team.tz, inline=False)
            embed.add_field(name="Aliases", value=", ".join(team.aliases), inline=False)

            await context.interaction.followup.send(content="**Team**", embed=embed)

        except Exception as e:
            await Discord.send_error(f"A problem occured while retreiving team `{key}`: {e}")


    @team.command(
        name="alias",
        description="Add or remove an alias for a team.",
    )
    @is_full_manager()
    @app_commands.describe(
        alias="The alias",
        key="The team id or shortname."
    )
    async def team_alias(self, context: Context, alias: str = None, key: str = None) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/team alias`")
            return

        await context.interaction.response.defer(ephemeral=False)

        try:
            team = Team(self.bot)
            await team.load_by_key(key)

            if not team.is_loaded():
                await Discord.send_warning(f"Team `{key}` doesn't exist.")
                return 

            if alias.lower() == team.shortname.lower():
                await Discord.send_warning(f"Alias `{alias}` is already used as the shortname of team id `{team.team_id}`: `{team.name}`.")
                return 

            if await team.is_alias(alias):
                # we remove the alias
                await team.remove_alias(alias)

                if not team.aliases:
                    aliases = "none"
                else:
                    aliases = ", ".join(team.aliases)


                await Discord.send_success(f"Alias `{alias}` removed from team `{team.name}` : `{aliases}`")
            else:
                # we add the alias
                await team.add_alias(alias)

                aliases = ", ".join(team.aliases)

                await Discord.send_success(f"Alias `{alias}` added to team `{team.name}` : `{aliases}`")
        except Exception as e:
            await Discord.send_error(f"A problem occured while manipulating alias `{alias}` for team `{team.name}`: {e}")
            return

    @team.command(
        name="upcoming",
        description="Search for upcoming matches of a team.",
    )
    @is_full_manager()
    @app_commands.describe(
        key="The team id or shortname."
    )
    async def team_upcoming(self, context: Context, key: str = None) -> None:
        pass

    @team.command(
        name="search",
        description="Search the team database.",
    )
    @app_commands.describe(
        criteria="Criteria for querying the name, shortname or aliases."
    )
    async def team_search(self, context: Context, criteria: str = None) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/team search`")
            return

        await context.interaction.response.defer(ephemeral=True)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(context, f"You cannot use this command in <#{context.channel.id}>. Go to <#{cmds_channel}>" )
            return

        try:
            team = Team(self.bot)
            teams = await team.search(criteria)

            n = len(teams)

            page = 1
            pheader = f"*{n} team{'s' if n != 1 else ''} found - [page {page}]*\n"
            header = f"```{'id':>3} {'shortname':<18} {'name'}\n"
            header += f"{'-'*40}\n"
            footer = "\n-# Use `/team show id|shortname` for more details on a team."

            body = ""
            table = ""

            if not teams:
                table = "no teams found"
                body = header + table 
            elif n > 50:
                table = f"too many matches ({n}): narrow your search."
                body = header + table 
            else:
                count = len(pheader) + len(header) + len(footer)
                for item in teams:
                    table += f"{item['team_id']:>3} {item['shortname']:<18} {item['name']}\n"
                    count += len(table)

                    if count > 1900:
                        table += "```"
                        body = pheader + header + table + footer
                        await context.interaction.followup.send(f"{body}", ephemeral=True)
                        count = len(header) + len(footer)
                        table = ""
                        page += 1
                        pheader = f"*[Page {page}]*\n"
                        


            if table:
                if page == 1:
                    table += "```"
                    pheader = f"*{n} team{'s' if n != 1 else ''} found*\n"
                    body = pheader + header + table + footer
                else:
                    table += "```"
                    body = pheader + header + table + footer

                await context.interaction.followup.send(f"{body}", ephemeral=True)

        except Exception as e:
            await Discord.send_error(f"A problem occured while searching: {e}")


    @team.command(
        name="edit",
        description="Edit team parameters.",
    )
    @is_full_manager()
    @app_commands.describe(
        key="The team id or shortname.",
        field="Field to edit.",
        value="Value to set."
    )
    async def team_edit(self, context: Context, key: str = None, field: TEAM_FIELDS_EDITABLE = None, value: str = None) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/team edit`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(context, f"You cannot use this command in <#{context.channel.id}>. Go to <#{cmds_channel}>" )
            return

        invoking_user = context.interaction.user

        try:
            team = Team(self.bot)

            await team.load_by_key(key)
            if not team.is_loaded():
                await Discord.send_warning(f"Team `{key}` doesn't exist!")
                return

            if not field.name or not value:
                await Discord.send_error(f"Missing parameters to edit team `{key}`!")
                return

            if not await team.update(field.name, value):
                await Discord.send_error(f"There was an error trying to update team `{key}`!")
                return

            await Discord.send_success(f"Team `{team.shortname}` updated: `{field.name}` = `{value}`")
        except Exception as e:
            await Discord.send_error(f"A problem occured while updating team: `{key}`: `{e}`")


async def setup(bot: DiscordBot) -> None:
    await bot.add_cog(TeamCog(bot))
