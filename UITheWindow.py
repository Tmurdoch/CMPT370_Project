# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import gi

from UIMainMenuBox import MainMenuBox
from PlayerType import PlayerType
from Game import Game
from ResumeChoiceBox import ResumeChoiceBox
from Timer import Timer
from Colours import ColourCodes
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
        Gtk.Window.__init__(self, title="Main Menu")
        self.set_border_width(70)
        self.set_position(Gtk.WindowPosition.CENTER)
        col = Gdk.Color(2000, 6000, 200)  # dark green
        self.modify_bg(Gtk.StateType.NORMAL, col)

        self.has_chess_save = 0
        self.has_checkers_save = 0

        if os.path.exists(directory + "/savedGame.cmpt370chess"):
            self.has_chess_save = 1
        if os.path.exists(directory + "/savedGame.cmpt370checkrs"):
            self.has_checkers_save = 1
        self.main_box = MainMenuBox(
            self.has_chess_save, self.has_checkers_save)
        if self.has_chess_save or self.has_checkers_save:
            self.main_box.resume_button.connect(
                "clicked", self.main_resume_clicked)

        self.main_box.play_button.connect("clicked", self.main_play_clicked)

        self.game_choice_box = GameChoiceBox()
        self.game_choice_box.chess_button.connect(
            "clicked", self.game_choice_chess_clicked)
        self.game_choice_box.checkers_button.connect(
            "clicked", self.game_choice_checkers_clicked)
        self.game_choice_box.back_button.connect(
            "clicked", self.game_choice_back_clicked)

        self.resume_choice_box = ResumeChoiceBox(
            self.has_chess_save, self.has_checkers_save)
        if self.has_chess_save:
            self.resume_choice_box.chess_button.connect(
                "clicked", self.resume_choice_chess_clicked)
        if self.has_checkers_save:
            self.resume_choice_box.checkers_button.connect(
                "clicked", self.esume_choice_checkers_clicked)
        self.resume_choice_box.back_button.connect(
            "clicked", self.resume_choice_back_clicked)

        self.player_type = PlayerTypeBox()
        self.player_type.single_button.connect(
            "clicked", self.player_type_single_clicked)
        self.player_type.multiplayer_button.connect(
            "clicked", self.player_type_multi_clicked)
        self.player_type.back_button.connect(
            "clicked", self.player_type_back_clicked)

        self.customization = CustomizationGrid()
        self.customization.back_button.connect(
            "clicked", self.customization_back_clicked)
        self.customization.start_button.connect(
            "clicked", self.customization_start_clicked)

        self.grid = Gtk.Grid()
        self.grid.attach(self.main_box, 0, 0, 1, 1)
        self.grid.attach(self.game_choice_box, 0, 0, 1, 1)
        self.grid.attach(self.player_type, 0, 0, 1, 1)
        self.grid.attach(self.customization, 0, 0, 1, 1)

        self.add(self.grid)
        self.main_box.show()

        # fixed the exit stalling problem
        self.connect("destroy", Gtk.main_quit)

    def main_play_clicked(self, button):
        print('Play was chosen')
        self.main_box.hide()
        self.game_choice_box.show()

    def main_resume_clicked(self, button):
        print('This should go to resumed game')
        self.main_box.hide()
        self.resume_choice_box.show()
        return

    def game_choice_chess_clicked(self, button):
        print('Chess was chosen')  # put next window here
        self.game_type = GameType.CHESS
        self.game_choice_box.hide()
        self.player_type.show()

    def game_choice_checkers_clicked(self, button):
        print('Checkers was chosen')  # put next window here
        self.game_type = GameType.CHECKERS
        self.game_choice_box.hide()
        self.player_type.show()

    def game_choice_back_clicked(self, button):
        print("This should go back to Main Menu Window")
        self.game_choice_box.hide()
        self.main_box.show()

    def resume_choice_chess_clicked(self, button):
        print('Resume chess was chosen')  # put next window here
        self.game_type = GameType.CHESS
        self.resume_choice_box.hide()
        print("SEE TODO STUFF NERE THIS LINE")
        # TODO CREATE AN ARE YOU SURE SCREEN AND A "PLAY"
        # BUTTON BEFORE STARTING THE LOADED GAME

    def resume_choice_checkers_clicked(self, button):
        print('Resume checkers was chosen')  # put next window here
        self.game_type = GameType.CHECKERS
        self.resume_choice_box.hide()
        print("SEE TODO STUFF NERE THIS LINE")
        # TODO CREATE AN ARE YOU SURE SCREEN AND A "PLAY"
        # BUTTON BEFORE STARTING THE LOADED GAME

    def resume_choice_back_clicked(self, button):
        print("This should go back to Main Menu Window")
        self.resume_choice_box.hide()
        self.main_box.show()

    def player_type_single_clicked(self, button):
        print('Single Player was chosen')  # put next window here
        self.player_type.hide()
        self.customization.show()

    def player_type_multi_clicked(self, button):
        print('Multi Player was chosen')  # put next window here
        self.player_type.hide()
        self.customization.show()

    def player_type_back_clicked(self, button):
        print("This should go back to Game Choice Window")
        self.player_type.hide()
        self.game_choice_box.show()

    def customization_back_clicked(self, button):
        print("This should go back to Game Choice Window")
        self.customization.hide()
        self.player_type.show()

    def customization_start_clicked(self, button):
        print("This should go to Board Window")
        # TODO: allow for users to set game type, right now hard coded as checkers
        self.customization.hide()
        # board = BoardWindow(self.__game, self.__game_type)

        piece_colour=0
        while (piece_colour!=len(self.customization.piece_radio_buttons)):
            if (self.customization.piece_radio_buttons[piece_colour].get_active()):
                break
            piece_colour += 1
        
        temp_game = Game(self.game_type, piece_colour)

        t1 = Timer(70, True)
        t2 = Timer(70, True)
        temp_game.build_light_player("light_player", PlayerType.HUMAN, t1)
        temp_game.build_dark_player("dark player", PlayerType.HUMAN, t2)
        # temp_game.get_light_player().__piece_set.__colour = "White"
        #                                                   \/ should it?
        # TODO: the game should be setup way earlier in the UI, this is jsut a placeholder
        # TODO: MOVE THIS WHEN THE OTHER UI WINDOWS ARE FUNCTIONAL
        self.board = BoardGrid("Test", "multiplayer", temp_game)
        self.grid.attach(self.board, 0, 0, 1, 1)
        self.board.show()
