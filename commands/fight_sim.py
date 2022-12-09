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
    spread_to_rows,
    embed,
    listen,
    ComponentContext,
)
import naff

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
        global channel
        channel = ctx.channel
        global challenger
        challenger = ctx.author
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
            custom_id=f"fight-button_{challenge_id}", style=ButtonStyles.GREEN, label="Fight🗡"
        )
        deny_btn = Button(
            custom_id=f"deny-button_{challenge_id}", style=ButtonStyles.RED, label="Deny❌"
        )

        mycomponents: list[ActionRow] = spread_to_rows(fight_btn, deny_btn)

        await ctx.send(
            f"{oponent.user.mention}, you have been challenged by {ctx.author.mention}",
            components=mycomponents,
        )

    # Init function – runs when the extension is loaded
    def __init__(self, bot):
        print(f"Extension {self.name} loaded")

    async def battle(challenged: Member.user):
        turn_id = challenged.user.id
        btn1 = Button(custom_id=f"btn1_{turn_id}", style=ButtonStyles.GREEN, label="Do smt 1")
        btn2 = Button(custom_id=f"btn2_{turn_id}", style=ButtonStyles.RED, label="Do smt 2")
        btn3 = Button(custom_id=f"btn3_{turn_id}", style=ButtonStyles.BLUE, label="end interaction")

        mycomponents: list[ActionRow] = spread_to_rows(btn1, btn2, btn3)

        embed = naff.Embed(title="Battle", description="player1 against player2", color=0x4969E9)
        embed.set_footer(text="Player 1 turn")
        await channel.send(embed=embed, components=mycomponents)

    # TODO: consider doing something with this, idk...?
    @listen()
    async def on_component(event: ComponentContext):
        # Gets the Event.context of the button click
        ctx = event.ctx

        # TODO: move into its own module
        # Fight, handled in a seperate module
        if ctx.custom_id.startswith("fight-button") or ctx.custom_id.startswith("deny-button"):
            # Gets the custom_id of the button click
            custom_id = int(ctx.custom_id.split("_")[1])

            def remove():
                # Remove from list
                # ok i agree this is absolute shit code (shall be refactored soon)
                challenged_users.remove(challenges[custom_id]["Challenged"])
                challenged_users.remove(ctx.author.id)
                challenges.pop(custom_id)

            if challenges[custom_id]["Challenged"] == ctx.author.id:
                # This is your button!
                if ctx.custom_id.startswith("fight-button"):
                    await ctx.send(f"{ctx.author.mention} has accepted the challenge!")
                    remove()
                    # trigger a function in file "fight_sim.py"
                    battle(ctx.author)
                elif ctx.custom_id.startswith("deny-button"):
                    await ctx.send(f"{ctx.author.mention} has denied the challenge!")
                    remove()
                    return

            elif challenges[custom_id]["Challenger"] == ctx.author.id:
                await ctx.send(
                    f"You cannot accept your own challenge. Are you some dummy?", ephemeral=True
                )
                return
            else:
                await ctx.send(f"This is not your button!", ephemeral=True)
                return

        # Disables components (aka the buttons)
        for row in ctx.message.components:
            for component in row.components:
                component.disabled = True
        await ctx.message.edit(components=ctx.message.components)


# This is called by NAFF, to determine how to load the Extension
def setup(bot):
    fighter(bot)
