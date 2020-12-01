# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import gi

from UIGameChoiceBox import GameChoiceBox

gi.require_version("Gtk", "3.0")
gi.require_version("Rsvg", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Rsvg, GLib


class PlayAgainWindow(Gtk.Window):
    """
       The PlayAgainWindow initializes a Gtk Window to hold Gtk buttons that allow a user to choose if they want to
       play again and restart the current game, go back to the main menu or exit the program.
       Attributes:
           main_box: A Gtk Box that holds the Gtk buttons.
           play_again_button: A Gtk button with the label "Play Again" that restarts the current game from the
           beginning.
           main_menu_button: A Gtk button with the label "Main Menu" that sends the user back to the main menu.
           exit_button: A Gtk button with the label "Exit" that exits the program.
    """
    def __init__(self):
        Gtk.Window.__init__(self, title="Play Again?")
        self.set_border_width(70)
        self.set_position(Gtk.WindowPosition.CENTER)
        col = Gdk.Color(2000, 6000, 200)
        self.modify_bg(Gtk.StateType.NORMAL, col)
        # b = Button()
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.main_box)
        # self.add(b)
        self.play_again_button = Gtk.Button.new_with_label("Play Again")
        self.play_again_button.connect("clicked", self.play_clicked)
        self.play_again_button.set_property("width-request", 300)
        self.play_again_button.set_property("height-request", 100)
        self.main_box.pack_start(self.play_again_button, True, True, 0)

        self.main_menu_button = Gtk.Button.new_with_label("Main Menu")
        self.main_menu_button.connect("clicked", self.main_menu_clicked)
        self.main_menu_button.set_property("width-request", 300)
        self.main_menu_button.set_property("height-request", 100)
        self.main_box.pack_start(self.main_menu_button, True, True, 0)

        self.exit_button = Gtk.Button.new_with_mnemonic("_Exit")
        self.exit_button.connect("clicked", self.exit_clicked)
        self.main_box.pack_start(self.exit_button, True, True, 0)

        # fixed the exit stalling problem
        self.connect("destroy", Gtk.main_quit)

    def play_clicked(self, button):
        print('Play was chosen')
        # do we want it to go back to the board or back through menus?
        game_type = GameChoiceBox()
        game_type.show_all()
        self.hide()

    def main_menu_clicked(self, button):
        print('This should go to resumed game')
        # main_menu = MainMenuBox()
        # main_menu.show_all()
        self.hide()

    @staticmethod
    def exit_clicked(self, button):
        print("This should exit")
        Gtk.main_quit()
