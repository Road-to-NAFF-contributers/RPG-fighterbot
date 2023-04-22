import json
import requests
import random
import datetime
from interactions import *

from utils.custom_extension import CustomExtension


class fun_commands(CustomExtension):
    @slash_command(name="8ball")
    @slash_option(
        name="question",
        description="Ask the magic 8ball a question!",
        opt_type=OptionType.STRING,
        required=True,
    )
    async def eight_ball(self, ctx: InteractionContext, question):
        answers = [
            "It is decidedly so.",
            "Without a doubt.",
            "Yes definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]

        # await ctx.send(f"Q: {question}\n**The Magic 🎱 says: **{random.choice(answers)}")

        embed = Embed(
            title="Magic 8ball", description=f"Q: {question}", timestamp=datetime.datetime.utcnow()
        )
        embed.add_field(name="The Magic 🎱 says:", value=f"{random.choice(answers)}\n** **")
        embed.set_footer(text=f"Asked by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @slash_command(name="cat", description="Gets a random cat picture!")
    async def cat(self, ctx: InteractionContext):
        f = r"https://aws.random.cat/meow"
        r = requests.get(f)
        data = json.loads(r.text)

        embed = Embed(
            title="Here's your random cat image!",
            image=data["file"],
            # krebit to larssbot 🗿🗿🗿
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @slash_command(name="dog", description="Gets a random dog picture!")
    async def dog(self, ctx: InteractionContext):
        f = r"https://random.dog/woof.json"
        page = requests.get(f)
        data = json.loads(page.text)

        embed = Embed(
            title="Here's your random dog image!",
            image=data["url"],
            # krebit to larssbot 🗿🗿🗿
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @slash_command(name="meme", description="Summons a random meme from the internet!")
    async def meme(self, ctx: InteractionContext):
        content = requests.get("https://meme-api.com/gimme").text
        data = json.loads(content)

        embed = Embed(title=data["title"], image=data["url"], timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


def setup(bot):
    fun_commands(bot)
