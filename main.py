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
    component_callback,
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
            custom_id="fight_button",
            style=ButtonStyles.GREEN,
            label="Fight🗡",
        ),
        Button(
            custom_id="deny_button",
            style=ButtonStyles.RED,
            label="Deny❌",
        ),
    )

    message = await ctx.send(f"{oponent.user.mention}, you have been challenged by {ctx.author.mention}", components=mycomponents)

#Fight button event callback
@component_callback("fight_button")
async def click_fight(ctx: ComponentContext):
    await ctx.send(f"{ctx.author.mention} has accepted the challenge!")

#Deny button event callback
@component_callback("deny_button")
async def click_deny(ctx: ComponentContext):
    await ctx.send(f"{ctx.author.mention} has denied the challenge!")

load_dotenv()
bot_TOKEN = os.environ["TOKEN"]
bot.start(bot_TOKEN)
