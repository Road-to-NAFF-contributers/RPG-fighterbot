# Import NAFF
from naff import (
    Colour,
    Embed, 
    Extension, 
    InteractionContext,
    Member,
    OptionTypes, 
    slash_command,
    slash_option
)

class info_commands(Extension):
    # Info commands
    @slash_command(name="info", description="Some basic info about the bot")
    async def info(self, ctx: InteractionContext):
        embed = Embed(
            title="Info",
            description="This bot is indev and we are making this lol.",
            color="#3498db",
        )

        await ctx.send(embed=embed)
    
    # TODO: help command!
    # @slash_command(name="help")

    # Spotify commands
    @slash_command("spotify", description="Share what you're listening to!")
    @slash_option(
        name="user",
        description="Check what other people are listening to",
        opt_type=OptionTypes.USER,
        required=False,
    )
    async def spotify(self, ctx: InteractionContext, user: Member.user = None):
        listener = user or ctx.author
        
        #Get the first activity that contains "Spotify". Return None, if none present.
        spotify_activity = next((x for x in listener.activities if x == "Spotify"), None)

        if spotify_activity != None:
            cover = f"https://i.scdn.co/image/{spotify_activity.assets.large_image.split(':')[1]}"
            embed = Embed(
                title=f"{listener.display_name}'s Spotify",
                description="Listening to {}".format(spotify_activity.details),
                color="#36b357",
            )
            #SUGGESTION: instead of "set_thumbnail", use "thumbnail=" in the Embed constructor
            embed.set_thumbnail(url=cover)
            embed.add_field(name="Artist", value=spotify_activity.state)
            embed.add_field(name="Album", value=spotify_activity.assets.large_text)
            await ctx.send(embeds=embed)
        else:
            embed = Embed(
                title=f"{listener.display_name}'s Spotify",
                description="Currently not listening to anything",
                color="#36b357",
            )

            await ctx.send(embeds=embed)

    # Init function - runs when the extension is loaded
    # def __init__(self, bot):
    #     print("Extension loaded")

# This is called by NAFF, to determine how to load the Extension
def setup(bot):
    info_commands(bot)
