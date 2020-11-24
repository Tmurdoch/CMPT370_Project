import gi
import math
from datetime import datetime
from Player import Player
from Timer import Timer
from PlayerType import PlayerType
from Colours import ColourCodes, ColourBoardCodes, ColourOffset, COLOUR_STRING_LOOK_UP_TABLE, COLOUR_BOARD_STRING_LOOK_UP_TABLE
gi.require_version("Gtk", "3.0")
gi.require_version('Rsvg', '2.0')
from gi.repository import Gtk, Gdk, GdkPixbuf,GObject, Rsvg, GLib
import cairo

from GameType import GameType


# Globals for initializing objects
resume = True
current = "Player 1"
player_1_timer = Timer(900, True)
player_2_timer = Timer(900, True)
player_2_type = None
game_type = None


class TheWindow(Gtk.Window):
        def __init__(self):
                Gtk.Window.__init__(self, title="Main Menu")
                self.set_border_width(60)
                self.set_position(Gtk.WindowPosition.CENTER)
                col = Gdk.Color(2000, 6000, 200)  # dark green
                self.modify_bg(Gtk.StateType.NORMAL, col)

                self.main_box = MainMenuBox()
                self.main_box.play_button.connect("clicked", self.main_play_clicked)
                if resume:
                        self.main_box.resume_button.connect("clicked", self.main_resume_clicked)

                self.game_choice_box = GameChoiceBox()
                self.game_choice_box.chess_button.connect("clicked", self.game_choice_chess_clicked)
                self.game_choice_box.checkers_button.connect("clicked", self.game_choice_checkers_clicked)
                self.game_choice_box.back_button.connect("clicked", self.game_choice_back_clicked)

                self.player_type = PlayerTypeBox()
                self.player_type.single_button.connect("clicked", self.player_type_single_clicked)
                self.player_type.multiplayer_button.connect("clicked", self.player_type_multi_clicked)
                self.player_type.back_button.connect("clicked", self.player_type_back_clicked)

                self.customization = CustomizationGrid()
                self.customization.back_button.connect("clicked", self.customization_back_clicked)
                self.customization.start_button.connect("clicked", self.customization_start_clicked)

                self.board = BoardGrid("Chess", "SinglePlayer")
                self.board.help_button.connect("clicked", self.board_help_clicked)
                self.board.save_quit_button.connect("clicked", self.board_save_clicked)
                self.board.pause_button.connect("clicked", self.pause_clicked)

                self.grid = Gtk.Grid()
                self.grid.attach(self.main_box, 0, 0, 1, 1)
                self.grid.attach(self.game_choice_box, 0, 0, 1, 1)
                self.grid.attach(self.player_type, 0, 0, 1, 1)
                self.grid.attach(self.customization, 0, 0, 1, 1)
                self.grid.attach(self.board, 0, 0, 1, 1)

                self.add(self.grid)
                self.board.hide()
                self.main_box.show()

                self.connect("destroy", Gtk.main_quit)  # fixed the exit stalling problem

        def main_play_clicked(self, button):
                print('Play was chosen')
                self.main_box.hide()
                self.game_choice_box.show()

        def main_resume_clicked(self, button):
                print('This should go to resumed game')
                return

        def game_choice_chess_clicked(self, button):
                print('Chess was chosen')  # put next window here
                game_type = GameType.CHESS
                self.game_choice_box.hide()
                self.player_type.show()

        def game_choice_checkers_clicked(self, button):
                print('Checkers was chosen')  # put next window here
                game_type = GameType.CHECKERS
                print(game_type)
                self.game_choice_box.hide()
                self.player_type.show()

                self.board.hide()

        def game_choice_back_clicked(self, button):
                print("This should go back to Main Menu Window")
                self.game_choice_box.hide()
                self.main_box.show_all()

        def player_type_single_clicked(self, button):
                print('Single Player was chosen')  # put next window here
                player_2_type = PlayerType.AI
                #print(player_2_type)
                self.player_type.hide()
                self.customization.show()

        def player_type_multi_clicked(self, button):
                print('Multi Player was chosen')  # put next window here
                player_2_type = PlayerType.HUMAN
                self.player_type.hide()
                self.customization.show()

        def player_type_back_clicked(self, button):
                print("This should go back to Game Choice Window")
                self.player_type.hide()
                self.game_choice_box.show_all()

        def customization_back_clicked(self, button):
                print("This should go back to Game Choice Window")
                self.customization.hide()
                self.player_type.show_all()

        def customization_start_clicked(self, button):
                print("This should go to Board Window")
                BoardGrid.start_clock_timer(self.board)
                self.customization.hide()
                self.board.show()

        def board_save_clicked(self, button):
                print("This should exit and save")
                Gtk.main_quit()

        def pause_clicked(self, button):
                player_1_timer.stop()
                player_2_timer.stop()

        def board_help_clicked(self, button):
                print("This should go to Help Window")
                board = HowToPlayWindow("Chess")
                board.show_all()


class MainMenuBox(Gtk.Box):
        def __init__(self):
                Gtk.Box.__init__(self,orientation=Gtk.Orientation.VERTICAL, spacing=10)
                # self.add(b)
                self.play_button = Gtk.Button.new_with_label("Play")
                #chess_button.connect("clicked", self.play_clicked)
                self.play_button.set_property("width-request", 300)
                self.play_button.set_property("height-request", 100)
                self.pack_start(self.play_button, True, True, 0)
                if resume:
                        self.resume_button = Gtk.Button.new_with_label("Resume")
                        #checkers_button.connect("clicked", self.resume_clicked)
                        self.resume_button.set_property("width-request", 300)
                        self.resume_button.set_property("height-request", 100)
                        self.pack_start(self.resume_button, True, True, 0)
                back_button = Gtk.Button.new_with_mnemonic("_Exit")
                back_button.connect("clicked", self.exit_clicked)
                self.pack_start(back_button, True, True, 0)

        def exit_clicked(self, button):
                print("This should exit")
                Gtk.main_quit()


class GameChoiceBox(Gtk.Box):
        def __init__(self):
                Gtk.Box.__init__(self,orientation=Gtk.Orientation.VERTICAL, spacing=10)

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

                self.connect("destroy", Gtk.main_quit)  # fixed the exit stalling problem


class PlayerTypeBox(Gtk.Box):
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


class CustomizationGrid(Gtk.Grid):
    def __init__(self):
        #, game, game_type):
        #self.__game = game
        #self.__game_type = game_type

        Gtk.Grid.__init__(self)
        self.set_column_spacing(10)
        self.set_row_spacing(20)
        title = Gtk.Label()
        title.set_markup("<big>Customize your pieces and board!</big>")
        title.set_justify(Gtk.Justification.RIGHT)
        title.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        self.attach(title, 3, 0, 1, 1)

        # Pieces choices label
        label_piece = Gtk.Label()
        label_piece.set_markup("<b>Pieces</b>")
        # label_piece.set_justify(Gtk.Justification.CENTER)
        label_piece.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        self.attach(label_piece, 1, 1, 1, 1)

        # Board choices label
        label_board = Gtk.Label()
        label_board.set_markup("<b>Board</b>")
        label_board.set_justify(Gtk.Justification.CENTER)
        label_board.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        self.attach(label_board, 4, 1, 1, 1)

        x = 0
        self.piece_radio_buttons = []
        self.piece_radio_buttons.append(Gtk.RadioButton.new_with_label(None, COLOUR_STRING_LOOK_UP_TABLE[x][ColourOffset.OFFSET_LIGHT] + " " + COLOUR_STRING_LOOK_UP_TABLE[x][ColourOffset.OFFSET_DARK]))
        x += 1
        while x != len(COLOUR_STRING_LOOK_UP_TABLE):
                self.piece_radio_buttons.append(Gtk.RadioButton.new_with_label_from_widget(self.piece_radio_buttons[0], COLOUR_STRING_LOOK_UP_TABLE[x][ColourOffset.OFFSET_LIGHT] + " " + COLOUR_STRING_LOOK_UP_TABLE[x][ColourOffset.OFFSET_DARK]))
                x += 1
        x = 0
        while x != len(COLOUR_STRING_LOOK_UP_TABLE):
                self.attach(self.piece_radio_buttons[x], 0, 2+x, 1, 1)
                self.piece_radio_buttons[x].override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
                x += 1

        x = 0
        self.board_radio_buttons = []
        self.board_radio_buttons.append(Gtk.RadioButton.new_with_label(None, COLOUR_BOARD_STRING_LOOK_UP_TABLE[x][ColourOffset.OFFSET_LIGHT] + " " + COLOUR_BOARD_STRING_LOOK_UP_TABLE[x][ColourOffset.OFFSET_DARK]))
        x += 1
        while x != len(COLOUR_BOARD_STRING_LOOK_UP_TABLE):
                self.board_radio_buttons.append(Gtk.RadioButton.new_with_label_from_widget(self.board_radio_buttons[0], COLOUR_BOARD_STRING_LOOK_UP_TABLE[x][ColourOffset.OFFSET_LIGHT] + " " + COLOUR_BOARD_STRING_LOOK_UP_TABLE[x][ColourOffset.OFFSET_DARK]))
                x += 1
        x = 0
        while x != len(COLOUR_BOARD_STRING_LOOK_UP_TABLE):
                self.attach(self.board_radio_buttons[x], 4, 2+x, 1, 1)
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
    def __init__(self, game, game_type):
        """
        @param game_obj: actual game object, initialize by Game()
        """
        Gtk.Grid.__init__(self)
        self.__game = game
        #self.__game_obj = game_obj
        self.surface = None

        col = Gdk.Color(2000, 6000, 200)
        self.modify_bg(Gtk.StateType.NORMAL, col)

        # create checkerboard area
        board_frame = Gtk.Frame()
        board_frame.set_shadow_type(Gtk.ShadowType.IN)
        self.add(board_frame)

        checkerboard_area = Gtk.DrawingArea()
        checkerboard_area.set_size_request(400, 400)
        board_frame.add(checkerboard_area)
        checkerboard_area.connect('draw', self.checkerboard_draw_event)
        checkerboard_area.connect('configure-event', self.click_configure_event)
        checkerboard_area.connect('button-press-event', self.mouse_press_event)
        checkerboard_area.set_events(checkerboard_area.get_events()
                                     | Gdk.EventMask.LEAVE_NOTIFY_MASK
                                     | Gdk.EventMask.BUTTON_PRESS_MASK)

        self.timer_area = Gtk.Label()   # Player 1 time
        self.add(self.timer_area)

        self.timer_area_2 = Gtk.Label()  # Player 2 time
        self.attach_next_to(self.timer_area_2, self.timer_area, Gtk.PositionType.RIGHT, 3, 1)

        player1_label = Gtk.Label()
        player1_label.set_markup("<b>Player 1 Time Remaining</b>")
        player1_label.set_justify(Gtk.Justification.CENTER)
        player1_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        self.attach_next_to(player1_label,self.timer_area, Gtk.PositionType.TOP, 1, 1)

        player2_label = Gtk.Label()
        player2_label.set_markup("<b>Player 2 Time Remaining</b>")
        player2_label.set_justify(Gtk.Justification.CENTER)
        player2_label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        self.attach_next_to(player2_label, player1_label, Gtk.PositionType.RIGHT, 1, 1)

        # just to see if promotion works
        # promote_button = Gtk.Button.new_with_label("promote?")
        # promote_button.connect("clicked", self.promote_clicked)
        # board_box.attach_next_to(promote_button, help_button, Gtk.PositionType.RIGHT, 1, 1)

        self.pause_button = Gtk.Button.new_with_label("Pause Timer")
        self.pause_button.connect("clicked", self.pause_clicked)
        self.attach(self.pause_button, 1, 4, 1, 1)

        self.resume_button = Gtk.Button.new_with_label("Resume Timer")
        self.resume_button.connect("clicked", self.resume_clicked)
        self.attach_next_to(self.resume_button,self.pause_button, Gtk.PositionType.BOTTOM, 1, 1)

        self.help_button = Gtk.Button.new_with_label("Help?")
        self.attach_next_to(self.help_button, self.pause_button,Gtk.PositionType.RIGHT, 1, 1)

        self.save_quit_button = Gtk.Button.new_with_label("Save and Quit")
        self.attach_next_to(self.save_quit_button, self.help_button, Gtk.PositionType.BOTTOM, 1, 1)

        self.show_all()
        self.connect('destroy', Gtk.main_quit)

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

        piece = Rsvg.Handle.new_from_file("C:/msys64/home/Joel/media/gfx/regular/wk.svg")
        #print(piece.get_dimensions().height, piece.get_dimensions().width)
        # piece.set_dpi((50/piece.get_dimensions().height)*300)
        cairo_ctx.scale(50 / piece.get_dimensions().width, 50 / piece.get_dimensions().height)
        #piece.render_cairo(cairo_ctx)
        cairo_ctx.translate(7000,7000)
        piece.render_cairo(cairo_ctx)

        return True

    def mouse_pointer(self, widget, x, y):
        # this might need to be used since it cant work without this but it works with nothing in it
        pass

    def click_configure_event(self, checkerboard_area, event):

        allocation = checkerboard_area.get_allocation()
        self.surface = checkerboard_area.get_window().create_similar_surface(cairo.CONTENT_COLOR,
                                                                             allocation.width,
                                                                             allocation.height)

        return True

    def mouse_press_event(self, checkerboard_area, event):
        """
        prints board coordinates for
        returns True on success
        False on Failure
        """
        if self.surface is None:
            return False

        if event.button == 1:
            self.mouse_pointer(checkerboard_area, event.x, event.y)
            print(event.x // 50,event.y // 50)

        return True

    def create_location_list(self, size):
        """
        creates a 2d list of size n where each i in the list is [x, y] and
        denotes a location to be placed on the UI window
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

        player1_time = player_1_timer.get_time_remaining_s() // 60  # get the minutes from Players' time remaining
        player1_time_sec = player_1_timer.get_time_remaining_s() % 60   # get the seconds from Player's time remaining
        player2_time = player_2_timer.get_time_remaining_s() // 60
        player2_time_sec = player_2_timer.get_time_remaining_s() % 60
        p1_time = "{:2d}:{:02d}".format(player1_time, player1_time_sec)  # format the minutes and seconds to be
        p2_time = "{:2d}:{:02d}".format(player2_time, player2_time_sec)  # normal clock looking

        # bold the times and set the to be white
        self.timer_area.set_markup("<b>"+p1_time+"</b>")
        self.timer_area.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        self.timer_area_2.set_markup("<b>" + p2_time + "</b>")
        self.timer_area_2.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        return True

        # Initialize Timer
    def start_clock_timer(self):
        if current == "Player 1":
            player_1_timer.start()
            GLib.timeout_add(1000, self.display_timer)
        else:
            player_2_timer.start()
            GLib.timeout_add(1000, self.display_timer)

    def pause_clicked(self, button):
        player_1_timer.stop()
        player_2_timer.stop()
        return True

    def resume_clicked(self, button):
        if current == "Player 1":
            player_1_timer.start()
        else:
            player_2_timer.start()
        return True

    def promote_clicked(self, button):
        print("This should go to PromotePawn Window")
        board = PromotePawnWindow()
        board.show_all()
        # self.hide()


class HowToPlayWindow(Gtk.Window):
    def __init__(self, game):
        Gtk.Window.__init__(self, title="How to Play " + game)
        self.set_border_width(50)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(200,400)
        col = Gdk.Color(2000, 6000, 200)
        self.modify_bg(Gtk.StateType.NORMAL, col)
        help_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(help_box)

        player_1_timer.stop()   # stop the timers while this is open, need to figure out to start again
        player_2_timer.stop()

        scrolled = Gtk.ScrolledWindow(vexpand=True)
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        label = Gtk.Label()

        # temporary to see if it worked
        if game == "Chess":
            file = open("chessrules.txt", encoding="utf8")
            chess_rules = file.read()
            label.set_markup(chess_rules)
        else:
            file = open("checkersrules.txt", encoding="utf8")
            checkers_rules = file.read()
            label.set_markup(checkers_rules)

        label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))

        scrolled.add(label)
        help_box.add(scrolled)

        self.connect("destroy", self.hide)  # this gives error message but still does it??


class PromotePawnWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Choose Promotion ")
        self.set_border_width(50)
        self.set_position(Gtk.WindowPosition.CENTER)
        col = Gdk.Color(2000, 6000, 200)  # dark green
        self.modify_bg(Gtk.StateType.NORMAL, col)
        promote_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.add(promote_box)

        player_1_timer.stop()  # stop the timers while this is open
        player_2_timer.stop()

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

    def queen_clicked(self, button):
        print('Queen was chosen')
        if current == "Player 1":
            player_1_timer.start()
        else:
            player_2_timer.start()
        self.hide()

    def knight_clicked(self, button):
        print('Knight was chosen')
        if current == "Player 1":
            player_1_timer.start()
        else:
            player_2_timer.start()
        self.hide()

    def bishop_clicked(self, button):
        print('Bishop was chosen')
        if current == "Player 1":
            player_1_timer.start()
        else:
            player_2_timer.start()
        self.hide()

    def rook_clicked(self, button):
        print('Rook was chosen')
        if current == "Player 1":
            player_1_timer.start()
        else:
            player_2_timer.start()
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

        self.connect("destroy", Gtk.main_quit)  # fixed the exit stalling problem

    def play_clicked(self, button):
        print('Play was chosen')
        game_type = GameChoiceBox()  # do we want it to go back to the board or back through menus?
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


if __name__ == "__main__":
    win = TheWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    win.game_choice_box.hide()
    win.player_type.hide()
    win.customization.hide()
    win.board.hide()
    Gtk.main()
