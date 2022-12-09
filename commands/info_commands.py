# Import NAFF
from naff import (
    Colour,
    Embed,
    Extension,
    InteractionContext,
    Member,
    OptionTypes,
    slash_command,
    slash_option,
)

bot_version = "1.1.1"


class info_commands(Extension):
    # Info commands
    @slash_command(name="info", description="Some basic info about the bot")
    async def info(self, ctx: InteractionContext):
        embed = Embed(
            title="Info",
            description="A rpg arcade battle simulator(indev) made using the NAFF api wrapper.",
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
            name="NAFF api wrapper:",
            value="> [Wrapper🐍](https://github.com/Road-to-NAFF-contributers/RPG-fighterbot)",
        )
        embed.add_field(
            name="Official testing/development server:",
            value="> [Invite👾](https://discord.gg/TReMEyBQsh)",
        )

        await ctx.send(embeds=embed)

    # TODO: help command!
    # @slash_command(name="help")

    # Init function - runs when the extension is loaded
    def __init__(self, bot):
        print(f"Extension {self.name} loaded")


# This is called by NAFF, to determine how to load the Extension
def setup(bot):
    info_commands(bot)
