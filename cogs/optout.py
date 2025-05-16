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


class OptoutCog(commands.Cog, name="optout"):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot

    @app_commands.command(
        name="optout",
        description="Opt out of a competition, or list your opt-outs.",
    )
    @app_commands.describe(
        competition="The competition to opt out of. Use 'all' for everything.",
    )

    async def optout(self, interaction: discord.Interaction, competition: Optional[str] = None):

        try:
            await interaction.response.defer(ephemeral=True)

            member: discord.Member = interaction.user

            if competition == "all":
                config = await Config.create(self.bot)
    
                if not await Discord.is_member_of_role(interaction.guild, member.id, int(config.optout_all_role_id)):
                    reason = f"{member.display_name} joining role Optout: all"
                    if not await Discord.join_role(interaction.guild, member.id, int(config.optout_all_role_id), reason):
                        await interaction.followup.send(f"ERR: A problem occured while joining role: {e}")
                        return

                    await interaction.followup.send(f"You opted out `{competition}` competitions.\n\nUse `/optin competition {competition}` to opt-in.")
                else:
                    await interaction.followup.send(f"You are already a member of `Optout: all`.\n\nUse /optin competition all` to opt-in.")

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
                
                if not await Discord.is_member_of_role(interaction.guild, member.id, int(c.optout_role_id)):
                    reason = f"{member.display_name} joining role Optout: {competition}"
                    if not await Discord.join_role(interaction.guild, member.id, int(c.optout_role_id), reason):
                        await interaction.followup.send(f"ERR: A problem occured while joining role: {e}")
                        return
                
                    await interaction.followup.send(f"You opted out `{competition}`.\n\nUse `/optin competition {competition}` to opt-in.")
                    return
                else:
                    await interaction.followup.send(f"You are already a member of `Optout: {competition}`.\n\nUse `/optin competition {competition}` to opt-in.")
                    return
            else:
                # Filter roles the user has that start with "Optout:"
                optout_roles = [
                    role.name.split(":", 1)[1].strip()
                    for role in member.roles
                        if role.name.startswith("Optout:")
                ]

                roles = []
                if optout_roles:
                    for shortname in optout_roles:
                        compname = comps[shortname]
                        roles.append(f"- `{shortname}` : {compname}")

                    role_list = "\n".join(roles)

                    await interaction.followup.send(
                        f"You are opted out of the following competitions:\n{role_list}"
                    )
                else:
                    await interaction.followup.send(
                        "You are not opted out of any competitions."
                    )

        except Exception as e:
            await interaction.followup.send(
                f"ERR: A problem occured while retrieving your data : {e}"
            )

async def setup(bot: DiscordBot) -> None:
    await bot.add_cog(OptoutCog(bot))
