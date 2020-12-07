# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import gi

from UIMainMenuBox import MainMenuBox
from PlayerType import PlayerType
from Game import Game
from UIResumeChoiceBox import ResumeChoiceBox
from Timer import Timer
from UIBoardGrid import BoardGrid
from UICustomizationGrid import CustomizationGrid
from UIGameChoiceBox import GameChoiceBox
from UIPlayerTypeBox import PlayerTypeBox

gi.require_version("Gtk", "3.0")
gi.require_version("Rsvg", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Rsvg, GLib
from GameType import GameType

import os


class TheWindow(Gtk.Window):
    def __init__(self, directory):
        Gtk.Window.__init__(self, title="370CC Main Menu")
        self.set_border_width(70)
        self.set_position(Gtk.WindowPosition.CENTER)
        col = Gdk.Color(2000, 6000, 200)  # dark green
        self.set_default_size(852, 627)
        self.modify_bg(Gtk.StateType.NORMAL, col)
        self.directory = directory

        self.has_chess_save = 0
        self.has_checkers_save = 0

        # Flags for UI
        self.single_player = 0
        self.multiplayer = 0

        # To be defined later
        self.game_type = None
        self.board = None

        if os.path.exists(directory + "/save-game.cmpt370Chess"):
            self.has_chess_save = 1
        if os.path.exists(directory + "/save-game.cmpt370Checkers"):
            self.has_checkers_save = 1
        self.main_box = MainMenuBox(
            self.has_chess_save, self.has_checkers_save)
        if self.has_chess_save or self.has_checkers_save:
            self.main_box.resume_button.connect("clicked", self.main_resume_clicked)

        self.main_box.play_button.connect("clicked", self.main_play_clicked)
        self.main_box.exit_button.connect("clicked", self.main_exit_clicked)

        self.game_choice_box = GameChoiceBox()
        self.game_choice_box.chess_button.connect("clicked", self.game_choice_chess_clicked)
        self.game_choice_box.checkers_button.connect("clicked", self.game_choice_checkers_clicked)
        self.game_choice_box.back_button.connect("clicked", self.game_choice_back_clicked)

        self.resume_choice_box = ResumeChoiceBox(self.has_chess_save, self.has_checkers_save)
        if self.has_chess_save:
            self.resume_choice_box.chess_button.connect("clicked", self.resume_choice_chess_clicked)
        if self.has_checkers_save:
            self.resume_choice_box.checkers_button.connect("clicked", self.resume_choice_checkers_clicked)
        self.resume_choice_box.back_button.connect("clicked", self.resume_choice_back_clicked)

        self.player_type = PlayerTypeBox()
        self.player_type.single_button.connect("clicked", self.player_type_single_clicked)
        self.player_type.multiplayer_button.connect("clicked", self.player_type_multi_clicked)
        self.player_type.back_button.connect("clicked", self.player_type_back_clicked)

        self.customization = CustomizationGrid()
        self.customization.back_button.connect("clicked", self.customization_back_clicked)
        self.customization.start_button.connect("clicked", self.customization_start_clicked)

        self.main_box.set_hexpand(True)
        self.game_choice_box.set_hexpand(True)
        self.resume_choice_box.set_hexpand(True)
        self.player_type.set_hexpand(True)
        self.customization.set_hexpand(True)

        self.grid = Gtk.Grid()
        self.grid.attach(self.main_box, 0, 0, 1, 1)
        self.grid.attach(self.game_choice_box, 0, 0, 1, 1)
        self.grid.attach(self.resume_choice_box, 0, 0, 1, 1)
        self.grid.attach(self.player_type, 0, 0, 1, 1)
        self.grid.attach(self.customization, 0, 0, 1, 1)

        self.add(self.grid)
        self.main_box.show()

        self.connect("destroy", Gtk.main_quit)

    def change_state(self, leaving, going):
        leaving.hide()
        going.show()
        if going is self.main_box:
            self.set_title("370CC Main Menu")
        elif going is self.game_choice_box:
            self.set_title("370CC - Choose Game Type")
        elif going is self.resume_choice_box:
            self.set_title("370CC - Choose What Game To Load")
        elif going is self.player_type:
            self.set_title("370CC - Choose Opponent")
        elif going is self.customization:
            self.set_title("370CC - Choose Colours")

    def main_play_clicked(self, button):
        print('Play was chosen')
        self.change_state(self.main_box, self.game_choice_box)

    def main_resume_clicked(self, button):
        print('This should go to resumed game')
        self.change_state(self.main_box, self.resume_choice_box)

    def main_exit_clicked(self, button):
        print('This should go to resumed game')
        Gtk.main_quit()

    def game_choice_chess_clicked(self, button):
        print('Chess was chosen')  # put next window here
        self.game_type = GameType.CHESS
        self.change_state(self.game_choice_box, self.player_type)

    def game_choice_checkers_clicked(self, button):
        print('Checkers was chosen')  # put next window here
        self.game_type = GameType.CHECKERS
        self.change_state(self.game_choice_box, self.player_type)

    def game_choice_back_clicked(self, button):
        print("This should go back to Main Menu Window")
        self.game_choice_box.hide()
        self.main_box.show()
        self.change_state(self.game_choice_box, self.main_box)

    def resume_choice_chess_clicked(self, button):
        print('Resume chess was chosen')  # put next window here
        self.game_type = GameType.CHESS
        self.resume_choice_box.hide()

        temp_game = Game(self.game_type, 0, 0)
        temp_game.load_from_file(self.directory)
        self.board = BoardGrid("Test", "multiplayer", temp_game, self.directory, load_from_file=1)
        self.grid.attach(self.board, 0, 0, 1, 1)
        self.board.show()

    def resume_choice_checkers_clicked(self, button):
        print('Resume checkers was chosen')  # put next window here
        self.game_type = GameType.CHECKERS
        self.resume_choice_box.hide()

        temp_game = Game(self.game_type, 0, 0)
        temp_game.load_from_file(self.directory)
        self.board = BoardGrid("Test", "multiplayer", temp_game, self.directory, load_from_file=1)
        self.grid.attach(self.board, 0, 0, 1, 1)
        self.board.show()

    def resume_choice_back_clicked(self, button):
        print("This should go back to Main Menu Window")
        self.resume_choice_box.hide()
        self.main_box.show()

    def player_type_single_clicked(self, button):
        print('Single Player was chosen')  # put next window here
        self.change_state(self.player_type, self.customization)
        self.single_player = 1

    def player_type_multi_clicked(self, button):
        print('Multi Player was chosen')  # put next window here
        self.change_state(self.player_type, self.customization)
        self.set_title("370CC - Choose Colours")
        self.multiplayer = 1

    def player_type_back_clicked(self, button):
        print("This should go back to Game Choice Window")
        self.change_state(self.player_type, self.game_choice_box)

    def customization_back_clicked(self, button):
        print("This should go back to Game Choice Window")
        self.change_state(self.customization, self.player_type)

    def customization_start_clicked(self, button):
        print("This should go to Board Window")
        self.customization.hide()

        piece_colour = 0
        while piece_colour != len(self.customization.piece_radio_buttons):
            if self.customization.piece_radio_buttons[piece_colour].get_active():
                break
            piece_colour += 1

        board_colour = 0
        while board_colour != len(self.customization.board_radio_buttons):
            if self.customization.board_radio_buttons[board_colour].get_active():
                break
            board_colour += 1

        temp_game = Game(self.game_type, piece_colour, board_colour)

        timer_active = self.customization.timer_radio_buttons[1].get_active()

        t1 = Timer(900, timer_active)
        t2 = Timer(900, timer_active)

        if self.multiplayer == 1:
            temp_game.build_light_player("light_player", PlayerType.HUMAN, t1)
            temp_game.build_dark_player("dark player", PlayerType.HUMAN, t2)
        else:
            temp_game.build_light_player("light_player", PlayerType.HUMAN, t1)
            temp_game.build_dark_player("dark player", PlayerType.AI, t2)

        self.board = BoardGrid("Test", "multiplayer", temp_game, self.directory)
        self.grid.attach(self.board, 0, 0, 1, 1)
        self.board.show()

    def return_to_main(self):
        self.board.destroy()
        self.main_box.show()
