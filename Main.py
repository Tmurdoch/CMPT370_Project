# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import gi

from TheWindow import TheWindow
from initializeFS import initializeFS

gi.require_version("Gtk", "3.0")
gi.require_version("Rsvg", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Rsvg, GLib


if __name__ == "__main__":
    win = TheWindow(initializeFS())
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    win.game_choice_box.hide()
    win.resume_choice_box.hide()
    win.player_type.hide()
    win.customization.hide()
    Gtk.main()

