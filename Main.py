# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import gi
import os

from TheWindow import TheWindow

gi.require_version("Gtk", "3.0")
gi.require_version("Rsvg", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Rsvg, GLib


def initializeFS():
    """initialize filesystem for storing stuff
    :returns: directory string"""
    if os.name == "posix":
        home = os.path.expanduser("~")
        if not (os.path.exists(home + "/.cmpt370checkerschess")):
            os.mkdir(home + "/.cmpt370checkerschess")
        return home + "/.cmpt370checkerschess"
    elif os.name == "nt":
        app_data = os.getenv("LOCALAPPDATA")
        if not (os.path.exists(app_data + "/.cmpt370checkerschess")):
            os.mkdir(app_data + "/.cmpt370checkerschess")
        return app_data + "/.cmpt370checkerschess"
    else:
        print("unknown os")
        return


if __name__ == "__main__":
    win = TheWindow(initializeFS())
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    win.game_choice_box.hide()
    win.resume_choice_box.hide()
    win.player_type.hide()
    win.customization.hide()
    Gtk.main()

