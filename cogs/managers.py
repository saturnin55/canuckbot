import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
import CanuckBot
from CanuckBot.Info import Info
from CanuckBot.types import User_Level
from CanuckBot.Manager import Manager, MANAGER_FIELDS_INFO, MANAGER_FIELDS_EDITABLE
from CanuckBot.Competition import Competition
from decorators.checks import is_superadmin, is_full_manager, is_comp_manager, is_trusted_user
from database.db_utils import is_user_manager
from Discord.types import Snowflake
from Discord.LoggingFormatter import LoggingFormatter
from Discord.DiscordBot import DiscordBot
from Discord import Discord
from CanuckBot.utils import get_dominant_color_from_url, validate_invoking_channel


class ManagerCog(commands.Cog, name="managers"):
    def __init__(self, bot: DiscordBot) -> None:
        self.bot = bot

    @commands.hybrid_group(
        name="mngr",
        description="Manage CanuckBot managers.",
    )
    @commands.has_permissions(manage_messages=True)
    async def mngr(self, context: Context) -> None:
        if not context.interaction:
            await Discord.send_error(context, "Usage: `/mngr`")


    @mngr.command(
        name="add",
        description="Add a new CanuckBot manager.",
    )
    @is_superadmin()
    @app_commands.describe(
        user="The user to add as a new CanuckBot manager.",
        level="The level of the CanuckBot manager",
    )
    async def mngr_add(self, context: Context, user: discord.User, level: User_Level) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/mngr add`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(context, f"You cannot use this command in <#{context.channel.id}>. Go to <#{cmds_channel}>" )
            return

        invoking_user = context.interaction.user

        manager = Manager(self.bot)
        ret = await manager.add(user.id, invoking_user.id, level)

        mngrname = getattr(user, 'display_name', user.name)

        if ret:
            await Discord.send_success(context, f"{mngrname} created as a new CanuckBot manager!")
        else:
            await Discord.send_error(context, f"There was an error trying to add {mngrname} as a new CanuckBot manager.")


    @mngr.command(
        name="level",
        description="Modify the level of a CanuckBot manager.",
    )
    @is_superadmin()
    @app_commands.describe(
        user="The user to modify the level.",
        level="The level of the CanuckBot manager",
    )
    async def mngr_level(self, context: Context, user: discord.User, level: User_Level) -> None:
        
        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/mngr level`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(context, f"You cannot use this command in <#{context.channel.id}>. Go to <#{cmds_channel}>" )
            return

        invoking_user = context.interaction.user

        m = Manager(self.bot)
        ret = await m.get(user.id)

        mngrname = getattr(user, 'display_name', user.name)

        await m.get(user.id)

        if not m.is_loaded():
            await Discord.send_error(context, f"User {mngrname} is not a manager!")
            return

        oldlevel = m.level

        try:
            ret = await m.update('level', int(level.value))

            # if new level is not disabled or Comp : clear manager_competitions
            if level.value != User_Level.Disabled and oldlevel == User_Level.Comp and level.value != User_Level.Comp:
                await m.clear_competitions()

            # if old level is not disabled or Comp : clear manager_competitions
            if oldlevel.value != User_Level.Disabled and oldlevel != User_Level.Comp and level.value == User_Level.Comp:
                await m.clear_competitions()
            
        except Exception as e:
            await Discord.send_error(context, "There was an error trying to get info from the database.")
            return

        await Discord.send_success(context, f"`{mngrname}` level set to `{level.name}`")


    @mngr.command(
        name="del",
        description="Remove a CanuckBot manager.",
    )
    @is_superadmin()
    @app_commands.describe(
        user="The user to remove as a CanuckBot manager.",
    )
    async def mngr_del(self, context: Context, user: discord.User) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/mngr del`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(context, f"You cannot use this command in <#{context.channel.id}>. Go to <#{cmds_channel}>" )
            return

        m = Manager(self.bot)
        mngrname = getattr(user, 'display_name', user.name)
        if await m.get(user.id):
            await m.remove(user.id)
            await Discord.send_success(context, f"{mngrname} removed as a CanuckBot manager!")
        else:
            await Discord.send_error(context,  f"{mngrname} is currently not a CanuckBot manager!")

    @mngr.command(
        name="list",
        description="List all CanuckBot managers.",
    )
    @is_full_manager()
    # @app_commands.describe(
    # )
    async def mngr_list(self, context: Context):

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/mngr list`")
            return

        await context.interaction.response.defer(ephemeral=True)

        m = Manager(self.bot)
        managers = await m.list()

        embeds = []

        k=0
        for item in managers:
            competitions = []
            await m.get(item["user_id"])

            if m.level in [User_Level.Superadmin, User_Level.Full] :
                competitions.append("all")
            elif not m.competitions:
                competitions.append("none")
            else:
                for competition_id in m.competitions:
                    comp = Competition(self.bot)
                    await comp.load_by_id(competition_id)
                    competitions.append(comp.shortname)

            manager = await Discord.get_user_or_member(context, int(m.user_id))
            mngrname = getattr(manager, 'display_name', manager.name)
            avatar_url = manager.avatar.url if manager.avatar else manager.default_avatar.url

            creator = await Discord.get_user_or_member(context, int(m.created_by))
            creatorname = getattr(creator, 'display_name', creator.name)

            formatted_date = m.created_at.strftime("%A, %B %d, %Y %I:%M %p")

            color = await get_dominant_color_from_url(self.bot.database, avatar_url)
            embed = discord.Embed(color=color)

            embed.set_author(name=manager.name, icon_url=avatar_url)
            embed.set_footer(text=f"Created by {creatorname} - {formatted_date}")

            embed.add_field(name="Name", value=manager.mention, inline=True)
            embed.add_field(name="User ID", value=manager.id, inline=True)
            embed.add_field(name="Level", value=m.level.name, inline=True)
            embed.add_field(name="Competitions managed", value=", ".join(competitions), inline=False)
            
            embeds.append(embed)

        nbr_embeds = len(embeds)
        if nbr_embeds <= 10:
            await context.interaction.followup.send(content="**CanuckBot Managers**", embeds=embeds)
        else:
            k = 1
            for i in range(0, len(embeds), 10):
                subembeds = embeds[i:i+10]
                await context.interaction.followup.send(content=f"**CanuckBot Managers {k}/**", embeds=subembeds)
                k = k + 1
                subembeds = []

    @mngr.command(
        name="info",
        description="Display information about manager options.",
    )
    @is_full_manager()
    @app_commands.describe(
    )
    async def mngr_info(self, context: Context) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/mngr info`")
            return

        await context.interaction.response.defer(ephemeral=True)

        try:
            manager = await Manager.create(self.bot)

            embed = discord.Embed()

            attributes = vars(manager)

            for attr in attributes:
                if attr not in MANAGER_FIELDS_INFO:
                    continue

                objinfo = await Info.create(self.bot, "manager", attr)
                if objinfo.info == "":
                    info = "n/a"
                else:
                    info = objinfo.info

                embed.add_field(name=attr, value=info, inline=False)

            await context.interaction.followup.send(content="**CanuckBot manager info**", embed=embed)
        except Exception as e:
           await Discsord.send_error(context, f"There was an error trying to get info from the database: {e}")

    @mngr.command(
        name="setinfo",
        description="Set information about a configuration parameter.",
    )
    @is_superadmin()
    @app_commands.describe(
        field="The field to set info on.",
    )
    async def mngr_setinfo(
        self, context: Context, field: MANAGER_FIELDS_INFO, info_text: str = None
    ) -> bool:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/mngr setinfo`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(context, f"You cannot use this command in <#{context.channel.id}>. Go to <#{cmds_channel}>" )
            return

        objinfo = await Info.create(self.bot, "manager", field.value)
        manager = await Manager.create(self.bot)

        try:
            getattr(manager, field.value)
        except AttributeError as e:
            await Discord.send_error(context, f"manager.{field.value} is not defined: {e}")
            return

        if await objinfo.set(info_text):
            await Discord.send_success(context, f"manager.{field.value} updated : `{info_text}`")
        else:
            await Discord.send_errorsend(context, f"Couldn't update manager.{field.value}")


    @mngr.command(
        name="trustedadd",
        description="Add a new CanuckBot Trusted manager.",
    )
    @is_full_manager()
    @app_commands.describe(
        user="The user to add as a CanuckBot Trusted manager."
    )
    async def mngr_trustedadd(self, context: Context, user: discord.User) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/mngr trustedadd`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(context, f"You cannot use this command in <#{context.channel.id}>. Go to <#{cmds_channel}>" )
            return

        invoking_user = context.interaction.user

        m = Manager(self.bot)

        mngrname = getattr(user, 'display_name', user.name)

        # check if the user isn't already a manager
        await m.get(user.id)
        if(m.user_id != 0):
            await Discord.send_error(context, f"User {mngrname} is already a manager!")
            return

        ret = await m.add(user.id, invoking_user.id, User_Level.Trusted)

        mngrname = getattr(user, 'display_name', user.name)
        if ret:
            await Discord.send_success(context, f"{mngrname} set as a new CanuckBot Trusted manager!")
        else:
            await Discord.send_error(context, f"There was an error trying to add {mngrname} as a new CanuckBot Trusted manager.")


    @mngr.command(
        name="trustedrevoke",
        description="Revoke Trusted manager privileges.",
    )
    @is_full_manager()
    @app_commands.describe(
        user="The user to revoke Trusted manager privileges.",
    )
    async def mngr_trustedrevoke(self, context: Context, user: discord.User) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/mngr trusterevoke`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(context, f"You cannot use this command in <#{context.channel.id}>. Go to <#{cmds_channel}>" )
            return

        m = Manager(self.bot)
        mngrname = getattr(user, 'display_name', user.name)

        await m.get(user.id)
        if m != 0 and m.level == User_Level.Trusted:
            await m.remove(user.id)
            await Discord.send_success(context, f"{mngrname}: CanuckBot {m.level.name} manager privileges revoked!")
        else:
            await Discord.send_error(context, f"{mngrname} is currently not a CanuckBot Trusted manager!")

    @mngr.command(
        name="comp",
        description="Add or remove a competition for a Comp Manager.",
    )
    @is_full_manager()
    @app_commands.describe(
        user="The Comp manage",
        key="The competition id or handle to add or remove"
    )
    async def mngr_comp(self, context: Context, user: discord.User, key:str = None) -> None:

        if context.interaction is None:
            await Discord.send_error(context, "Usage: `/mngr comp`")
            return

        await context.interaction.response.defer(ephemeral=False)

        if not await validate_invoking_channel(self.bot, context):
            cmds_channel = int(Discord.get_cmds_channel_id())
            await Discord.send_error(context, f"You cannot use this command in <#{context.channel.id}>. Go to <#{cmds_channel}>" )
            return

        invoking_user = context.interaction.user

        m = Manager(self.bot)
        mngrname = getattr(user, 'display_name', user.name)

        # check if the user isn't already a manager
        await m.get(user.id)
        if not m.is_loaded() or m.level != User_Level.Comp:
            await Discord.send_error(context, f"`{mngrname}` isn't a Comp manager!")
            return

        # check if the competition exists
        comp = Competition(self.bot)
        await comp.load_by_key(key)
        if not comp.is_loaded():
            await Discord.send_error(context, f"The competition `{key}` doesn't exist!")
            return

        try:
            if comp.competition_id in m.competitions:
                # remove the comp from the managed competitions of that trusted manager
                await m.delcomp(comp.competition_id)
                await Discord.send_success(context, f"`{comp.shortname}` removed to `{mngrname}`'s competitions.")
            else:
                # add the comp from the managed competitions of that trusted manager
                await m.addcomp(comp.competition_id)
                await Discord.send_success(context, f"`{comp.shortname}` added to `{mngrname}`'s competitions.")
        except Exception as e:
            await Discord.send_error(context, f"There was an error: {e}")
        

async def setup(bot: DiscordBot) -> None:
    await bot.add_cog(ManagerCog(bot))
