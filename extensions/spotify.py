import os
from datetime import datetime
from dotenv import load_dotenv
import hikari
import lightbulb
import spotipy
from spotipy.oauth2 import SpotifyOAuth
spotify_plugin = lightbulb.Plugin("spotifypub")


load_dotenv()

clientID = os.environ['SPOTIPY_CLIENT_ID']
scope = 'playlist-modify-public'
username = os.environ['user']
redirect = os.environ['SPOTIPY_REDIRECT_URI']
secret=os.environ['SPOTIPY_CLIENT_SECRET']

oAuth = SpotifyOAuth(
    scope=scope,
    username=username,
    redirect_uri=redirect,
    client_id=clientID,
    client_secret=secret
)


spotifyObject = spotipy.Spotify(auth_manager=oAuth)

# create the playlist first

#playlistName = 'Equi Public Playlist'
#playlistDesc = 'A discord bot playlist'

#spotifyObject.user_playlist_create(
#    user=username,
#    name=playlistName,
#    public=True,
#    description=playlistDesc
#)
equiplaylist = spotifyObject.user_playlists(user=username)
playlist = equiplaylist['items'][0]['id']


def getALLURIs():
    results= spotifyObject.playlist(playlist_id=playlist)
    return [item["track"]["uri"] for item in results["tracks"]["items"]]





@spotify_plugin.command
@lightbulb.option(
    "song", 
    "The song you want to add to the playlisy",
    type=str,
    required=True)
@lightbulb.command(
    "addsong",
    "add a song to the public playlist")
@lightbulb.implements(lightbulb.SlashCommand)
async def addnewsong(ctx: lightbulb.Context) -> None:
    song = ctx.options.song
    uriCache = getALLURIs()

    result = spotifyObject.search(q=song)
    try:
        result = result['tracks']['items'][0]['uri']
    except IndexError:
        embed = (
            hikari.Embed(
                title="Error",
                description="No Song Found"
            )
        )
        await ctx.respond(embed)
    
    if result in uriCache:
        embed = (
            hikari.Embed(
                title="Song In Playlist Already",
                description="Someone added that song to the playlist already"
            )
        )
    elif result not in uriCache:
        embed = (
            hikari.Embed(
                title= "Song Added!",
                colour=0x3B9DFF,
                timestamp=datetime.now().astimezone(),
                description=f"Your song '{song}' was add to the playlist."
            )
            .set_footer(
                text=f"Requested by {ctx.member.display_name}",
                icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
            )

        )
        spotifyObject.playlist_add_items(
            playlist_id=playlist,
            items=[result]
        )
    await ctx.respond(embed)

@spotify_plugin.command
@lightbulb.command("playlist", "Gives bot playlist.")
@lightbulb.implements(lightbulb.SlashCommand)
async def linkplaylist(ctx: lightbulb.Context) -> None:
    playlists = "https://open.spotify.com/playlist/3SdzePq0gUFreR4uCKmXX1?si=feb7a548a3ff4e16"
    await ctx.respond(playlists)



def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(spotify_plugin)