import gi
import cairo
import requests
from pynput.keyboard import Key, Controller
import time
import os


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


def button_press(eventbox, event):
    keyboard.press(Key.enter)
    time.sleep(0.5)
    keyboard.release(Key.enter)
    print("yo")


keyboard = Controller()

builder = Gtk.Builder()
builder.add_from_file("widgets/google.glade")

window = builder.get_object("Google")
icon = builder.get_object("icon")
click = builder.get_object("click")

screen = window.get_screen()
visual = screen.get_rgba_visual()
if visual and screen.is_composited():
    window.set_visual(visual)

click.connect("button_press_event", button_press)

window.set_app_paintable(True)
window.connect("draw", draw)

os.system("./run_google_voice")

window.show_all()
Gtk.main()