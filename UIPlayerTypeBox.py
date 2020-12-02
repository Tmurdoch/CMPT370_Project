# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Rsvg", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Rsvg, GLib


class PlayerTypeBox(Gtk.Box):
    """
       The CustomizationGrid initializes a Gtk Box to hold Gtk buttons that allow a user to choose the type of opponent
       they want to play against with the choices being single player against an AI or multi player against a local
       Human.
       Attributes:
           single_button: A Gtk button with the label "Single Player" that sets the game type to Single Player.
           multi_player_button: A Gtk button with the label "Multi Player" that sets the game type to Multi Player.
           back_button: A Gtk button that allows the user to go back to the previous menu.
    """
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=10)

        self.single_button = Gtk.Button.new_with_label("Single-Player")
        # single_button.get_style_context().add_class("suggested-action") changes button to blue
        self.single_button.set_property("width-request", 300)
        self.single_button.set_property("height-request", 100)
        self.pack_start(self.single_button, True, True, 0)

        self.multiplayer_button = Gtk.Button.new_with_label("Multi-Player")
        self.multiplayer_button.set_property("width-request", 300)
        self.multiplayer_button.set_property("height-request", 100)
        self.pack_start(self.multiplayer_button, True, True, 0)

        self.back_button = Gtk.Button.new_with_mnemonic("_Back")

        self.pack_start(self.back_button, True, True, 0)
