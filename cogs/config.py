from __future__ import annotations
import discord
from typing import Optional
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from CanuckBot.Config import Config, CONFIG_FIELDS_EDITABLE, CONFIG_FIELDS_INFO
from CanuckBot.Info import Info
from CanuckBot.utils import validate_invoking_channel
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
                description="Use /config commands",
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

    async def config_set(
        self, context: Context, field: CONFIG_FIELDS_EDITABLE, value: Optional[str] = None
    ) -> None:

        if not await validate_invoking_channel(self.bot, context):
            await context.send(f"You cannot use this command in this channel.", ephemeral=True)
            return

        if context.interaction:
            await context.interaction.response.defer(ephemeral=False)
        else:
            await context.send(f"ERR: Use `/config` slash command", ephemeral=True)
            return


        if field.name and value:
            config = await Config.create(bot=self.bot)
            setattr(config, field.name, value)

            if await config.update(field.name):
                if field.name == 'interval_cleanup_task':
                    self.bot.cleanup_task.change_interval(minutes=float(value))
                elif field.name == 'interval_status_task':
                    self.bot.status_task.change_interval(minutes=float(value))
                elif field.name == 'interval_match_task':
                    self.bot.match_task.change_interval(minutes=float(value))
                await context.send("Configuration updated.")
            else:
                await context.interaction.followup.send(
                    "ERR: There was an error trying to update the config."
                )
        else:
            await context.interaction.followup.send("ERR: no field or value was provided.")


    @config.command(
        name="info",
        description="Display information about config options.",
    )
    @is_comp_manager()
    @app_commands.describe(
    )
    async def config_info(self, context: Context) -> None:

        if not await validate_invoking_channel(self.bot, context):
            await context.send(f"You cannot use this command in this channel.", ephemeral=True)
            return

        if context.interaction:
            await context.interaction.response.defer(ephemeral=True)
        else:
            await context.send(f"ERR: Use `/config` slash command", ephemeral=True)
            return

        try:
            config = await Config.create(bot=self.bot)

            embed = discord.Embed()

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
                await context.interaction.followup.send("ERR: There was an error trying to get info from the database: {e}")


    @config.command(
        name="setinfo",
        description="Set information about a configuration parameter.",
    )
    @is_superadmin()
    @app_commands.describe(
        field="The field to set info on.",
    )
    async def config_setinfo( self, context: Context, field: CONFIG_FIELDS_INFO, info_text: Optional[str] = None) -> None:

        if not await validate_invoking_channel(self.bot, context):
            await context.send(f"You cannot use this command in this channel.", ephemeral=True)
            return

        if context.interaction:
            await context.interaction.response.defer(ephemeral=False)
        else:
            await context.send(f"ERR: Use `/config` slash command", ephemeral=True)
            return

        try:
            objinfo = await Info.create(self.bot, "config", field.name)
            if await objinfo.set(info_text):
                await context.interaction.followup.send(f"config.{field.name} updated : `{info_text}`")
            else:
                await context.interaction.followup.send(f"config.{field.name} updated : `{info_text}`")
                await context.interaction.followup.send(f"ERR: couldn't update config.{field.name}")
        except Exception as e:
            await context.interaction.followup.send(f"ERR: couldn't update config.{field.name}: {e}")


    @config.command(
        name="list",
        description="List CanuckBot's configuration.",
    )
    @is_comp_manager()
    # @app_commands.describe(
    # )
    async def config_list(self, context: Context):

        if not await validate_invoking_channel(self.bot, context):
            await context.send(f"You cannot use this command in this channel.", ephemeral=True)
            return

        if context.interaction:
            await context.interaction.response.defer(ephemeral=True)
        else:
            await context.send(f"ERR: Use `/config` slash command", ephemeral=True)
            return

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

        await context.interaction.followup.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(ConfigCog(bot))
