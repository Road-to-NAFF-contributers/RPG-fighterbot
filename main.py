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
bot_intents: Intents = Intents.GUILD_PRESENCES | Intents.DEFAULT

# Create a new instance of the Client
bot = Client(intents=bot_intents, sync_interactions=True, send_command_tracebacks=False)

# Ran when the bot is ready
@listen()
async def on_startup():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


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
