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
    """
       The CustomizationGrid initializes a Gtk Grid to hold Gtk radio buttons to customize the players pieces and board,
       a Gtk button to go back to the previous menu and a Gtk button start the game that was chosen.
       Attributes:
           piece_radio_buttons: List: A List to store the radio buttons for piece colour choices.
           board_radio_buttons: List: A List to store the radio buttons for board colour choices.
           back_button: A Gtk button with a label of "Back" that allows the user to go back to the previous menu.
           start_button: A Gtk button with a label of "Start" that initializes the chosen game, game type, piece
           colours, and board colours and shows the UIBoardGrid box.

       """
    def __init__(self):
        Gtk.Grid.__init__(self)
        self.set_column_spacing(10)
        self.set_row_spacing(20)
        title = Gtk.Label()
        title.set_markup("<big>Customize your pieces and board!</big>")
        title.set_justify(Gtk.Justification.RIGHT)
        title.override_color(Gtk.StateFlags.NORMAL,
                             Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        title.set_hexpand(True)
        self.attach(title, 2, 0, 1, 1)

        # Pieces choices label
        label_piece = Gtk.Label()
        label_piece.set_markup("<b>Pieces</b>")
        label_piece.set_justify(Gtk.Justification.CENTER)
        label_piece.override_color(
            Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        self.attach(label_piece, 0, 1, 1, 1)

        # Board choices label
        label_board = Gtk.Label()
        label_board.set_markup("<b>Board</b>")
        label_board.set_justify(Gtk.Justification.CENTER)
        label_board.override_color(
            Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        self.attach(label_board, 1, 1, 1, 1)

        # Timer label
        label_board = Gtk.Label()
        label_board.set_markup("<b>Timer</b>")
        label_board.set_justify(Gtk.Justification.CENTER)
        label_board.override_color(
            Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        self.attach(label_board, 3, 1, 1, 1)

        # Timer
        self.timer_radio_buttons = [
            Gtk.RadioButton.new_with_label(None, "No")]
        self.timer_radio_buttons.append(
            Gtk.RadioButton.new_with_label_from_widget(self.timer_radio_buttons[0], "Yes"))
        self.timer_radio_buttons[1].set_hexpand(True)
        self.timer_radio_buttons[0].set_hexpand(True)

        self.timer_radio_buttons[0].override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        self.timer_radio_buttons[1].override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))

        self.attach(self.timer_radio_buttons[1], 3, 2, 1, 1)
        self.attach(self.timer_radio_buttons[0], 3, 3, 1, 1)

        # Piece colours
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

        # Board colours
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
            self.attach(self.board_radio_buttons[x], 1, 2 + x, 1, 1)
            self.board_radio_buttons[x].override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
            x += 1

        self.back_button = Gtk.Button.new_with_label("Back")
        self.attach(self.back_button, 0, 2 + max(len(COLOUR_BOARD_STRING_LOOK_UP_TABLE),
                                                 len(COLOUR_STRING_LOOK_UP_TABLE)), 1, 1)

        self.start_button = Gtk.Button.new_with_label("Start")
        self.attach(self.start_button, 3, 2 + max(len(COLOUR_BOARD_STRING_LOOK_UP_TABLE),
                                                  len(COLOUR_STRING_LOOK_UP_TABLE)), 1, 1)

    @staticmethod
    def on_button_toggled(button, name):
        if button.get_active():
            state = "on"
        else:
            state = "off"
        print(name, "was turned", state)
