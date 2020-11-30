# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Rsvg", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Rsvg, GLib


class GameChoiceBox(Gtk.Box):
    """
       The GameChoiceBox initializes a Gtk Box to hold Gtk buttons that allow a user to choose what game they want to
       play.
       Attributes:
           chess_button: A Gtk button with a label "Chess" that sets the game to Chess.
           checkers_button: A Gtk button with a label "Checkers" that sets the game to Checkers.
           back_button: A Gtk button that allows the user to go back to the previous menu.
    """
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)

        self.chess_button = Gtk.Button.new_with_label("Chess")
        self.chess_button.set_property("width-request", 300)
        self.chess_button.set_property("height-request", 100)
        self.pack_start(self.chess_button, True, True, 0)

        self.checkers_button = Gtk.Button.new_with_label("Checkers")
        self.checkers_button.set_property("width-request", 300)
        self.checkers_button.set_property("height-request", 100)
        self.pack_start(self.checkers_button, True, True, 0)

        self.back_button = Gtk.Button.new_with_label("Back")
        self.pack_start(self.back_button, True, True, 0)

