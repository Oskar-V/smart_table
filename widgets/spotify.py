import sys
import spotipy
import spotipy.util as util
import gi
import cairo
import requests
import urllib.request
import time

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk, GObject, GLib
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import Gio


def draw(widget, context):
    context.set_source_rgba(0, 0, 0, 0)
    context.set_operator(cairo.OPERATOR_SOURCE)
    context.paint()
    context.set_operator(cairo.OPERATOR_OVER)


def buttonPlayPause(eventbox, event):
    print("play/pause")
    try:
        sp1.pause_playback()
        playpause_pic = Pixbuf.new_from_file_at_size("spotify_pics/play1.png", 32, 32)
        button_play.set_from_pixbuf(playpause_pic)
    except:
        sp1.start_playback()
        playpause_pic = Pixbuf.new_from_file_at_size("spotify_pics/pause1.png", 32, 32)
        button_play.set_from_pixbuf(playpause_pic)
        setSongInfo()


def buttonPressNext(eventbox, event):
    next_pic = Pixbuf.new_from_file_at_size("spotify_pics/next.png", 32, 32)
    button_next.set_from_pixbuf(next_pic)


def buttonPressPrevious(eventbox, event):
    previous_pic = Pixbuf.new_from_file_at_size("spotify_pics/next3.png", 32, 32)
    button_previous.set_from_pixbuf(previous_pic)


def buttonPressPlay(eventbox, event):
    if sp2.current_user_playing_track()['is_playing']:
        play_pic = Pixbuf.new_from_file_at_size("spotify_pics/pause.png", 32, 32)
        button_play.set_from_pixbuf(play_pic)
    else:
        play_pic = Pixbuf.new_from_file_at_size("spotify_pics/play.png", 32, 32)
        button_play.set_from_pixbuf(play_pic)


def buttonNext(eventbox, event):
    print("next")
    next_pic = Pixbuf.new_from_file_at_size("spotify_pics/next1.png", 32, 32)
    button_next.set_from_pixbuf(next_pic)
    sp1.next_track()
    time.sleep(0.5)
    setSongInfo()


def buttonPrevious(eventbox, event):
    print("previous")
    previous_pic = Pixbuf.new_from_file_at_size("spotify_pics/next2.png", 32, 32)
    button_previous.set_from_pixbuf(previous_pic)
    sp1.previous_track()
    time.sleep(0.5)
    setSongInfo()


def setAlbumArt():
    url = sp2.currently_playing()['item']['album']['images'][2]['url']
    response = urllib.request.urlopen(url)
    input_stream = Gio.MemoryInputStream.new_from_data(response.read(), None)
    pixbuf = Pixbuf.new_from_stream(input_stream, None)
    album_art.set_from_pixbuf(pixbuf)


def setSongInfo():
    try:
        artist.set_label(str(sp2.currently_playing()['item']['artists'][0]['name'])[0:22])
        song.set_label(str(sp2.currently_playing()['item']['name'])[0:22])
        setAlbumArt()
    except:
        return None


def checkPlayback():
    try:
        current = sp2.current_user_playing_track().get('is_playing')
    except:
        current = False
    if not current:
        playpause_pic = Pixbuf.new_from_file_at_size("spotify_pics/play1.png", 32, 32)
        button_play.set_from_pixbuf(playpause_pic)
        setSongInfo()
    else:
        playpause_pic = Pixbuf.new_from_file_at_size("spotify_pics/pause1.png", 32, 32)
        button_play.set_from_pixbuf(playpause_pic)
        setSongInfo()
    return True


def onLoad():
    previous_pic = Pixbuf.new_from_file_at_size("spotify_pics/next2.png", 32, 32)
    button_previous.set_from_pixbuf(previous_pic)
    next_pic = Pixbuf.new_from_file_at_size("spotify_pics/next1.png", 32, 32)
    button_next.set_from_pixbuf(next_pic)
    try:
        current = sp2.current_user_playing_track().get('is_playing')
    except:
        current = False
    if current:
        play_pic = Pixbuf.new_from_file_at_size("spotify_pics/pause1.png", 32, 32)
        button_play.set_from_pixbuf(play_pic)
        setSongInfo()
    else:
        play_pic = Pixbuf.new_from_file_at_size("spotify_pics/play1.png", 32, 32)
        button_play.set_from_pixbuf(play_pic)
        artist.set_label("---")
        song.set_label("---")


# Spotify details
scope1 = 'user-modify-playback-state'
scope2 = 'user-read-currently-playing'
username = 'randaqplay'
client_id = '60c2eb2acfad4c449fb25f3168086add'
client_secret = '7f35e085fcca497e97b09cdc59da8007'

builder = Gtk.Builder()
builder.add_from_file("spotify.glade")

# gets all the objects
window = builder.get_object("Spotify")
button_next = builder.get_object("next")
button_previous = builder.get_object("previous")
button_play = builder.get_object("play")
artist = builder.get_object("artist")
song = builder.get_object("song")
play_event = builder.get_object("play_event")
previous_event = builder.get_object("previous_event")
next_event = builder.get_object("next_event")
album_art = builder.get_object("album_art")

play_event.connect("button_release_event", buttonPlayPause)
previous_event.connect("button_release_event", buttonPrevious)
next_event.connect("button_release_event", buttonNext)
next_event.connect("button_press_event", buttonPressNext)
previous_event.connect("button_press_event", buttonPressPrevious)
play_event.connect("button_press_event", buttonPressPlay)

# handles window transparency
screen = window.get_screen()
visual = screen.get_rgba_visual()
if visual and screen.is_composited():
    window.set_visual(visual)


token1 = util.prompt_for_user_token(username, scope1, client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost:8888/callback/')
token2 = util.prompt_for_user_token(username, scope2, client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost:8888/callback/')
sp1 = spotipy.Spotify(auth=token1)
sp2 = spotipy.Spotify(auth=token2)
onLoad()
GLib.timeout_add_seconds(5, checkPlayback)
window.set_app_paintable(True)
window.connect("draw", draw)
window.show_all()
Gtk.main()



# sp1 = spotipy.Spotify(auth=token1)
# sp2 = spotipy.Spotify(auth=token2)
# # sp1.next_track()
# sp1.pause_playback()
# # sp.previous_track()
# # sp1.start_playback()
# # sp.volume(100)
# print(sp2.currently_playing()['item']['artists'][0]['name'])  # artist
# print(sp2.currently_playing()['item']['name'])  # song name
# print(sp2.currently_playing()['item']['album']['images'][2]['url'])  # album art
