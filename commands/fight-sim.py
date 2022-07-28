# Import NAFF
from naff import (
    ActionRow,
    Button,
    ButtonStyles,
    Extension,
    InteractionContext,
    Member,
    OptionTypes,
    slash_command,
    slash_option,
    spread_to_rows
)

class fighter(Extension):
    @slash_command(name="challenge")
    @slash_option(
        name="oponent",
        description="Challenge someone to a battle!",
        opt_type=OptionTypes.USER,
        required=True,
    )
    async def challenge_user(self, ctx: InteractionContext, oponent: Member.user):
        # global mycomponents
        mycomponents: list[ActionRow] = spread_to_rows(
            # TODO: Add a custom emoji
            Button(
                custom_id=f"fight_button_{oponent.id}",
                style=ButtonStyles.GREEN,
                label="Fight🗡",
            ),
            Button(
                custom_id=f"deny_button_{oponent.id}",
                style=ButtonStyles.RED,
                label="Deny❌",
            ),
        )

        message = await ctx.send(
            f"{oponent.user.mention}, you have been challenged by {ctx.author.mention}",
            components=mycomponents,
        )

    # Init function – runs when the extension is loaded
    def __init__(self, bot):
        print(f"Extension {self.name} loaded")

# This is called by NAFF, to determine how to load the Extension
def setup(bot):
    fighter(bot)