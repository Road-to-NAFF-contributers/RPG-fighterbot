# Import NAFF
from interactions import (
    ActionRow,
    Button,
    ButtonStyle,
    Extension,
    InteractionContext,
    Member,
    OptionType,
    slash_command,
    slash_option,
    spread_to_rows,
    Embed,
    listen,
    ComponentContext,
)

from utils.custom_extension import CustomExtension

bot_version = "2.0 beta"


class info_commands(CustomExtension):
    # Info commands
    @slash_command(name="info", description="Some basic info about the bot")
    async def info(self, ctx: InteractionContext):
        embed = Embed(
            title="Info",
            description="A rpg arcade battle simulator(indev) made using the interactions v5 (NAFF got deprecated 💀) api wrapper.",
            color="#3498db",
        )
        embed.add_field(name="Bot version:", value=f"> {bot_version}", inline=True)
        embed.add_field(
            name="Created by:", value=f"> <@737983831000350731>\n> <@975738227669499916>"
        )
        embed.add_field(
            name="Official github repository:",
            value="> [Repo👨‍💻](https://github.com/Road-to-NAFF-contributers/RPG-fighterbot)",
        )
        embed.add_field(
            name="Official testing/development server:",
            value="> [Invite👾](https://discord.gg/TReMEyBQsh)",
        )

        await ctx.send(embeds=embed)

    # TODO: help command!
    # @slash_command(name="help")


# This is called by NAFF, to determine how to load the Extension
def setup(bot):
    info_commands(bot)
