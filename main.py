# Bot made by using NAFF
# pip install git+https://github.com/NAFTeam/NAFF@dev

import os
import naff
from naff import (
    ActionRow,
    Client,
    Button,
    ButtonStyles,
    slash_command,
    slash_option,
    ComponentContext,
    OptionTypes,
    InteractionContext,
    listen,
    Member,
    spread_to_rows,
)
from dotenv import load_dotenv

bot = Client(sync_interactions=True)

@listen()
async def on_startup():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")

@slash_command(name="challenge")
@slash_option(
    name="oponent",
    description="Challenge someone to a battle!",
    opt_type=OptionTypes.USER,
    required=True,
)
async def challenge_user(ctx: InteractionContext, oponent: Member.user):
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

    message = await ctx.send(f"{oponent.user.mention}, you have been challenged by {ctx.author.mention}", components=mycomponents)

@listen()
async def on_component(event: ComponentContext):
    #Gets the Event.context of the button click
    ctx = event.context

    #Checks whether the button was the button of who was challenged
    if (not ctx.custom_id.endswith(f"{ctx.author.id}")):
        await ctx.send("This is not your button!", ephemeral=True)
        return
    else:
        # await ctx.message.edit(content="Edited message", components=None)

        if ctx.custom_id.startswith("fight_button"):
            await ctx.send(f"{ctx.author.mention} has accepted the challenge!")
        elif ctx.custom_id.startswith("deny_button"):
            await ctx.send(f"{ctx.author.mention} has denied the challenge!")

load_dotenv()
bot_TOKEN = os.environ["TOKEN"]
bot.start(bot_TOKEN)
