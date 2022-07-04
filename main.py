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


@slash_command(name="challenge")
@slash_option(
    name="oponent",
    description="Challenge someone to a battle!",
    opt_type=OptionTypes.USER,
    required=True,
)
async def challenge_user(ctx: InteractionContext, oponent: Member.user):
    button1 = Button(
        style=ButtonStyles.GREEN,
        label="Fight⚔",
    )
    button2 = Button(
        style=ButtonStyles.RED,
        label="Deny❌",
    )

    message = await ctx.send(
        f"{oponent.user.mention}, you have been challenged by {ctx.author.mention}",
        components=[button1, button2],
    )

    async def checktrue(component: button1) -> bool:
        global pressedfight
        pressedfight = True
        global username
        username = component.context.author.mention
        return component.context.author

    async def checkfalse(component: button2) -> bool:
        global pressedfight
        pressedfight = False
        global username
        username = component.context.author.mention
        return component.context.author

    try:
        # you need to pass the component you want to listen for here
        # you can also pass an ActionRow, or a list of ActionRows. Then a press on any component in there will be listened for
        truecomponent = await bot.wait_for_component(
            components=button1, check=checktrue, timeout=30
        )
        falsecomponent = await bot.wait_for_component(
            components=button2, check=checkfalse, timeout=30
        )

    except TimeoutError:
        await ctx.send("Request timed out!")

        button1.disabled = True
        button2.disabled = True
        await message.edit(components=[button1, button2])

    else:
        if pressedfight == True:
            await truecomponent.context.send(f"Yep, {username} accepted your challenge.")
        elif pressedfight == False:
            await falsecomponent.context.send(f"Nope, {username} denied your challenge.")
        button1.disabled = True
        button2.disabled = True
        await message.edit(components=[button1, button2])


load_dotenv()
bot_TOKEN = os.environ["TOKEN"]
bot.start(bot_TOKEN)
