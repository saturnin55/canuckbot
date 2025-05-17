from __future__ import annotations
import discord
from typing import Optional
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from CanuckBot.types import Log_Level
from CanuckBot.Config import Config, CONFIG_FIELDS_EDITABLE, CONFIG_FIELDS_INFO
from CanuckBot.Info import Info
from CanuckBot.utils import validate_invoking_channel
from decorators.checks import is_superadmin, is_full_manager, is_comp_manager, is_trusted_user
from Discord.LoggingFormatter import LoggingFormatter
from Discord.DiscordBot import DiscordBot
from Discord import Discord, Color


class ConfigCog(commands.Cog, name="config"):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot

    @commands.hybrid_group(
        name="config",
        description="Configure CanuckBot.",
    )
    @commands.has_permissions(manage_messages=True)
    async def config(self, context: Context) -> None:
        if not context.interaction:
            await Discord.send_error(context, "Usage: `/config`")


    @config.command(
        name="set",
        description="Set a CanuckBot config parameter.",
    )
    #@commands.is_owner()
    @is_superadmin()
    @app_commands.describe(
        field="The field to set.",
        value="The text info to set for the selected field.",
    )

    async def config_set(
        self, context: Context, field: CONFIG_FIELDS_EDITABLE, value: Optional[str] = None
    ) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/config set`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(context, f"You cannot use this command in <#{context.channel.id}>. Go to <#{cmds_channel}>" )
            return


        if field.name and value:
            config = await Config.create(bot=self.bot)
            oldvalue = str(getattr(config, field.name))
            setattr(config, field.name, value)

            if await config.update(field.name):
                if field.name == 'interval_cleanup_task':
                    self.bot.cleanup_task.change_interval(minutes=float(value))
                elif field.name == 'interval_status_task':
                    self.bot.status_task.change_interval(minutes=float(value))
                elif field.name == 'interval_match_task':
                    self.bot.match_task.change_interval(minutes=float(value))
                await Discord.send_success(context, f"Configuration updated `config.{field.name}` : `{oldvalue}` -> `{value}`")
            else:
                await Discord.send_error(context, "There was an error trying to update the config.")
        else:
            await Discord.send_error(context, "No field or value was provided.")


    @config.command(
        name="info",
        description="Display information about config options.",
    )
    @is_comp_manager()
    @app_commands.describe(
    )
    async def config_info(self, context: Context) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/config info`")
            return

        await context.interaction.response.defer(ephemeral=True)

        try:
            config = await Config.create(bot=self.bot)

            embed = discord.Embed(color=Color.Success)

            attributes = vars(config)
            for attr in attributes:
                objinfo = await Info.create(self.bot, "config", attr)
                if objinfo.info == "":
                    info = "n/a"
                else:
                    info = objinfo.info

                embed.add_field(name=attr, value=info, inline=False)

            await context.interaction.followup.send(content="**CanuckBot config info**", embed=embed)
        except Exception as e:
            await Discord.send_error(context, f"There was an error trying to get info from the database: {e}")


    @config.command(
        name="setinfo",
        description="Set information about a configuration parameter.",
    )
    @is_superadmin()
    @app_commands.describe(
        field="The field to set info on.",
    )
    async def config_setinfo( self, context: Context, field: CONFIG_FIELDS_INFO, info_text: Optional[str] = None) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/config setinfo`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(f"You cannot use this command in this channel. Go to <#{cmds_channel}>" )
            return

        try:
            objinfo = await Info.create(self.bot, "config", field.name)
            oldinfo = obj.info
            if await objinfo.set(info_text):
                await Discord.send_success(f"config.{field.name} updated : `{oldinfo}` -> `{info_text}`")
            else:
                await Discord.send_error(f"Couldn't update config.{field.name}")
        except Exception as e:
            await Discord.send_error(f"couldn't update config.{field.name}: {e}")


    @config.command(
        name="list",
        description="List CanuckBot's configuration.",
    )
    @is_comp_manager()
    # @app_commands.describe(
    # )
    async def config_list(self, context: Context):

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/config list`")
            return

        await context.interaction.response.defer(ephemeral=True)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(f"You cannot use this command in this channel. Go to <#{cmds_channel}>" )
            return

        config = await Config.create(self.bot)

        embed = discord.Embed(
            title="CanuckBot Configuration", color=Color.Success
        )

        #embed.set_author(name=mngrname, icon_url=avatar_url)
        #embed.set_footer(text=f"Added by {creatorname} - {formatted_date}")
        logs_channel = await Discord.get_channel(context, int(config.logs_channel_id))
        cmds_channel = await Discord.get_channel(context, int(config.cmds_channel_id))
        category = await Discord.get_category(context, int(config.default_category_id))
        mngr_role = await Discord.get_role(context, int(config.mngr_role_id))
        optout_role = await Discord.get_role(context, int(config.optout_all_role_id))

        embed.add_field(name="logs_channel_id", value=logs_channel.mention, inline=False)
        embed.add_field(name="cmds_channel_id", value=cmds_channel.mention, inline=False)
        embed.add_field(name="interval_cleanup_task", value=config.interval_cleanup_task, inline=False)
        embed.add_field(name="interval_status_task", value=config.interval_status_task, inline=False)
        embed.add_field(name="interval_match_task", value=config.interval_match_task, inline=False)
        embed.add_field(name="default_add_hours_before", value=config.default_add_hours_before, inline=False)
        embed.add_field(name="default_del_hours_after", value=config.default_del_hours_after, inline=False)
        embed.add_field(name="default_category_id", value=f"{category.id} [{category.name}]", inline=False)
        embed.add_field(name="default_logo_url", value=config.default_logo_url, inline=False)
        embed.add_field(name="default_tz", value=config.default_tz, inline=False)
        embed.add_field(name="mngr_role_id", value=mngr_role.mention, inline=False)
        embed.add_field(name="log_level", value=config.log_level.name, inline=False)
        embed.add_field(name="optout_all_role_id", value=optout_role.mention, inline=False)

        await context.interaction.followup.send(embed=embed)


    @config.command(
        name="loglevel",
        description="Modify the log level.",
    )
    @is_superadmin()
    @app_commands.describe(
        loglevel="The log level.",
    )
    async def config_level(self, context: Context, loglevel: Log_Level) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/config loglevel`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(context, f"You cannot use this command in <#{context.channel.id}>. Go to <#{cmds_channel}>" )
            return

        if loglevel.value:
            config = await Config.create(bot=self.bot)
            oldvalue = str(getattr(config, 'log_level'))
            setattr(config, 'log_level', loglevel.value)

            if await config.update('log_level'):
                await Discord.send_success(context, f"Configuration updated for `config.log_level` : `{Log_Level[oldvalue].name}` -> `{loglevel.name}`")
            else:
                await Discord.send_error(context, "There was an error trying to update the config.")


async def setup(bot) -> None:
    await bot.add_cog(ConfigCog(bot))
