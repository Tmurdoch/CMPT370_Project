# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import gi

from Colours import ColourOffset, COLOUR_STRING_LOOK_UP_TABLE, \
    COLOUR_BOARD_STRING_LOOK_UP_TABLE

gi.require_version("Gtk", "3.0")
gi.require_version("Rsvg", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Rsvg, GLib


class CustomizationGrid(Gtk.Grid):
    def __init__(self):


        Gtk.Grid.__init__(self)
        self.set_column_spacing(10)
        self.set_row_spacing(20)
        title = Gtk.Label()
        title.set_markup("<big>Customize your pieces and board!</big>")
        title.set_justify(Gtk.Justification.RIGHT)
        title.override_color(Gtk.StateFlags.NORMAL,
                             Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        self.attach(title, 3, 0, 1, 1)

        # Pieces choices label
        label_piece = Gtk.Label()
        label_piece.set_markup("<b>Pieces</b>")
        # label_piece.set_justify(Gtk.Justification.CENTER)
        label_piece.override_color(
            Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        self.attach(label_piece, 0, 1, 1, 1)

        # Board choices label
        label_board = Gtk.Label()
        label_board.set_markup("<b>Board</b>")
        label_board.set_justify(Gtk.Justification.CENTER)
        label_board.override_color(
            Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        self.attach(label_board, 4, 1, 1, 1)

        x = 0
        self.piece_radio_buttons = []
        self.piece_radio_buttons.append(Gtk.RadioButton.new_with_label(
            None, COLOUR_STRING_LOOK_UP_TABLE[x][ColourOffset.OFFSET_LIGHT] + " " + COLOUR_STRING_LOOK_UP_TABLE[x][
                ColourOffset.OFFSET_DARK]))
        x += 1
        while x != len(COLOUR_STRING_LOOK_UP_TABLE):
            self.piece_radio_buttons.append(Gtk.RadioButton.new_with_label_from_widget(
                self.piece_radio_buttons[0],
                COLOUR_STRING_LOOK_UP_TABLE[x][ColourOffset.OFFSET_LIGHT] + " " + COLOUR_STRING_LOOK_UP_TABLE[x][
                    ColourOffset.OFFSET_DARK]))
            x += 1
        x = 0
        while x != len(COLOUR_STRING_LOOK_UP_TABLE):
            self.attach(self.piece_radio_buttons[x], 0, 2 + x, 1, 1)
            self.piece_radio_buttons[x].override_color(
                Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
            x += 1

        x = 0
        self.board_radio_buttons = []
        self.board_radio_buttons.append(Gtk.RadioButton.new_with_label(None, COLOUR_BOARD_STRING_LOOK_UP_TABLE[x][
            ColourOffset.OFFSET_LIGHT] + " " + COLOUR_BOARD_STRING_LOOK_UP_TABLE[x][ColourOffset.OFFSET_DARK]))
        x += 1
        while x != len(COLOUR_BOARD_STRING_LOOK_UP_TABLE):
            self.board_radio_buttons.append(
                Gtk.RadioButton.new_with_label_from_widget(
                    self.board_radio_buttons[0],
                    COLOUR_BOARD_STRING_LOOK_UP_TABLE[x][ColourOffset.OFFSET_LIGHT] + " " +
                    COLOUR_BOARD_STRING_LOOK_UP_TABLE[x][ColourOffset.OFFSET_DARK]))
            x += 1
        x = 0
        while x != len(COLOUR_BOARD_STRING_LOOK_UP_TABLE):
            self.attach(self.board_radio_buttons[x], 4, 2 + x, 1, 1)
            self.board_radio_buttons[x].override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
            x += 1

        self.back_button = Gtk.Button.new_with_label("Back")
        self.attach(self.back_button, 0, 8, 1, 1)

        self.start_button = Gtk.Button.new_with_label("Start")
        self.attach(self.start_button, 4, 8, 1, 1)

    @staticmethod
    def on_button_toggled(button, name):
        if button.get_active():
            state = "on"
            # self.colour()
        else:
            state = "off"
        print(name, "was turned", state)
