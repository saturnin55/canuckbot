from __future__ import annotations
import discord
from typing import Optional
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from CanuckBot.Config import Config, CONFIG_FIELDS_EDITABLE
from CanuckBot.Info import Info
from decorators.checks import is_superadmin, is_full_manager, is_comp_manager, is_trusted_user
from Discord.LoggingFormatter import LoggingFormatter
from Discord.DiscordBot import DiscordBot
from Discord import Discord


class ConfigCog(commands.Cog, name="config"):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot

    @commands.hybrid_group(
        name="config",
        description="Configure CanuckBot.",
    )
    @commands.has_permissions(manage_messages=True)
    async def config(self, context: Context) -> None:
        if context.invoked_subcommand is None:
            embed = discord.Embed(
                description="Please specify a subcommand.\n\n**Subcommands:**\n`set` - Set CanuckBot's configuration.\n`list` - List CanuckBot's configuration.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)

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
#    @app_commands.choices(field=[
#        app_commands.Choice(name="logs_channel_id", value="logs_channel_id"),
#        app_commands.Choice(name="cmds_channel_id", value="cmds_channel_id"),
#        app_commands.Choice(name="default_add_hours_before", value="default_add_hours_before"),
#        app_commands.Choice(name="default_del_hours_after", value="default_del_hours_after"),
#        app_commands.Choice(name="default_category", value="default_category"),
#        app_commands.Choice(name="default_logo_url", value="default_logo_url"),
#        app_commands.Choice(name="default_tz", value="default_tz"),
#        app_commands.Choice(name="mngr_role_id", value="mngr_role_id"),
#        app_commands.Choice(name="default_comp_color", value="default_comp_color"),
#        app_commands.Choice(name="optout_all_role_id", value="optout_all_role_id")
#    ])
    async def config_set(
        self, context: Context, field: CONFIG_FIELDS_EDITABLE, value: Optional[str] = None
        #self, context: Context, field: Optional[str] = None, value: Optional[str] = None
#        self, context: Context, interaction: discord.Interaction, field: Optional[str] = None, value: Optional[str] = None
    ) -> None:
        self.bot.logger.info(LoggingFormatter.format_invoked_slash_cmd("/config set", context.author, context.kwargs))

        if field and value:
            config = await Config.create(bot=self.bot)
            setattr(config, field, value)
            if await config.update(field):
                await context.send("Configuration updated.")
            else:
                await context.send(
                    "ERR: There was an error trying to update the config."
                )
        else:
            await context.send("ERR: no field or value was provided.")

    @config.command(
        name="info",
        description="Display information about a configuration parameter.",
    )
    @is_comp_manager()
    @app_commands.describe(
        field="The field to get info on.",
    )
    async def config_info(self, context: Context, field: Optional[str] = None) -> None:
        config = await Config.create(bot=self.bot)

        # if not config.field_exists(field):
        #    await context.send(f"ERR: config.{field} is not defined.")
        #    return

        objinfo = await Info.create(self.bot, "config", field)
        if objinfo.info == "":
            info = "n/a"
        else:
            info = objinfo.info

        if info:
            await context.send(f"config.{field} : `{info}`")
        else:
            await context.send(
                "ERR: There was an error trying to get info from the database."
            )

    @config.command(
        name="setinfo",
        description="Set information about a configuration parameter.",
    )
    @is_superadmin()
    @app_commands.describe(
        field="The field to set info on.",
    )
    async def config_setinfo(
        self,
        context: Context,
        field: Optional[str] = None,
        info_text: Optional[str] = None,
    ) -> None:
        objinfo = await Info.create(self.bot, "config", field)
        if await objinfo.set(info_text):
            await context.send(f"config.{field} updated : `{info_text}`")
        else:
            await context.send(f"ERR: couldn't update config.{field}")

    @config.command(
        name="list",
        description="List CanuckBot's configuration.",
    )
    @is_comp_manager()
    # @app_commands.describe(
    # )
    async def config_list(self, context: Context):
        self.bot.logger.info(LoggingFormatter.format_invoked_slash_cmd("/config list", context.author, context.kwargs))

        config = await Config.create(self.bot)

        embed = discord.Embed(
            title="CanuckBot Configuration", color=int(config.default_comp_color,16)
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
        embed.add_field(name="default_comp_color", value=config.default_comp_color, inline=False)
        embed.add_field(name="optout_all_role_id", value=optout_role.mention, inline=False)

        #for key, v in config.model_dump().items():
        #    v = await config.get_attrval_str(context, key)
#
#            if v is None:
#                v = "n/a"

            # get a string representation
#            embed.add_field(
#                name=f"{key}",
#                value=f"{v}",
#                inline=True,  # Set to True to make columns
#            )
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(ConfigCog(bot))
