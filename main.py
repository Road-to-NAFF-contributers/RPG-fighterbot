import os
from naff import Client, Button, ButtonStyles, CommandTypes, context_menu, prefixed_command, listen
from dotenv import load_dotenv
import os

bot = Client(sync_interactions=True)

print("I made changes")


@listen()
async def on_startup():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


load_dotenv()
bot_TOKEN = os.environ["TOKEN"]
bot.start(bot_TOKEN)
