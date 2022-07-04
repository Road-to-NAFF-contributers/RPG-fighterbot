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
    OptionTypes,
    InteractionContext,
    context_menu,
    listen,
    Member,
)
from dotenv import load_dotenv

bot = Client(sync_interactions=True)


@listen()
async def on_startup():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@slash_command(name="challenge")
@slash_option(
    name="challenge",
    description="Challenge someone to a battle!",
    opt_type=OptionTypes.USER,
    required=True,
)
async def challenge_user(ctx: InteractionContext, oponent: Member.user):
    await ctx.send(f"{oponent.user.mention}, you have been challenged by {ctx.author.mention}")


load_dotenv()
bot_TOKEN = os.environ["TOKEN"]
bot.start(bot_TOKEN)
