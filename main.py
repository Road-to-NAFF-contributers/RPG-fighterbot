# Bot made by using NAFF
# pip install git+https://github.com/NAFTeam/NAFF@dev

import os
import json

#whar does this do? Whar is "setlogmask"?
from syslog import setlogmask
from dotenv import load_dotenv

# Import NAFF
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
    Extension,
)

# Create a new instance of the Client
bot = Client(sync_interactions=True)

# Ran when the bot is ready
@listen()
async def on_startup():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")

#TODO: move this code into its own file!
@slash_command(name="challenge")
@slash_option(
    name="oponent",
    description="Challenge someone to a battle!",
    opt_type=OptionTypes.USER,
    required=True,
)
async def challenge_user(ctx: InteractionContext, oponent: Member.user):
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


#TODO: consider doing something with this, idk...?
@listen()
async def on_component(event: ComponentContext):
    # Gets the Event.context of the button click
    ctx = event.context

    # Checks whether the button was the button of who was challenged
    if not ctx.custom_id.endswith(f"{ctx.author.id}"):
        await ctx.send("This is not your button!", ephemeral=True)
        return
    else:
        # await ctx.message.edit(content="Edited message", components=None)

        if ctx.custom_id.startswith("fight_button"):
            await ctx.send(f"{ctx.author.mention} has accepted the challenge!")
        elif ctx.custom_id.startswith("deny_button"):
            await ctx.send(f"{ctx.author.mention} has denied the challenge!")

        #TODO: disable components when either is selected

        # await ctx.message.delete()
        for row in ctx.message.components:
            for component in row.components:
                component.disabled = True
        await ctx.message.edit(components=ctx.message.components)

        # mycomponents[0].components[0].disabled = True

# Load all modules, from a JSON file, for convenience
with open('modules.json', 'r') as file:
    data = json.load(file)

    for extension in data["extensions"]:
        bot.load_extension(extension)

# Load .env file secrets
load_dotenv()

# Start the bot
bot_TOKEN = os.environ["TOKEN"]
bot.start(bot_TOKEN)
