import gi
import cairo
import requests

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk, GObject, GLib
from datetime import datetime, date


class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def onButtonPressed(self, button):
        print("Hello World!")


def draw(widget, context):
    context.set_source_rgba(0, 0, 0, 0)
    context.set_operator(cairo.OPERATOR_SOURCE)
    context.paint()
    context.set_operator(cairo.OPERATOR_OVER)


def get_date_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = date.today().strftime("%d %B %Y")
    time_label.set_label(current_time)
    date_label.set_label(current_date)
    return True


def get_weather():
    current_weather = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?id=588409&appid=839c6039d16b507dedb5b19f8160fe5e')
    current_temp = str(round(current_weather.json()['main']['temp'] - 273.15, 1))
    weather_label.set_label("Tallinn " + current_temp + "°C")
    return True


builder = Gtk.Builder()
builder.add_from_file("clock.glade")

# gets all the objects
window = builder.get_object("Clock")
time_label = builder.get_object("time")
date_label = builder.get_object("date")
weather_label = builder.get_object("weather")

# handles window transparency
screen = window.get_screen()
visual = screen.get_rgba_visual()
if visual and screen.is_composited():
    window.set_visual(visual)

window.custom_title = Gtk.Label(label=" ")
window.set_app_paintable(True)
window.connect("draw", draw)
get_date_time()
get_weather()

GLib.timeout_add_seconds(1, get_date_time)
GLib.timeout_add_seconds(60, get_weather)

window.show_all()
Gtk.main()