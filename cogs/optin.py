import time
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from typing import Any, Optional
import CanuckBot
from CanuckBot.Info import Info
from CanuckBot.Config import Config
from CanuckBot.types import User_Level
from CanuckBot.Competition import Competition
from decorators.checks import is_superadmin, is_full_manager, is_comp_manager, is_trusted_user
from database.db_utils import is_user_manager
from Discord.types import Snowflake
from Discord.LoggingFormatter import LoggingFormatter
from Discord.DiscordBot import DiscordBot
from Discord import Discord
from CanuckBot.utils import get_dominant_color_from_url, is_valid_handle, validate_invoking_channel


class OptinCog(commands.Cog, name="optin"):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot

    @app_commands.command(
        name="optin",
        description="Opt in a competition. Use `/optin competition all` for all competitions!",
    )
    @app_commands.describe(
        competition="The competition to opt in.",
    )

    async def optin(self, interaction: discord.Interaction, competition: str = None):

        try:
            await interaction.response.defer(ephemeral=True)

            member: discord.Member = interaction.user

            if not competition:
                await interaction.followup.send(f"Usage: `/optin competition [competition]`")
                return

            if competition == "all":
                config = await Config.create(self.bot)
    
                if await Discord.is_member_of_role(interaction.guild, member.id, int(config.optout_all_role_id)):
                    reason = f"{member.display_name} leaving role `Optout: all`"
                    if not await Discord.leave_role(interaction.guild, member.id, int(config.optout_all_role_id), reason):
                        await interaction.followup.send(f"ERR: A problem occured while leaving role: {e}")
                        return
                
                    await interaction.followup.send(f"You opted in `{competition}`.\n\nUse `/optout competition {competition}` to opt-out.")
                else:
                    await interaction.followup.send(f"You are not a member of `Optout: all`..\n\nUse `/optout competition {competition}` to opt-out.")

                return


            c = Competition(self.bot)
            competitions = await c.list()
            comps: dict[str,str] = {}
            for item in competitions:
                comps[item["shortname"]] = item["name"]
            comps["all"] = "All competitions"
            

            if competition:
                await c.load_by_key(competition)
                if not c.is_loaded():
                    await interaction.followup.send(f"ERR: Competition `{competition}` doesn't exist.")
                    return
                
                if await Discord.is_member_of_role(interaction.guild, member.id, int(c.optout_role_id)):
                    reason = f"{member.display_name} leaving role `Optout: {competition}`"
                    if not await Discord.leave_role(interaction.guild, member.id, int(c.optout_role_id), reason):
                        await interaction.followup.send(f"ERR: A problem occured while leaving role: {e}")
                        return
                
                    await interaction.followup.send(f"You opted in `{competition}`.\n\nUse `/optout competition {competition}` to opt-out.")
                else:
                    await interaction.followup.send(f"You are not a member of `Optout: {competition}`..\n\nUse `/optout competition {competition}` to opt-out.")

        except Exception as e:
            await interaction.followup.send(
                f"ERR: A problem occured while retrieving your data : {e}"
            )

async def setup(bot: DiscordBot) -> None:
    await bot.add_cog(OptinCog(bot))
