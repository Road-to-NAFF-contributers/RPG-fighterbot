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

# challenges = {
#     ["fight_button", "deny_button", "challenger_id", "challenged_id"]
# }

challenged_users = []

challenges = []

class fighter(Extension):
    # Create challenges dictionary to store all challenges
    # [fight button id, deny button id, challenger id, challenged id]

    @slash_command(name="challenge")
    @slash_option(
        name="oponent",
        description="Challenge someone to a battle!",
        opt_type=OptionTypes.USER,
        required=True,
    )
    async def challenge_user(self, ctx: InteractionContext, oponent: Member.user):
        if ctx.author.id in challenged_users:
            await ctx.send(f"You are already in a challenge!", ephemeral=True)
            return
        elif oponent.id in challenged_users:
            await ctx.send(f"{oponent.mention} is already in a challenge!", ephemeral=True)
            return

        challenged_users.extend([ctx.author.id, oponent.id])

        # Append the values necessary for the challenge to the list
        challenges.append({"Challenged": oponent.id, "Challenger": ctx.author.id})
        
        # Create a challenge ID for easy accessing of values – not an actual ID, instead a unique number, the element number in the list
        challenge_id = len(challenges) - 1

        # TODO: Add a custom emoji
        
        fight_btn = Button(
                custom_id=f"fight-button_{challenge_id}",
                style=ButtonStyles.GREEN,
                label="Fight🗡")
        deny_btn = Button(
                custom_id=f"deny-button_{challenge_id}",
                style=ButtonStyles.RED,
                label="Deny❌")

        mycomponents: list[ActionRow] = spread_to_rows(
            fight_btn,
            deny_btn
        )

        await ctx.send(
            f"{oponent.user.mention}, you have been challenged by {ctx.author.mention}",
            components=mycomponents,
        )

    # Init function – runs when the extension is loaded
    def __init__(self, bot):
        print(f"Extension {self.name} loaded")

# This is called by NAFF, to determine how to load the Extension
def setup(bot):
    fighter(bot)