# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import gi
from Pieces import King, Queen, Knight, Bishop, Rook, Pawn

from Colours import ColourOffset, COLOUR_STRING_LOOK_UP_TABLE
from UIHowToPlayWindow import HowToPlayWindow
gi.require_version("Gtk", "3.0")
gi.require_version("Rsvg", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Rsvg, GLib
from GameType import GameType

import cairo
import build_list_of_moves

SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2


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
        while svglc != 6:
            # read binary to ensure no nonsense on windows
            fp = open(svg_targets[svglc], "rb")
            fp.seek(0, SEEK_END)
            fps = fp.tell()
            fp.seek(0, SEEK_SET)
            chess_svg_light_data_array.append(fp.read(fps))
            fp.close()
            svglc += 1
        while svglc != len(svg_targets):
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
                        if isinstance(cur_piece, King):
                            if (cur_piece.get_colour() == self.__game_obj.get_light_player().get_colour()):
                                piece_to_draw = self.wk
                            else:
                                piece_to_draw = self.bk
                        elif isinstance(cur_piece, Queen):
                            if (cur_piece.get_colour() == self.__game_obj.get_light_player().get_colour()):
                                piece_to_draw = self.wq
                            else:
                                piece_to_draw = self.bq
                        elif isinstance(cur_piece, Knight):
                            if (cur_piece.get_colour() == self.__game_obj.get_light_player().get_colour()):
                                piece_to_draw = self.wn
                            else:
                                piece_to_draw = self.bn
                        elif isinstance(cur_piece, Bishop):
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
                        if (cur_piece.is_promoted()):  # 1 is king
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
