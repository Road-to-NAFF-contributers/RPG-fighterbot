# Bot made with the interactions v5 (NAFF has been deprecated) Discord-Bot API Wrapper

# pip install -U discord-py-interactions

from utils.keep_alive import start

start()

import os
import json
from dotenv import load_dotenv

# Import interactions
from interactions import (
    Client,
    listen,
    slash_command,
    OptionType,
    InteractionType,
    Intents,
    Activity,
    ActivityType,
    Status,
)
import interactions as inter  # deal with it AR :P

import commands.fight_sim as fight_sim

# Intents for the bot
bot_intents: Intents = Intents.GUILD_PRESENCES | Intents.DEFAULT

# Create a new instance of the Client
bot = Client(intents=bot_intents, sync_interactions=True, send_command_tracebacks=False)

challengeid = 0

# Ran when the bot is ready
@listen()
async def on_startup():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")
    await bot.change_presence(
        activity=Activity(
            name="Larss_J and FlopTheMost struggle with this bots development",
            type=ActivityType.WATCHING,
        ),
        status=Status.IDLE,
    )


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
