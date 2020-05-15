import gi
import cairo
import requests
from pynput.keyboard import Key, Controller


gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk, GObject, GLib
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import Gio

IS_PRESSED = False

def draw(widget, context):
    context.set_source_rgba(0, 0, 0, 0)
    context.set_operator(cairo.OPERATOR_SOURCE)
    context.paint()
    context.set_operator(cairo.OPERATOR_OVER)


def toggle_alt(eventbox, event):
    global IS_PRESSED

    if IS_PRESSED:
        keyboard.release(Key.alt)
        icon_pic = Pixbuf.new_from_file_at_size("alt_pics/edit1.png", 24, 24)
        icon.set_from_pixbuf(icon_pic)
        print("not pressed")
        IS_PRESSED = False
    else:
        keyboard.press(Key.alt)
        icon_pic = Pixbuf.new_from_file_at_size("alt_pics/close1.png", 24, 24)
        icon.set_from_pixbuf(icon_pic)
        print("pressed")
        IS_PRESSED = True


keyboard = Controller()

builder = Gtk.Builder()
builder.add_from_file("alt.glade")

window = builder.get_object("Alt")
icon = builder.get_object("icon")
toggle = builder.get_object("toggle")

screen = window.get_screen()
visual = screen.get_rgba_visual()
if visual and screen.is_composited():
    window.set_visual(visual)

toggle.connect("button_press_event", toggle_alt)
icon_pic = Pixbuf.new_from_file_at_size("alt_pics/edit1.png", 24, 24)
icon.set_from_pixbuf(icon_pic)
window.set_app_paintable(True)
window.connect("draw", draw)

window.show_all()
Gtk.main()