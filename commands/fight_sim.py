import interactions as inter
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
import os
from utils.custom_extension import CustomExtension
import random

# maybe we should cut the "challenge1" to just the id to simplify the json
# template vvvv
# challenges[f"challenge{challengeid}"] = {
#     "challenged_id": opponent.id,
#     "challenger_id": ctx.author.id,
#     "challenge_custom_id": challengeid,
# }
# ^^^^^^^^^^^^^^^
challenges = {}

challenged_users = []


class fighter(CustomExtension):
    # Create challenges dictionary to store all challenges
    # [fight button id, deny button id, challenger id, challenged id]

    @slash_command(name="challenge", description="Challenge someone to a battle!")
    @slash_option(
        name="opponent",
        description="Challenge someone to a battle!",
        opt_type=OptionType.USER,
        required=True,
    )
    # Removed .user from Member.user
    async def challenge_user(self, ctx: InteractionContext, opponent: Member):
        from main import challengeid

        channel = ctx.channel
        challenger = ctx.author
        if ctx.author.id in challenged_users:
            await ctx.send(f"You are already in a challenge!", ephemeral=True)
            return
        elif opponent.id in challenged_users:
            await ctx.send(f"{opponent.mention} is already in a challenge!", ephemeral=True)
            return

        challenged_users.extend([ctx.author.id, opponent.id])

        # Append the values necessary for the challenge to the list
        challenges[f"challenge{challengeid}"] = {
            "challenged_id": opponent.id,
            "challenger_id": ctx.author.id,
            "challenge_custom_id": challengeid,  # ik you could technically just use the variable ending as the custom id, but this is more readable
        }

        # TODO: Add a custom emoji

        fight_btn = Button(
            custom_id=f"fight-button_{challengeid}", style=ButtonStyle.GREEN, label="Fight🗡"
        )
        deny_btn = Button(
            custom_id=f"deny-button_{challengeid}", style=ButtonStyle.RED, label="Deny❌"
        )

        mycomponents: list[ActionRow] = spread_to_rows(fight_btn, deny_btn)

        await ctx.send(
            f"{opponent.user.mention}, you have been challenged by {ctx.author.mention}",
            components=mycomponents,
        )

        async def battle(challengeid):
            turn_id = random.randint(1, 2)
            if turn_id == 1:
                turn_id = challenges.get(f"challenge{challengeid}").get("challenger_id")
            btn1 = Button(custom_id=f"btn1_{turn_id}", style=ButtonStyle.GREEN, label="Do smt 1")
            btn2 = Button(custom_id=f"btn2_{turn_id}", style=ButtonStyle.RED, label="Do smt 2")
            btn3 = Button(
                custom_id=f"btn3_{turn_id}", style=ButtonStyle.BLUE, label="end interaction"
            )

            mycomponents: list[ActionRow] = spread_to_rows(btn1, btn2, btn3)

            embed = Embed(title="Battle", description="player1 against player2", color=0x4969E9)
            embed.set_footer(
                text="Succesfully challenged (this is still in development. Please be patient!)"
            )
            await channel.send(embed=embed, components=mycomponents)

        # Haha comment go brrr (this is a joke, please dont take it seriously)
        # gonna rewrite this shiz (supercatrocket 4 months ago)

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
                    challenges[f"challenge{custom_id}"] == None

                if challenges.get(f"challenge{custom_id}").get("challenged_id") == ctx.author.id:
                    # This is your button!
                    if ctx.custom_id.startswith("fight-button"):
                        await ctx.send(f"{ctx.author.mention} has accepted the challenge!")
                        remove()
                        # TODO: make it trigger a function in another
                        battle(ctx.author)
                    elif ctx.custom_id.startswith("deny-button"):
                        await ctx.send(f"{ctx.author.mention} has denied the challenge!")
                        remove()
                        return
                elif challenges.get(f"challenger{custom_id}").get("challenger_id") == ctx.author.id:
                    await ctx.send(
                        f"You cannot accept your own challenge. Are you some dummy?", ephemeral=True
                    )
                    return
                else:
                    await ctx.send(f"This is not your button!", ephemeral=True)
                    return


#     # Disables components (aka the buttons)
#     for row in ctx.message.components:
#         for component in row.components:
#             component.disabled = True
#     await ctx.message.edit(components=ctx.message.components)


# Called by interactions, upon loading the extension
def setup(bot):
    fighter(bot)
