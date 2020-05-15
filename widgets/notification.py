import gi
import cairo
import requests
from pynput.keyboard import Key, Controller
import json

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, Gdk, GObject, GLib
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import Gio

SLOT = 1


def draw(widget, context):
    context.set_source_rgba(0, 0, 0, 0)
    context.set_operator(cairo.OPERATOR_SOURCE)
    context.paint()
    context.set_operator(cairo.OPERATOR_OVER)


def add_notification(slot_nr, label, content):
    if slot_nr == 1:
        slot1_pic = Pixbuf.new_from_file_at_size("notification_pics/noti_msg.png", 320, 65)
        slot1.set_from_pixbuf(slot1_pic)
        label1.set_label(label)
        content1.set_label(content)
    elif slot_nr == 2:
        slot2_pic = Pixbuf.new_from_file_at_size("notification_pics/noti_msg.png", 320, 65)
        slot2.set_from_pixbuf(slot2_pic)
        label2.set_label(label)
        content2.set_label(content)
    elif slot_nr == 3:
        slot3_pic = Pixbuf.new_from_file_at_size("notification_pics/noti_msg.png", 320, 65)
        slot3.set_from_pixbuf(slot3_pic)
        label3.set_label(label)
        content3.set_label(content)
    elif slot_nr == 4:
        slot4_pic = Pixbuf.new_from_file_at_size("notification_pics/noti_msg.png", 320, 65)
        slot4.set_from_pixbuf(slot4_pic)
        label4.set_label(label)
        content4.set_label(content)


def notification(label, content):
    global SLOT
    if SLOT <= 4:
        add_notification(SLOT, label, content)
        SLOT += 1
        return True
    else:
        more_notifications.set_label("More notifications on phone")
        return False


def timer():
    global SLOT
    with open('json.json') as json_file:
        data = json.load(json_file)
        for item in data:
            notification(data[item]['appTitle'], data[item]['message'])

    with open('json.json', 'w') as outfile:
        json.dump({}, outfile)
    return True


def remove_notifications():
    global SLOT
    slot1.clear()
    label1.set_label("")
    content1.set_label("")
    slot2.clear()
    label2.set_label("")
    content2.set_label("")
    slot3.clear()
    label3.set_label("")
    content3.set_label("")
    slot4.clear()
    label4.set_label("")
    content4.set_label("")
    more_notifications.set_label("")
    SLOT = 1


def clear_button_press(eventbox, event):
    clear_pic = Pixbuf.new_from_file_at_size("notification_pics/close.svg", 24, 24)
    clear.set_from_pixbuf(clear_pic)


def clear_button_release(eventbox, event):
    clear_pic = Pixbuf.new_from_file_at_size("notification_pics/close1.png", 24, 24)
    clear.set_from_pixbuf(clear_pic)
    remove_notifications()


builder = Gtk.Builder()
builder.add_from_file("notification.glade")

window = builder.get_object("Notification")
slot1 = builder.get_object("slot1")
slot2 = builder.get_object("slot2")
slot3 = builder.get_object("slot3")
slot4 = builder.get_object("slot4")
label1 = builder.get_object("label1")
label2 = builder.get_object("label2")
label3 = builder.get_object("label3")
label4 = builder.get_object("label4")
content1 = builder.get_object("content1")
content2 = builder.get_object("content2")
content3 = builder.get_object("content3")
content4 = builder.get_object("content4")
clear = builder.get_object("clear")
clear_event = builder.get_object("clear_event")
more_notifications = builder.get_object("more_notifications")

screen = window.get_screen()
visual = screen.get_rgba_visual()
if visual and screen.is_composited():
    window.set_visual(visual)

window.set_app_paintable(True)
window.connect("draw", draw)

clear_event.connect("button_press_event", clear_button_press)
clear_event.connect("button_release_event", clear_button_release)
GLib.timeout_add_seconds(5, timer)

window.show_all()
Gtk.main()
