# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import gi
from Player import Player
from PlayerType import PlayerType
from Game import Game
from Pieces import King, Queen, Knight, Bishop, Rook, Pawn, CheckersCoin
from PieceSet import PieceSet
from Timer import Timer
from Colours import ColourCodes, ColourBoardCodes, ColourOffset, COLOUR_STRING_LOOK_UP_TABLE, \
    COLOUR_BOARD_STRING_LOOK_UP_TABLE

gi.require_version("Gtk", "3.0")
gi.require_version("Rsvg", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Rsvg, GLib
from GameType import GameType
from datetime import datetime
import cairo
import build_list_of_moves
import os

# make c-stdlib style definitions so
# the code is readable and without
# magic numbers
SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2

resume = True


class TheWindow(Gtk.Window):
    def __init__(self, directory):
        Gtk.Window.__init__(self, title="Main Menu")
        self.set_border_width(70)
        self.set_position(Gtk.WindowPosition.CENTER)
        col = Gdk.Color(2000, 6000, 200)  # dark green
        self.modify_bg(Gtk.StateType.NORMAL, col)

        self.has_chess_save = 0
        self.has_checkers_save = 0

        if (os.path.exists(directory + "/savedGame.cmpt370chess")):
            self.has_chess_save = 1
        if (os.path.exists(directory + "/savedGame.cmpt370checkrs")):
            self.has_checkers_save = 1
        self.main_box = MainMenuBox(
            self.has_chess_save, self.has_checkers_save)
        if (self.has_chess_save or self.has_checkers_save):
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
        if (self.has_chess_save):
            self.resume_choice_box.chess_button.connect(
                "clicked", self.resume_choice_chess_clicked)
        if (self.has_checkers_save):
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
        print('Chess was chosen')  # put next window here
        self.game_type = GameType.CHESS
        self.game_choice_box.hide()
        self.player_type.show()

    def resume_choice_checkers_clicked(self, button):
        print('Checkers was chosen')  # put next window here
        self.game_type = GameType.CHECKERS
        self.game_choice_box.hide()
        self.player_type.show()

    def resume_choice_back_clicked(self, button):
        print("This should go back to Main Menu Window")
        self.game_choice_box.hide()
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
        self.game_type.show()

    def customization_back_clicked(self, button):
        print("This should go back to Game Choice Window")
        self.customization.hide()
        self.player_type.show()

    def customization_start_clicked(self, button):
        print("This should go to Board Window")
        # TODO: allow for users to set game type, right now hard coded as checkers
        self.customization.hide()
        # board = BoardWindow(self.__game, self.__game_type)
        game_type = 1
        temp_game = Game(game_type, ColourCodes.RED_BLACK)
        t1 = Timer(900, True)
        t2 = Timer(900, True)
        temp_game.build_light_player("light_player", PlayerType.HUMAN, t1)
        temp_game.build_dark_player("dark player", PlayerType.HUMAN, t2)
        # temp_game.get_light_player().__piece_set.__colour = "White"
        #                                                   \/ should it?
        # TODO: the game should be setup way earlier in the UI, this is jsut a placeholder
        # TODO: MOVE THIS WHEN THE OTHER UI WINDOWS ARE FUNCTIONAL
        self.board = BoardGrid("Test", "multiplayer", temp_game)
        self.grid.attach(self.board, 0, 0, 1, 1)
        self.board.show()


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

        if (has_chess_save or has_checkers_save):
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


class ResumeChoiceBox(Gtk.Box):
    def __init__(self, has_chess_save, has_checkers_save):
        Gtk.Box.__init__(
            self, orientation=Gtk.Orientation.VERTICAL, spacing=10)

        if (has_chess_save):
            self.chess_button = Gtk.Button.new_with_label("Chess")
            self.chess_button.set_property("width-request", 300)
            self.chess_button.set_property("height-request", 100)
            self.pack_start(self.chess_button, True, True, 0)

        if (has_checkers_save):
            self.checkers_button = Gtk.Button.new_with_label("Checkers")
            self.checkers_button.set_property("width-request", 300)
            self.checkers_button.set_property("height-request", 100)
            self.pack_start(self.checkers_button, True, True, 0)

        self.back_button = Gtk.Button.new_with_label("Back")
        self.pack_start(self.back_button, True, True, 0)

        # fixed the exit stalling problem
        self.connect("destroy", Gtk.main_quit)


class GameChoiceBox(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(
            self, orientation=Gtk.Orientation.VERTICAL, spacing=10)

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

        # fixed the exit stalling problem
        self.connect("destroy", Gtk.main_quit)


class PlayerTypeBox(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(
            self, orientation=Gtk.Orientation.VERTICAL, spacing=10)

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


class CustomizationGrid(Gtk.Grid):
    def __init__(self):  # , game, game_type):
        # self.__game = game
        # self.__game_type = game_type

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
        while (x != len(COLOUR_STRING_LOOK_UP_TABLE)):
            self.piece_radio_buttons.append(Gtk.RadioButton.new_with_label_from_widget(
                self.piece_radio_buttons[0],
                COLOUR_STRING_LOOK_UP_TABLE[x][ColourOffset.OFFSET_LIGHT] + " " + COLOUR_STRING_LOOK_UP_TABLE[x][
                    ColourOffset.OFFSET_DARK]))
            x += 1
        x = 0
        while (x != len(COLOUR_STRING_LOOK_UP_TABLE)):
            self.attach(self.piece_radio_buttons[x], 0, 2 + x, 1, 1)
            self.piece_radio_buttons[x].override_color(
                Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
            x += 1

        x = 0
        self.board_radio_buttons = []
        self.board_radio_buttons.append(Gtk.RadioButton.new_with_label(None, COLOUR_BOARD_STRING_LOOK_UP_TABLE[x][
            ColourOffset.OFFSET_LIGHT] + " " + COLOUR_BOARD_STRING_LOOK_UP_TABLE[x][ColourOffset.OFFSET_DARK]))
        x += 1
        while (x != len(COLOUR_BOARD_STRING_LOOK_UP_TABLE)):
            self.board_radio_buttons.append(Gtk.RadioButton.new_with_label_from_widget(self.board_radio_buttons[0],
                                                                                       COLOUR_BOARD_STRING_LOOK_UP_TABLE[
                                                                                           x][
                                                                                           ColourOffset.OFFSET_LIGHT] + " " +
                                                                                       COLOUR_BOARD_STRING_LOOK_UP_TABLE[
                                                                                           x][
                                                                                           ColourOffset.OFFSET_DARK]))
            x += 1
        x = 0
        while (x != len(COLOUR_BOARD_STRING_LOOK_UP_TABLE)):
            self.attach(self.board_radio_buttons[x], 4, 2 + x, 1, 1)
            self.board_radio_buttons[x].override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
            x += 1

        self.back_button = Gtk.Button.new_with_label("Back")
        self.attach(self.back_button, 0, 8, 1, 1)

        self.start_button = Gtk.Button.new_with_label("Start")
        self.attach(self.start_button, 4, 8, 1, 1)

    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "on"
            # self.colour()
        else:
            state = "off"
        print(name, "was turned", state)


class BoardGrid(Gtk.Grid):
    def __init__(self, game, game_type, game_obj):
        """
        @param game_obj: actual game object, initialize by Game()
        @attribute current_selected_piece: Piece obejct, last clicked on piece
        @attribute possible_moves_for_cur_piece: list
        """
        Gtk.Grid.__init__(self)
        self.__game = game
        self.__game_obj = game_obj
        self.place_pieces()
        self.surface = None
        # save the selected piece so we can check if they click on a possible
        # moves for that piece
        self.current_selected_location = None
        self.possible_moves_for_cur_piece = []
        # create checkerboard area
        board_frame = Gtk.Frame()
        board_frame.set_shadow_type(Gtk.ShadowType.IN)
        self.add(board_frame)

        checkerboard_area = Gtk.DrawingArea()
        checkerboard_area.set_size_request(400, 400)
        board_frame.add(checkerboard_area)
        checkerboard_area.connect('draw', self.checkerboard_draw_event)
        checkerboard_area.connect(
            'configure-event', self.click_configure_event)
        checkerboard_area.connect('button-press-event', self.mouse_press_event)
        checkerboard_area.set_events(checkerboard_area.get_events()
                                     | Gdk.EventMask.LEAVE_NOTIFY_MASK
                                     | Gdk.EventMask.BUTTON_PRESS_MASK)

        self.timer_area = Gtk.Label()  # Player 1 time
        self.add(self.timer_area)
        self.timer_area_2 = Gtk.Label()  # Player 2 time
        self.attach_next_to(self.timer_area_2, self.timer_area, Gtk.PositionType.RIGHT, 3, 1)

        player1_label = Gtk.Label()  # Label for Player 1 timer
        player1_label.set_markup("<b>Player 1 Time Remaining</b>")
        player1_label.set_justify(Gtk.Justification.CENTER)
        player1_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        self.attach_next_to(player1_label, self.timer_area, Gtk.PositionType.TOP, 1, 1)

        player2_label = Gtk.Label()  # Label for Player 2 timer
        player2_label.set_markup("<b>Player 2 Time Remaining</b>")
        player2_label.set_justify(Gtk.Justification.CENTER)
        player2_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        self.attach_next_to(player2_label, player1_label, Gtk.PositionType.RIGHT, 1, 1)

        # just to see if promotion works
        # promote_button = Gtk.Button.new_with_label("promote?")
        # promote_button.connect("clicked", self.promote_clicked)
        # board_box.attach_next_to(promote_button, help_button, Gtk.PositionType.RIGHT, 1, 1)

        self.help_button = Gtk.Button.new_with_label("Help?")
        self.help_button.connect("clicked", self.help_clicked)
        self.attach(self.help_button,1 ,4, 1, 1)

        self.save_quit_button = Gtk.Button.new_with_label("Save and Quit")
        self.save_quit_button.connect("clicked", self.save_quit_clicked)
        self.attach(self.save_quit_button, 2, 5, 1, 1)

        self.start_clock_timer()  # start the Timer
        self.show_all()
        self.connect('destroy', Gtk.main_quit)

        chess_svg_light_data_array = []
        chess_svg_dark_data_array = []
        svg_targets = ["media/gfx/regular/wk.svg",
                       "media/gfx/regular/wq.svg",
                       "media/gfx/regular/wn.svg",
                       "media/gfx/regular/wb.svg",
                       "media/gfx/regular/wr.svg",
                       "media/gfx/regular/wp.svg",
                       "media/gfx/regular/bk.svg",
                       "media/gfx/regular/bq.svg",
                       "media/gfx/regular/bn.svg",
                       "media/gfx/regular/bb.svg",
                       "media/gfx/regular/br.svg",
                       "media/gfx/regular/bp.svg"]

        # load the data
        svglc = 0
        while (svglc != 6):
            # read binary to ensure no nonsense on windows
            fp = open(svg_targets[svglc], "rb")
            fp.seek(0, SEEK_END)
            fps = fp.tell()
            fp.seek(0, SEEK_SET)
            chess_svg_light_data_array.append(fp.read(fps))
            fp.close()
            svglc += 1
        while (svglc != len(svg_targets)):
            # read binary to ensure no nonsense on windows
            fp = open(svg_targets[svglc], "rb")
            fp.seek(0, SEEK_END)
            fps = fp.tell()
            fp.seek(0, SEEK_SET)
            chess_svg_dark_data_array.append(fp.read(fps))
            fp.close()
            svglc += 1
        assert (len(chess_svg_light_data_array)
                == len(chess_svg_dark_data_array))

        # replace the colours
        svglc = 0
        while (svglc != len(chess_svg_light_data_array)):
            chess_svg_light_data_array[svglc] = chess_svg_light_data_array[svglc].replace(
                b"f9f9f9",
                COLOUR_STRING_LOOK_UP_TABLE[self.__game_obj.get_colour_mode()][ColourOffset.OFFSET_LIGHT_HEX])
            svglc += 1
        svglc = 0
        while (svglc != len(chess_svg_dark_data_array)):
            chess_svg_dark_data_array[svglc] = chess_svg_dark_data_array[svglc].replace(
                b"000000", COLOUR_STRING_LOOK_UP_TABLE[self.__game_obj.get_colour_mode()][ColourOffset.OFFSET_DARK_HEX])
            svglc += 1

        # get light handles
        self.wk = Rsvg.Handle.new_from_data(chess_svg_light_data_array[0])
        self.wq = Rsvg.Handle.new_from_data(chess_svg_light_data_array[1])
        self.wn = Rsvg.Handle.new_from_data(chess_svg_light_data_array[2])
        self.wb = Rsvg.Handle.new_from_data(chess_svg_light_data_array[3])
        self.wr = Rsvg.Handle.new_from_data(chess_svg_light_data_array[4])
        self.wp = Rsvg.Handle.new_from_data(chess_svg_light_data_array[5])

        # get dark handels
        self.bk = Rsvg.Handle.new_from_data(chess_svg_dark_data_array[0])
        self.bq = Rsvg.Handle.new_from_data(chess_svg_dark_data_array[1])
        self.bn = Rsvg.Handle.new_from_data(chess_svg_dark_data_array[2])
        self.bb = Rsvg.Handle.new_from_data(chess_svg_dark_data_array[3])
        self.br = Rsvg.Handle.new_from_data(chess_svg_dark_data_array[4])
        self.bp = Rsvg.Handle.new_from_data(chess_svg_dark_data_array[5])

        # checkers
        checkers_svg_data_array = []
        svg_targets = ["media/gfx/checkers/wc.svg",
                       "media/gfx/checkers/wd.svg",
                       "media/gfx/checkers/bc.svg",
                       "media/gfx/checkers/bd.svg"]
        svglc = 0
        while (svglc != len(svg_targets)):
            # read binary to ensure no nonsense on windows
            fp = open(svg_targets[svglc], "rb")
            fp.seek(0, SEEK_END)
            fps = fp.tell()
            fp.seek(0, SEEK_SET)
            checkers_svg_data_array.append(fp.read(fps))
            fp.close()
            svglc += 1
        # replace the colours
        svglc = 0
        while (svglc != len(checkers_svg_data_array)):
            checkers_svg_data_array[svglc] = checkers_svg_data_array[svglc].replace(
                b"f9f9f9",
                COLOUR_STRING_LOOK_UP_TABLE[self.__game_obj.get_colour_mode()][ColourOffset.OFFSET_LIGHT_HEX])
            checkers_svg_data_array[svglc] = checkers_svg_data_array[svglc].replace(
                b"000000", COLOUR_STRING_LOOK_UP_TABLE[self.__game_obj.get_colour_mode()][ColourOffset.OFFSET_DARK_HEX])
            svglc += 1

        self.wc = Rsvg.Handle.new_from_data(checkers_svg_data_array[0])
        self.wd = Rsvg.Handle.new_from_data(checkers_svg_data_array[1])
        self.bc = Rsvg.Handle.new_from_data(checkers_svg_data_array[2])
        self.bd = Rsvg.Handle.new_from_data(checkers_svg_data_array[3])

    def place_pieces(self):
        """
        place the pieces on the board, stored in game->board
        first try to load from file, if file does not exist, build starting board
        """
        try:
            self.__game_obj.load_from_file()
            return
        except:
            print("no save file found")

        if self.__game_obj.get_game_type() == 0:
            print("is Chess")
            pcs_player1 = self.__game_obj.get_light_player().get_piece_set()
            pcs_player2 = self.__game_obj.get_dark_player().get_piece_set()
            self.__game_obj.get_board().build_chess_board(
                pcs_player1.get_live_pieces(), pcs_player2.get_live_pieces())

        if self.__game_obj.get_game_type() == 1:
            print("is Checkers")
            pcs_player1 = self.__game_obj.get_light_player().get_piece_set()
            pcs_player2 = self.__game_obj.get_dark_player().get_piece_set()
            self.__game_obj.get_board().build_checkers_board(
                pcs_player1.get_live_pieces(), pcs_player2.get_live_pieces())

    def checkerboard_draw_event(self, checkerboard_area, cairo_ctx):

        # At the start of a draw handler, a clip region has been set on
        # the Cairo context, and the contents have been cleared to the
        # widget's background color. The docs for
        # gdk_window_begin_paint_region() give more details on how this
        # works.
        check_size = 50
        spacing = 0

        xcount = 0
        i = spacing
        width = checkerboard_area.get_allocated_width()
        height = checkerboard_area.get_allocated_height()

        cairo_ctx.save()

        while i < width:
            j = spacing
            ycount = xcount % 2  # start with even/odd depending on row
            while j < height:
                if ycount % 2:
                    cairo_ctx.set_source_rgb(0.300, .155, 0.119)
                else:
                    cairo_ctx.set_source_rgb(0, 1, 1)
                # If we're outside the clip this will do nothing.
                cairo_ctx.rectangle(i, j,
                                    check_size,
                                    check_size)
                cairo_ctx.fill()

                j += check_size + spacing
                ycount += 1

            i += check_size + spacing
            xcount += 1

            game_type = self.__game_obj.get_game_type()

        cairo_ctx.restore()
        row = 0
        while (row != self.__game_obj.get_board().get_size()):
            col = 0
            while (col != self.__game_obj.get_board().get_size()):
                cur_piece = self.__game_obj.get_board().get_game_square(
                    row, col).get_occupying_piece()

                if (not (cur_piece is None)):
                    if (game_type == GameType.CHESS):
                        if (isinstance(cur_piece, King)):
                            if (cur_piece.get_colour() == self.__game_obj.get_light_player().get_colour()):
                                piece_to_draw = self.wk
                            else:
                                piece_to_draw = self.bk
                        elif (isinstance(cur_piece, Queen)):
                            if (cur_piece.get_colour() == self.__game_obj.get_light_player().get_colour()):
                                piece_to_draw = self.wq
                            else:
                                piece_to_draw = self.bq
                        elif (isinstance(cur_piece, Knight)):
                            if (cur_piece.get_colour() == self.__game_obj.get_light_player().get_colour()):
                                piece_to_draw = self.wn
                            else:
                                piece_to_draw = self.bn
                        elif (isinstance(cur_piece, Bishop)):
                            if (cur_piece.get_colour() == self.__game_obj.get_light_player().get_colour()):
                                piece_to_draw = self.wb
                            else:
                                piece_to_draw = self.bb
                        elif (isinstance(cur_piece, Rook)):
                            if (cur_piece.get_colour() == self.__game_obj.get_light_player().get_colour()):
                                piece_to_draw = self.wr
                            else:
                                piece_to_draw = self.br
                        elif (isinstance(cur_piece, Pawn)):
                            if (cur_piece.get_colour() == self.__game_obj.get_light_player().get_colour()):
                                piece_to_draw = self.wp
                            else:
                                piece_to_draw = self.bp
                    elif (game_type == GameType.CHECKERS):
                        if (cur_piece.get_promotion_status()):  # 1 is king
                            if (cur_piece.get_colour() == self.__game_obj.get_light_player().get_colour()):
                                piece_to_draw = self.wd
                            else:
                                piece_to_draw = self.bd
                        else:
                            if (cur_piece.get_colour() == self.__game_obj.get_light_player().get_colour()):
                                piece_to_draw = self.wc
                            else:
                                piece_to_draw = self.bc

                    else:
                        assert (0)
                    cairo_ctx.save()
                    # scale piece to size of square
                    cairo_ctx.scale(50 / piece_to_draw.get_dimensions().width,
                                    50 / piece_to_draw.get_dimensions().height)
                    cairo_ctx.translate(piece_to_draw.get_dimensions(
                    ).width * col, piece_to_draw.get_dimensions().height * row)
                    piece_to_draw.render_cairo(cairo_ctx)
                    cairo_ctx.restore()
                col += 1
            row += 1

        return True

    def mouse_pointer(self, widget, x, y):
        # this might need to be used since it cant work without this but it works with nothing in it
        pass

    def click_configure_event(self, checkerboard_area, event):

        allocation = checkerboard_area.get_allocation()
        self.surface = checkerboard_area.get_window().create_similar_surface(cairo.CONTENT_COLOR,
                                                                             allocation.width,
                                                                             allocation.height)

        cairo_ctx = cairo.Context(self.surface)
        cairo_ctx.set_source_rgb(1, 1, 1)
        cairo_ctx.paint()

        return True

    def mouse_press_event(self, checkerboard_area, event):
        """
        handles mouse press events on the board grid
        returns False on Failure
        """

        if self.surface is None:  # paranoia check, in case we haven't gotten a configure event
            return False

        if event.button == 1:
            # click registered
            self.mouse_pointer(checkerboard_area, event.x, event.y)
            cur_piece = current_selected_piece = self.__game_obj.get_board().get_game_square(
                int(event.y // 50), int(event.x // 50)).get_occupying_piece()

            cur_location = current_selected_piece = self.__game_obj.get_board(
            ).get_game_square(int(event.y // 50), int(event.x // 50))

            if cur_piece is not None:
                print(cur_piece.get_colour())
            print(self.__game_obj.get_light_player().get_piece_set().get_colour())

            print(self.__game_obj.get_dark_player().get_piece_set().get_colour())
            # check if making a move
            if cur_location in self.possible_moves_for_cur_piece:
                # move the piece
                print(self.current_selected_location)
                print(cur_location)
                self.__game_obj.get_current_player().make_move(
                    self.current_selected_location, cur_location, self.__game_obj)
                print("Made Move")
                checkerboard_area.queue_draw()
                # switch players, flip board
                self.__game_obj.change_current_player()
                # change the timer to other player
                if self.__game_obj.get_current_player() is self.__game_obj.get_dark_player():
                    self.__game_obj.get_light_player().get_timer().stop()
                    self.__game_obj.get_dark_player().get_timer().start()
                else:
                    self.__game_obj.get_light_player().get_timer().start()
                    self.__game_obj.get_dark_player().get_timer().stop()
                self.__game_obj.get_board().switch_sides()

                # reset attributes
                self.current_selected_location = None
                self.possible_moves_for_cur_piece = []

            # not making a move, so set attributes and build possible moves for next click
            else:
                if cur_piece is None:
                    return
                self.current_selected_location = cur_location
                # build the possible pieces for a game square
                self.possible_moves_for_cur_piece = build_list_of_moves.build_list_of_moves(
                    cur_location, self.__game_obj)
                # TODO: check return value of above line, display somehow

    def create_location_list(self, size):
        """
        creates a 2d list of size n where each i in the list is [x, y] and
        denotes a location to be placed on the UI window
        this is for locations the mouse will click on the grid, to later be
        indexed to get gamesquare at that grid location
        @return: 2d list of integers
        """
        cur_length = 50
        rv_list = []

        for i in range(size):
            col_list = []
            cur_width = 50
            for j in range(size):
                col_list.append([cur_width, cur_length])
                cur_width += 50
            cur_length += 50
            rv_list.append(col_list)

        return rv_list

    def display_timer(self):
        # needs to have True or it only runs once

        # get the minutes from Players' time remaining
        player1_time = int(self.__game_obj.get_light_player().get_timer().get_time_remaining_s() // 60)
        player2_time = int(self.__game_obj.get_dark_player().get_timer().get_time_remaining_s() // 60)
        # get the seconds from Player's time remaining
        player1_time_sec = int(self.__game_obj.get_light_player().get_timer().get_time_remaining_s() % 60)
        player2_time_sec = int(self.__game_obj.get_dark_player().get_timer().get_time_remaining_s() % 60)

        p1_time = "{:2d}:{:02d}".format(player1_time, player1_time_sec)  # format the minutes and seconds to be
        p2_time = "{:2d}:{:02d}".format(player2_time, player2_time_sec)  # normal clock looking

        # bold the times and set them to be white
        self.timer_area.set_markup("<b>" + p1_time + "</b>")
        self.timer_area.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        self.timer_area_2.set_markup("<b>" + p2_time + "</b>")
        self.timer_area_2.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        return True

        # Initialize Timer
    def start_clock_timer(self):
        if self.__game_obj.get_current_player() is self.__game_obj.get_light_player():
            self.__game_obj.get_light_player().get_timer().start()
            GLib.timeout_add(1000, self.display_timer)
        else:
            self.__game_obj.get_dark_player().get_timer().start()
            GLib.timeout_add(1000, self.display_timer)

    def help_clicked(self, button):
        print("This should go to HowToPlay Window")
        # self.__game_obj.get_light_player().get_timer().stop()
        # self.__game_obj.get_dark_player().get_timer().stop()
        board = HowToPlayWindow(self.__game)
        board.show_all()
        # self.hide()

    def promote_clicked(self, button):
        print("This should go to PromotePawn Window")
        self.__game_obj.get_light_player().get_timer().stop()
        self.__game_obj.get_dark_player().get_timer().stop()
        board = PromotePawnWindow()
        board.show_all()
        # self.hide()

    def save_quit_clicked(self, button):
        print("This should exit")
        Gtk.main_quit()



class HowToPlayWindow(Gtk.Window):
    def __init__(self, game):
        Gtk.Window.__init__(self, title="How to Play " + game)
        self.set_border_width(50)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(200, 400)
        col = Gdk.Color(2000, 6000, 200)
        self.modify_bg(Gtk.StateType.NORMAL, col)
        help_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(help_box)
        # if we want there to be text in the window

        scrolled = Gtk.ScrolledWindow(vexpand=True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        label = Gtk.Label()
        if game == "Chess":
            file = open("chessrules.txt", encoding="utf8")
            chess_rules = file.read()
            label.set_markup(chess_rules)
        else:
            file = open("checkersrules.txt", encoding="utf8")
            checkers_rules = file.read()
            label.set_markup(checkers_rules)

        label.override_color(Gtk.StateFlags.NORMAL,
                             Gdk.RGBA(1.0, 1.0, 1.0, 1.0))

        scrolled.add(label)
        help_box.add(scrolled)

        # this gives error message but still does it??
        self.connect("destroy", self.hide)
    # implement this when fixed the parent problem
    """def closed(self):
        BoardGrid.__game_obj.get_light_player().get_timer().start()
        BoardGrid.__game_obj.get_dark_player().get_timer().start()
        self.hide()"""


class PromotePawnWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Choose Promotion ")
        self.set_border_width(50)
        self.set_position(Gtk.WindowPosition.CENTER)
        col = Gdk.Color(2000, 6000, 200)  # dark green
        self.modify_bg(Gtk.StateType.NORMAL, col)
        promote_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.add(promote_box)

        queen_button = Gtk.Button.new_with_label("Queen")
        queen_button.connect("clicked", self.queen_clicked)

        knight_button = Gtk.Button.new_with_label("Knight")
        knight_button.connect("clicked", self.knight_clicked)

        bishop_button = Gtk.Button.new_with_label("Bishop")
        bishop_button.connect("clicked", self.bishop_clicked)

        rook_button = Gtk.Button.new_with_label("Queen")
        rook_button.connect("clicked", self.rook_clicked)

        promote_box.add(queen_button)
        promote_box.add(knight_button)
        promote_box.add(bishop_button)
        promote_box.add(rook_button)
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


class PlayAgainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Play Again?")
        self.set_border_width(70)
        self.set_position(Gtk.WindowPosition.CENTER)
        col = Gdk.Color(2000, 6000, 200)
        self.modify_bg(Gtk.StateType.NORMAL, col)
        # b = Button()
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)
        # self.add(b)
        chess_button = Gtk.Button.new_with_label("Play Again")
        chess_button.connect("clicked", self.play_clicked)
        chess_button.set_property("width-request", 300)
        chess_button.set_property("height-request", 100)
        main_box.pack_start(chess_button, True, True, 0)

        chess_button = Gtk.Button.new_with_label("Main Menu")
        chess_button.connect("clicked", self.main_menu_clicked)
        chess_button.set_property("width-request", 300)
        chess_button.set_property("height-request", 100)
        main_box.pack_start(chess_button, True, True, 0)

        back_button = Gtk.Button.new_with_mnemonic("_Exit")
        back_button.connect("clicked", self.exit_clicked)
        main_box.pack_start(back_button, True, True, 0)

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
        main_menu = MainMenuBox()
        main_menu.show_all()
        self.hide()

    def exit_clicked(self, button):
        print("This should exit")
        Gtk.main_quit()


def initializeFS():
    """initialize filesystem for storing stuff
    :returns: directory string"""
    if (os.name == "posix"):
        home = os.path.expanduser("~")
        if (not (os.path.exists(home + "/.cmpt370checkerschess"))):
            os.mkdir(home + "/.cmpt370checkerschess")
        return (home + "/.cmpt370checkerschess")
    elif (os.name == "nt"):
        app_data = os.getenv("LOCALAPPDATA")
        if (not (os.path.exists(app_data + "/.cmpt370checkerschess"))):
            os.mkdir(app_data + "/.cmpt370checkerschess")
        return (app_data + "/.cmpt370checkerschess")
    else:
        print("uknown os")
        return


if __name__ == "__main__":
    win = TheWindow(initializeFS())
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    win.game_choice_box.hide()
    win.resume_choice_box.hide()
    win.player_type.hide()
    win.customization.hide()
    Gtk.main()
