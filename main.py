# Bot made by using NAFF
# pip install git+https://github.com/NAFTeam/NAFF@dev

import os
import naff
from naff import (
    Client,
    Button,
    ButtonStyles,
    CommandTypes,
    slash_command,
    slash_option,
    component_callback,
    ComponentContext,
    OptionTypes,
    InteractionContext,
    context_menu,
    listen,
    components,
    Member,
)
from dotenv import load_dotenv

bot = Client(sync_interactions=True)


@listen()
async def on_startup():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


acceptdeny = [
    Button(
        custom_id="startbattle",
        style=ButtonStyles.GREEN,
        label="Fight⚔",
    ),
    Button(
        custom_id="denyrequest",
        style=ButtonStyles.RED,
        label="Deny❌",
    ),
]


@slash_command(name="challenge")
@slash_option(
    name="oponent",
    description="Challenge someone to a battle!",
    opt_type=OptionTypes.USER,
    required=True,
)
async def challenge_user(ctx: InteractionContext, oponent: Member.user):
    acceptdeny = [
        Button(
            custom_id="startbattle",
            style=ButtonStyles.GREEN,
            label="Fight⚔",
        ),
        Button(
            custom_id="denyrequest",
            style=ButtonStyles.RED,
            label="Deny❌",
        ),
    ]
    await ctx.send(
        f"{oponent.user.mention}, you have been challenged by {ctx.author.mention}",
        components=acceptdeny,
    )


@listen()
async def on_component(event: components):
    ctx = event.context

    match ctx.custom_id:
        case "startbattle":
            await ctx.send("Battle started.")


@listen()
async def on_component(event: components):
    ctx = event.context

    match ctx.custom_id:
        case "denyrequest":
            await ctx.send("Battle denied.")


load_dotenv()
bot_TOKEN = os.environ["TOKEN"]
bot.start(bot_TOKEN)
