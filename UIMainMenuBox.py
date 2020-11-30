# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Rsvg", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Rsvg, GLib


class MainMenuBox(Gtk.Box):
    def __init__(self, has_chess_save, has_checkers_save):
        Gtk.Box.__init__(
            self, orientation=Gtk.Orientation.VERTICAL, spacing=10)
        # self.add(b)
        self.play_button = Gtk.Button.new_with_label("Play")
        # chess_button.connect("clicked", self.play_clicked)
        self.play_button.set_property("width-request", 300)
        self.play_button.set_property("height-request", 100)
        self.pack_start(self.play_button, True, True, 0)

        if has_chess_save or has_checkers_save:
            self.resume_button = Gtk.Button.new_with_label("Resume")
            # checkers_button.connect("clicked", self.resume_clicked)
            self.resume_button.set_property("width-request", 300)
            self.resume_button.set_property("height-request", 100)
            self.pack_start(self.resume_button, True, True, 0)

        back_button = Gtk.Button.new_with_mnemonic("_Exit")
        back_button.connect("clicked", self.exit_clicked)
        self.pack_start(back_button, True, True, 0)

    def exit_clicked(self, button):
        print("This should exit")
        Gtk.main_quit()
