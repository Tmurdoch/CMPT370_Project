import gi
from datetime import datetime

gi.require_version("Gtk", "3.0")
import cairo
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject

resume = True
checkers = False
chess = False


class MainMenuWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Main Menu")
        self.set_border_width(70)
        self.set_position(Gtk.WindowPosition.CENTER)
        col = Gdk.Color(2000, 6000, 200)  # dark green
        self.modify_bg(Gtk.StateType.NORMAL, col)
        # b = Button()
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)
        # self.add(b)
        chess_button = Gtk.Button.new_with_label("Play")
        chess_button.connect("clicked", self.play_clicked)
        chess_button.set_property("width-request", 300)
        chess_button.set_property("height-request", 100)
        main_box.pack_start(chess_button, True, True, 0)

        if resume:
            checkers_button = Gtk.Button.new_with_label("Resume")
            checkers_button.connect("clicked", self.resume_clicked)
            checkers_button.set_property("width-request", 300)
            checkers_button.set_property("height-request", 100)
            main_box.pack_start(checkers_button, True, True, 0)

        exit_button = Gtk.Button.new_with_label("Exit")
        exit_button.connect("clicked", self.exit_clicked)
        main_box.pack_start(exit_button, True, True, 0)

        self.connect("destroy", Gtk.main_quit)  # fixed the exit stalling problem

    def play_clicked(self, button):
        print('Play was chosen')  # put next window here
        game_type = GameChoiceWindow()
        game_type.show_all()
        self.hide()

    def resume_clicked(self, button):
        print('This should go to resumed game')  # put next window here
        game_type = GameChoiceWindow()
        game_type.show_all()
        self.hide()

    def exit_clicked(self, button):
        print("This should exit")
        Gtk.main_quit()


class GameChoiceWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Game Choice")
        self.set_border_width(70)
        self.set_position(Gtk.WindowPosition.CENTER)
        col = Gdk.Color(2000, 6000, 200)
        self.modify_bg(Gtk.StateType.NORMAL, col)
        game_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(game_box)

        chess_button = Gtk.Button.new_with_label("Chess")
        chess_button.connect("clicked", self.chess_clicked)
        chess_button.set_property("width-request", 300)
        chess_button.set_property("height-request", 100)
        game_box.pack_start(chess_button, True, True, 0)

        checkers_button = Gtk.Button.new_with_label("Checkers")
        checkers_button.connect("clicked", self.checkers_clicked)
        checkers_button.set_property("width-request", 300)
        checkers_button.set_property("height-request", 100)
        game_box.pack_start(checkers_button, True, True, 0)

        back_button = Gtk.Button.new_with_label("Back")
        back_button.connect("clicked", self.back_clicked)
        game_box.pack_start(back_button, True, True, 0)

        self.connect("destroy", Gtk.main_quit)  # fixed the exit stalling problem

    def chess_clicked(self, button):
        print('Chess was chosen')  # put next window here
        player_type = PlayerTypeWindow("Chess")
        player_type.show_all()
        self.hide()

    def checkers_clicked(self, button):
        print('Checkers was chosen')  # put next window here
        player_type = PlayerTypeWindow("Checkers")
        player_type.show_all()
        self.hide()

    def back_clicked(self, button):
        print("This should go back to Main Menu Window")
        main_window = MainMenuWindow()
        main_window.show_all()
        self.hide()


class PlayerTypeWindow(Gtk.Window):
    def __init__(self, game):
        Gtk.Window.__init__(self, title=game)
        self.__game = game
        self.set_border_width(70)
        self.set_position(Gtk.WindowPosition.CENTER)
        col = Gdk.Color(2000, 6000, 200)
        self.modify_bg(Gtk.StateType.NORMAL, col)
        player_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(player_box)

        single_button = Gtk.Button.new_with_label("Single-Player")
        # single_button.get_style_context().add_class("suggested-action") changes button to blue
        single_button.connect("clicked", self.single_clicked)
        single_button.set_property("width-request", 300)
        single_button.set_property("height-request", 100)
        player_box.pack_start(single_button, True, True, 0)

        multiplayer_button = Gtk.Button.new_with_label("Multi-Player")
        multiplayer_button.connect("clicked", self.multi_clicked)
        multiplayer_button.set_property("width-request", 300)
        multiplayer_button.set_property("height-request", 100)
        player_box.pack_start(multiplayer_button, True, True, 0)

        back_button = Gtk.Button.new_with_label("Back")
        back_button.connect("clicked", self.back_clicked)
        player_box.pack_start(back_button, True, True, 0)

        self.connect("destroy", Gtk.main_quit)  # fixed the exit stalling problem

    def single_clicked(self, button):
        print('Single Player was chosen')  # put next window here
        customization = CustomizationWindow(self.__game, "Single-Player")
        customization.show_all()
        self.hide()

    def multi_clicked(self, button):
        print('Multi Player was chosen')  # put next window here
        customization = CustomizationWindow(self.__game, "Multi-Player")
        customization.show_all()
        self.hide()

    def back_clicked(self, button):
        print("This should go back to Game Choice Window")
        game_type = GameChoiceWindow()
        game_type.show_all()
        self.hide()


class CustomizationWindow(Gtk.Window):
    def __init__(self, game, game_type):
        Gtk.Window.__init__(self, title=game + " " + game_type)
        self.__game = game
        self.__game_type = game_type
        self.set_border_width(60)
        self.set_default_size(150, 150)
        self.set_position(Gtk.WindowPosition.CENTER)
        col = Gdk.Color(2000, 6000, 200)
        self.modify_bg(Gtk.StateType.NORMAL, col)

        customization = Gtk.Grid()
        self.add(customization)
        customization.set_column_spacing(10)
        customization.set_row_spacing(20)
        title = Gtk.Label()
        title.set_markup("<big>Customize your pieces and board!</big>")
        title.set_justify(Gtk.Justification.RIGHT)
        title.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach(title, 3, 0, 1, 1)

        # Pieces choices label
        label_piece = Gtk.Label()
        label_piece.set_markup("<b>Pieces</b>")
        # label_piece.set_justify(Gtk.Justification.CENTER)
        label_piece.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach(label_piece, 1, 1, 1, 1)

        # Board choices label
        label_board = Gtk.Label()
        label_board.set_markup("<b>Board</b>")
        label_board.set_justify(Gtk.Justification.CENTER)
        label_board.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach(label_board, 4, 1, 1, 1)

        # Visualization of the colour choice of Piece
        colour_visual = Gtk.Frame()
        colour_visual.set_shadow_type(Gtk.ShadowType.IN)
        customization.add(colour_visual)

        # All Piece Choices
        black_white = Gtk.RadioButton.new_with_label_from_widget(None, "P1-Black P2-White")
        black_white.connect("toggled", self.on_button_toggled, "Black/White")
        black_white.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach(black_white, 0, 2, 2, 1)

        white_black = Gtk.RadioButton.new_with_label_from_widget(black_white, "P1-White P2-Black")
        white_black.connect("toggled", self.on_button_toggled, "White/Black")
        white_black.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach_next_to(white_black, black_white, Gtk.PositionType.RIGHT, 2, 1)

        red_white = Gtk.RadioButton.new_with_label_from_widget(black_white, "P1-Red P2-White")
        red_white.connect("toggled", self.on_button_toggled, "Red/White")
        red_white.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach_next_to(red_white, black_white, Gtk.PositionType.BOTTOM, 2, 1)

        white_red = Gtk.RadioButton.new_with_label_from_widget(red_white, "P1-White P2-Red")
        white_red.connect("toggled", self.on_button_toggled, "White/Red")
        white_red.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach_next_to(white_red, red_white, Gtk.PositionType.RIGHT, 1, 1)

        blue_green = Gtk.RadioButton.new_with_label_from_widget(red_white, "P1-Blue P2- Green")
        blue_green.connect("toggled", self.on_button_toggled, "Blue/Green")
        blue_green.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach_next_to(blue_green, red_white, Gtk.PositionType.BOTTOM, 2, 1)

        green_blue = Gtk.RadioButton.new_with_label_from_widget(red_white, "P1-Green P2-Blue")
        green_blue.connect("toggled", self.on_button_toggled, "Green/Blue")
        green_blue.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach_next_to(green_blue, blue_green, Gtk.PositionType.RIGHT, 2, 1)

        red_blue = Gtk.RadioButton.new_with_label_from_widget(red_white, "P1-Red P2-Blue")
        red_blue.connect("toggled", self.on_button_toggled, "Red/Blue")
        red_blue.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach_next_to(red_blue, blue_green, Gtk.PositionType.BOTTOM, 2, 1)

        blue_red = Gtk.RadioButton.new_with_label_from_widget(red_white, "P1-Blue P2-Red")
        blue_red.connect("toggled", self.on_button_toggled, "Green/Blue")
        blue_red.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach_next_to(blue_red, green_blue, Gtk.PositionType.BOTTOM, 2, 1)

        # All board choices
        b_black_white = Gtk.RadioButton.new_with_label_from_widget(None, "Black and White")
        b_black_white.connect("toggled", self.on_button_toggled, "Black and White")
        b_black_white.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach_next_to(b_black_white, white_black, Gtk.PositionType.RIGHT, 2, 1)

        b_brown_white = Gtk.RadioButton.new_with_label_from_widget(b_black_white, "Brown and White")
        b_brown_white.connect("toggled", self.on_button_toggled, "Brown and White")
        b_brown_white.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach_next_to(b_brown_white, b_black_white, Gtk.PositionType.BOTTOM, 2, 1)

        b_green_yellow = Gtk.RadioButton.new_with_label_from_widget(b_black_white, "Green and Yellow")
        b_green_yellow.connect("toggled", self.on_button_toggled, "Green and Yellow")
        b_green_yellow.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach_next_to(b_green_yellow, b_brown_white, Gtk.PositionType.BOTTOM, 2, 1)

        b_light_checkerboard_dark_brown = Gtk.RadioButton.new_with_label_from_widget(b_black_white, "Light Brown and checkerboard_dark Brown")
        b_light_checkerboard_dark_brown.connect("toggled", self.on_button_toggled, "Light Brown and checkerboard_dark Brown")
        b_light_checkerboard_dark_brown.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach_next_to(b_light_checkerboard_dark_brown, b_green_yellow, Gtk.PositionType.BOTTOM, 2, 1)

        back_button = Gtk.Button.new_with_label("Back")
        back_button.connect("clicked", self.back_clicked)
        customization.attach(back_button, 0, 8, 1, 1)

        start_button = Gtk.Button.new_with_label("Start")
        start_button.connect("clicked", self.start_clicked)
        customization.attach(start_button, 4, 8, 1, 1)

        self.connect("destroy", Gtk.main_quit)  # fixed the exit stalling problem

    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "on"
            #self.colour()
        else:
            state = "off"
        print(name, "was turned", state)

    """def colour(self, cairo_ctx,drawing_area):
        context = drawing_area.get_style_context()

        height= drawing_area.get_allocated_height()
        width= drawing_area.get_allocated_width()
        Gtk.render_background(context,cairo_ctx, 0,0,width, height)
        cairo_ctx.set_source_rgb(0.300, .155, 0.119)
        cairo_ctx.rectangle(0, 0, width, height)
        cairo_ctx.fill()"""

    def back_clicked(self, button):
        print("This should go back to Game Choice Window")
        player_type = PlayerTypeWindow(self.__game)
        player_type.show_all()
        self.hide()

    def start_clicked(self, button):
        print("This should go to Board Window")
        board = BoardWindow(self.__game, self.__game_type)
        board.show_all()
        self.hide()


class BoardWindow(Gtk.Window):
    def __init__(self, game, game_type):
        Gtk.Window.__init__(self, title=game + " " + game_type)
        self.__game = game
        self.surface = None

        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(80)
        col = Gdk.Color(2000, 6000, 200)
        self.modify_bg(Gtk.StateType.NORMAL, col)

        board_box = Gtk.Grid()
        self.add(board_box)

        # create checkerboard area
        board_frame = Gtk.Frame()
        board_frame.set_shadow_type(Gtk.ShadowType.IN)
        board_box.add(board_frame)

        checkerboard_area = Gtk.DrawingArea()
        checkerboard_area.set_size_request(400, 400)
        board_frame.add(checkerboard_area)
        checkerboard_area.connect('draw', self.checkerboard_draw_event)
        checkerboard_area.connect('configure-event', self.click_configure_event)
        checkerboard_area.connect('button-press-event', self.mouse_press_event)
        checkerboard_area.set_events(checkerboard_area.get_events()
                                     | Gdk.EventMask.LEAVE_NOTIFY_MASK
                                     | Gdk.EventMask.BUTTON_PRESS_MASK)

        timer_frame = Gtk.Frame()
        timer_frame.set_shadow_type(Gtk.ShadowType.IN)
        board_box.add(timer_frame)

        self.timer_area = Gtk.Label()
        board_box.add(self.timer_area)

        help_button = Gtk.Button.new_with_label("help?")
        help_button.connect("clicked", self.help_clicked)
        board_box.attach(help_button, 2, 4, 1, 1)

        # just to see if promotion works
        #promote_button = Gtk.Button.new_with_label("promote?")
        #promote_button.connect("clicked", self.promote_clicked)
        #board_box.attach_next_to(promote_button, help_button, Gtk.PositionType.RIGHT, 1, 1)

        save_quit_button = Gtk.Button.new_with_label("Save and Quit")
        save_quit_button.connect("clicked", self.save_quit_clicked)
        board_box.attach_next_to(save_quit_button,help_button, Gtk.PositionType.RIGHT, 1, 1)
        self.startclocktimer()
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
        if self.surface is None:  # paranoia check, in case we haven't gotten a configure event
            return False

        if event.button == 1:
            self.mouse_pointer(checkerboard_area, event.x, event.y)
            list_list = [[50,50],[50,100],[50,150]]
            y=1
            for x in list_list:
                if event.x <= x[0] and event.y <= x[1]:
                    print(event.x, event.y)
                    print("square ", y)
                    y+=1

        return True

    def displayclock(self):
        #  putting our datetime into a var and setting our label to the result.
        #  we need to return "True" to ensure the timer continues to run, otherwise it will only run once.
        datetimenow = str(datetime.now().second)
        self.timer_area.set_label(datetimenow)
        self.timer_area.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        return True

        # Initialize Timer

    def startclocktimer(self):
        #  this takes 2 args: (how often to update in millisec, the method to run)
        GObject.timeout_add(1000, self.displayclock)

    def help_clicked(self, button):
        print("This should go to HowToPlay Window")
        board = HowToPlayWindow(self.__game)
        board.show_all()
        #self.hide()

    def promote_clicked(self, button):
        print("This should go to PromotePawn Window")
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
        self.set_size_request(200,400)
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

        label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))

        scrolled.add(label)
        help_box.add(scrolled)

        self.connect("destroy", self.hide)  # this gives error message but still does it??


""" will we want to pause timer while this is happening? """
class PromotePawnWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Choose Promotion ")
        self.set_border_width(50)
        self.set_position(Gtk.WindowPosition.CENTER)
        col = Gdk.Color(2000, 6000, 200)  # dark green
        self.modify_bg(Gtk.StateType.NORMAL, col)
        promote_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
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

    def queen_clicked(self, button):
        print('Queen was chosen')
        self.hide()

    def knight_clicked(self, button):
        print('Knight was chosen')
        self.hide()

    def bishop_clicked(self, button):
        print('Bishop was chosen')
        self.hide()

    def rook_clicked(self, button):
        print('Rook was chosen')
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
        game_type = GameChoiceWindow()  # do we want it to go back to the board or back through menus?
        game_type.show_all()
        self.hide()

    def main_menu_clicked(self, button):
        print('This should go to resumed game')
        main_menu = MainMenuWindow()
        main_menu.show_all()
        self.hide()

    def exit_clicked(self, button):
        print("This should exit")
        Gtk.main_quit()


"""class Button(Gtk.Button):
    def __init__(self):
        super().Gtk.Button.new_with_label("Play")
        print("b")"""

if __name__ == "__main__":
    win = MainMenuWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
