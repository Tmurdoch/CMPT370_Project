# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Rsvg", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Rsvg, GLib

# make c-stdlib style definitions so
# the code is readable and without
# magic numbers
SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2

resume = True


class ResumeChoiceBox(Gtk.Box):
    def __init__(self, has_chess_save, has_checkers_save):
        Gtk.Box.__init__(
            self, orientation=Gtk.Orientation.VERTICAL, spacing=10)

        if (has_chess_save):
            self.chess_button = Gtk.Button.new_with_label("Chess")
            self.chess_button.set_property("width-request", 300)
            self.chess_button.set_property("height-request", 100)
            self.pack_start(self.chess_button, True, True, 0)

        if (has_checkers_save):
            self.checkers_button = Gtk.Button.new_with_label("Checkers")
            self.checkers_button.set_property("width-request", 300)
            self.checkers_button.set_property("height-request", 100)
            self.pack_start(self.checkers_button, True, True, 0)

        self.back_button = Gtk.Button.new_with_label("Back")
        self.pack_start(self.back_button, True, True, 0)

