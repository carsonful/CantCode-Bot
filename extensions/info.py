from datetime import datetime
import requests
import hikari
import lightbulb
import miru

info_plugin = lightbulb.Plugin("Info")


@info_plugin.command
@lightbulb.option(
    "target", "The member to get information about.", hikari.User, required=True
)
@lightbulb.command(
    "userinfo", "Get info on a server member."
)
@lightbulb.implements(lightbulb.SlashCommand)
async def userinfo(ctx: lightbulb.Context) -> None:
    #USE THIS COMMAND TO GET TARGET OF USER
    target = ctx.get_guild().get_member(ctx.options.target or ctx.user)

    if not target:
        await ctx.respond("That user is not in the server.")
        return

    created_at = int(target.created_at.timestamp())
    joined_at = int(target.joined_at.timestamp())

    roles = (await target.fetch_roles())[1:]  # All but @everyone

    embed = (
        hikari.Embed(
            title=f"User Info - {target.display_name}",
            description=f"ID: `{target.id}`",
            colour=0x3B9DFF,
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(  
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
        )
        .set_thumbnail(target.avatar_url or target.default_avatar_url)
        .add_field(
            "Bot?",
            str(target.is_bot),
            inline=True,
        )
        .add_field(
            "Created account on",
            f"<t:{created_at}:d>\n(<t:{created_at}:R>)",
            inline=True,
        )
        .add_field(
            "Joined server on",
            f"<t:{joined_at}:d>\n(<t:{joined_at}:R>)",
            inline=True,
        )
        .add_field(
            "Roles",
            ", ".join(r.mention for r in roles),
            inline=False,
        )
    )

    await ctx.respond(embed)

@info_plugin.command
@lightbulb.option(
    "target", "The person's avatar you want", hikari.User, required=True
)
@lightbulb.command(
    "av", "get the avatar of a user"
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def av(ctx: lightbulb.Context):
    target = ctx.get_guild().get_member(ctx.options.target or ctx.user)
    if not target:
        await ctx.respond("That user is not in the server.")
        return 
    embed = (
        hikari.Embed(
            title=f"`Avatar of` - {target.display_name}",
            description=f"ID: `{target.id}`",
            color=0x3b9DFF,
            timestamp=datetime.now().astimezone()
        )#.set_thumbnail(target.avatar_url or target.default_avatar_url)
        .set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
        )
        .set_image(target.avatar_url or target.default_avatar_url)
    )
    await ctx.respond(embed)





@info_plugin.command
@lightbulb.command(
    "bitcoin", "Gives the current price of Bitcoin"
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)

async def bitcoin(ctx: lightbulb.Context) -> None:
    
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    data = response.json()
    price = data['bpi']['USD']['rate']
    embed = (
        hikari.Embed(
            title= "Bitcoin Price",
            colour=0xFFFFFF,
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
        )
        .add_field(
            "Price",
            str(price),
            inline=False
        )
        .set_thumbnail('https://media.kasperskydaily.com/wp-content/uploads/sites/92/2021/02/04045853/cryptoscam-in-discord-featured.jpg')
    )
    await ctx.respond(embed)




def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(info_plugin)