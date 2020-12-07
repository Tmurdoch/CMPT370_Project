# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Rsvg", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Rsvg, GLib


class MainMenuBox(Gtk.Box):
    """
       The MainMenuBox initializes a Gtk Box to hold Gtk buttons that allow a user to choose if they want to play a
       game, resume a saved game if a save file is available or exit the program.
       Attributes:
           play_button: A Gtk button with the label "Play" that starts the sequence to play a game of chess or checkers.
           resume_button: A Gtk button with the label "Resume" that, if a save file exists, will resume a game of chess
           or checkers based on the saved game a user wants to play. If no save file was found, this button is hidden.
    """
    def __init__(self, has_chess_save, has_checkers_save):
        Gtk.Box.__init__(
            self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.play_button = Gtk.Button.new_with_label("Play")
        self.play_button.set_property("width-request", 300)
        self.play_button.set_property("height-request", 100)
        self.pack_start(self.play_button, True, True, 0)

        if has_chess_save or has_checkers_save:
            self.resume_button = Gtk.Button.new_with_label("Resume")
            self.resume_button.set_property("width-request", 300)
            self.resume_button.set_property("height-request", 100)
            self.pack_start(self.resume_button, True, True, 0)

        self.exit_button = Gtk.Button.new_with_label("Exit")
        self.pack_start(self.exit_button, True, True, 0)
