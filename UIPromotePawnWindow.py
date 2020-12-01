# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Rsvg", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Rsvg, GLib


class PromotePawnWindow(Gtk.Window):
    """
       The PromotePawnWindow initializes a Gtk Window that pops up to display Gtk buttons that when a Players Pawn
       reaches the opponents last row, that player chooses between a Queen, Rook, Knight or Bishop for that Pawn to be
       promoted to.
       Attributes:
           promote_box: A Gtk Box that holds the Gtk buttons.
           queen_button: A Gtk button that promotes a Pawn to a Queen.
           knight_button: A Gtk button that promotes a Pawn to a Knight.
           bishop_button: A Gtk button that promotes a Pawn to a Bishop.
           rook_button: A Gtk button that promotes a Pawn to a Rook.
    """
    def __init__(self):
        Gtk.Window.__init__(self, title="Choose Promotion ")
        self.set_border_width(50)
        self.set_position(Gtk.WindowPosition.CENTER)
        col = Gdk.Color(2000, 6000, 200)  # dark green
        self.modify_bg(Gtk.StateType.NORMAL, col)
        self.promote_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.add(self.promote_box)

        self.queen_button = Gtk.Button.new_with_label("Queen")
        self.queen_button.connect("clicked", self.queen_clicked)

        self.knight_button = Gtk.Button.new_with_label("Knight")
        self.knight_button.connect("clicked", self.knight_clicked)

        self.bishop_button = Gtk.Button.new_with_label("Bishop")
        self.bishop_button.connect("clicked", self.bishop_clicked)

        self.rook_button = Gtk.Button.new_with_label("Queen")
        self.rook_button.connect("clicked", self.rook_clicked)

        self.promote_box.add(self.queen_button)
        self.promote_box.add(self.knight_button)
        self.promote_box.add(self.bishop_button)
        self.promote_box.add(self.rook_button)
        self.connect("destroy", self.hide)

    # CHANGE THIS WHEN GAME OBJECT IS FIGURED OUT
    def queen_clicked(self, button):
        print('Queen was chosen')
        if self.__game_obj.get_current_player() is self.__game_obj.get_light_player():
            self.__game_obj.get_light_player().get_timer().start()
        else:
            self.__game_obj.get_dark_player().get_timer().start()
        self.hide()

    def knight_clicked(self, button):
        print('Knight was chosen')
        if self.__game_obj.get_current_player() is self.__game_obj.get_light_player():
            self.__game_obj.get_light_player().get_timer().start()
        else:
            self.__game_obj.get_dark_player().get_timer().start()
        self.hide()

    def bishop_clicked(self, button):
        print('Bishop was chosen')
        if self.__game_obj.get_current_player() is self.__game_obj.get_light_player():
            self.__game_obj.get_light_player().get_timer().start()
        else:
            self.__game_obj.get_dark_player().get_timer().start()
        self.hide()

    def rook_clicked(self, button):
        print('Rook was chosen')
        if self.__game_obj.get_current_player() is self.__game_obj.get_light_player():
            self.__game_obj.get_light_player().get_timer().start()
        else:
            self.__game_obj.get_dark_player().get_timer().start()
        self.hide()
