# Bot made by using NAFF
# pip install git+https://github.com/NAFTeam/NAFF@dev

import os
import json
from dotenv import load_dotenv

# Import NAFF
from naff import (
    Client,
    Intents,
    ComponentContext,
    listen,
)

import commands.fight_sim as fight_sim

# Intents for the bot
bot_intents: Intents = (Intents.GUILD_PRESENCES | Intents.DEFAULT)

# Create a new instance of the Client
bot = Client(intents=bot_intents, sync_interactions=True, send_command_tracebacks=False)

# Ran when the bot is ready
@listen()
async def on_startup():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")

# TODO: consider doing something with this, idk...?
@listen()
async def on_component(event: ComponentContext):
    # Gets the Event.context of the button click
    ctx = event.context

    # TODO: move into its own module
    # Fight, handled in a seperate module
    if ctx.custom_id.startswith("fight-button") or ctx.custom_id.startswith("deny-button"):
        # Gets the custom_id of the button click
        custom_id = int(ctx.custom_id.split("_")[1])
        
        def remove():
            # Remove from list
            # ok i agree this is absolute shit code (shall be refactored soon)
            fight_sim.challenged_users.remove(fight_sim.challenges[custom_id]["Challenged"])
            fight_sim.challenged_users.remove(ctx.author.id)
            fight_sim.challenges.pop(custom_id)

        if fight_sim.challenges[custom_id]["Challenged"] == ctx.author.id:
            # This is your button! 
            if ctx.custom_id.startswith("fight-button"):
                await ctx.send(f"{ctx.author.mention} has accepted the challenge!")
                remove()
            elif ctx.custom_id.startswith("deny-button"):
                await ctx.send(f"{ctx.author.mention} has denied the challenge!")
                remove()
                return

        elif fight_sim.challenges[custom_id]["Challenger"] == ctx.author.id:
            await ctx.send(f"You cannot accept your own challenge. Are you some dummy?", ephemeral=True)
            return
        else:
            await ctx.send(f"This is not your button!", ephemeral=True)
            return
    
    # Disables components (aka the buttons)
    for row in ctx.message.components:
        for component in row.components:
            component.disabled = True
    await ctx.message.edit(components=ctx.message.components)


# Load all modules, from a JSON file, for convenience
with open("modules.json", "r") as file:
    data = json.load(file)

    for extension in data["extensions"]:
        bot.load_extension(extension)

# Load .env file secrets
load_dotenv()

# Start the bot
bot_TOKEN = os.environ["TOKEN"]
bot.start(bot_TOKEN)
