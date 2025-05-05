import discord
from typing import Optional
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from CanuckBot.Config import Config
from CanuckBot.Info import Info
from decorators.checks import is_superadmin, is_full_manager, is_trusted_manager


class ConfigCog(commands.Cog, name="config"):
    def __init__(self, bot) -> None:
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
        info="The text info to set for the selected field.",
    )
    async def config_set(
        self, context: Context, field: Optional[str] = None, info: Optional[str] = None
    ) -> None:
        if field and info:
            config = await Config.create(bot=self.bot)
            setattr(config, field, info)
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
    @is_trusted_manager()
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
    @is_trusted_manager()
    # @app_commands.describe(
    # )
    async def config_list(self, context: Context):
        config = await Config.create(self.bot)

        embed = discord.Embed(
            title="CanuckBot Configuration", color=discord.Color.blue()
        )

        for key, v in config.model_dump().items():
            # print(f"{key}: {v}")

            embed.add_field(
                name=f"{key}",
                value=f"{v}",
                inline=True,  # Set to True to make columns
            )
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(ConfigCog(bot))
