import dotenv, hikari, lightbulb, aiohttp, os
from datetime import datetime



dotenv.load_dotenv()

bot = lightbulb.BotApp(
    os.environ["TOKEN"],
    prefix="+",
    banner=None,
    help_slash_command=True,
    intents=hikari.Intents.ALL,
    default_enabled_guilds=(985644102416732180)
)

# * Simple Commands

@bot.command
@lightbulb.command(
    name="ping",
    description="The bot's ping"
    )
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    embed = (
        hikari.Embed(
            title= "Pong",
            colour=0X3b9DFF,
            timestamp=datetime.now().astimezone()
        )
        .add_field(
            "Latency",
            f"Pong! {bot.heartbeat_latency*100:.2f}ms",
            inline=True,
        )
    )
    await ctx.respond(embed=embed)

@bot.command
@lightbulb.option(
    name="text",
    description="What you want to copy"
)
@lightbulb.command(
    name="copy",
    description="Copy's exactly what you say!"
)
@lightbulb.implements(lightbulb.SlashCommand)
async def copy(ctx: lightbulb.Context) -> None:
    await ctx.respond(ctx.options.text)
    
# * Setup the extensions from file
bot.load_extensions_from("./extensions/", must_exist=True)

@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
    bot.d.aio_session = aiohttp.ClientSession()

@bot.listen()
async def on_stopping(event: hikari.StoppingEvent) -> None:
    await bot.d.aio_session.close()

if __name__ == "__main__":
    if os.name != "nt":
        import uvloop




        uvloop.install()

    bot.run()



