from naff import Colour, Extension
import naff


class Quick_commands(Extension):
    @naff.slash_command(name="info")
    async def info(ctx: naff.InteractionContext):
        embed = naff.Embed(
            title="Info",
            description="This bot is indev and we are making this lol.",
            color="#213fff",
        )

    @naff.slash_command("spotify", description="Share what youre listening!")
    async def spotify(self, ctx: naff.InteractionContext):
        listener = ctx.author
        if listener.activities:
            for activity in listener.activities:
                if activity.name == "Spotify":
                    cover = f"https://i.scdn.co/image/{activity.assets.large_image.split(':')[1]}"
                    embed = naff.Embed(
                        title=f"{listener.display_name}'s Spotify",
                        description="Listening to {}".format(activity.details),
                        color="#36b357",
                    )
                    embed.set_thumbnail(url=cover)
                    embed.add_field(name="Artist", value=activity.state)
                    embed.add_field(name="Album", value=activity.assets.large_text)
                    await ctx.send(embeds=embed)
        else:
            embed = naff.Embed(
                title=f"{listener.display_name}'s Spotify",
                description="Currently not listening anything",
                color="#36b357",
            )
            await ctx.send(embeds=embed)


def setup(bot):
    # This is called by naff so it knows how to load the Extension
    Quick_commands(bot)
