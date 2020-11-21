import gi
from Player import Player
from PlayerType import PlayerType
from Game import Game
from PieceSet import PieceSet
from Timer import Timer
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf

resume = True
checkers = False
chess = False

class TheWindow(Gtk.Window):
        def __init__(self):
                Gtk.Window.__init__(self, title="Main Menu")
                self.set_border_width(70)
                self.set_position(Gtk.WindowPosition.CENTER)
                col = Gdk.Color(2000, 6000, 200)  # dark green
                self.modify_bg(Gtk.StateType.NORMAL, col)

                self.main_box = MainMenuBox()#Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

                self.game_choice_box = GameChoiceBox()
                self.game_choice_box.hide()


                self.grid = Gtk.Grid()
                self.grid.attach(self.main_box,0,0,1,1)
                self.grid.attach(self.game_choice_box,0,0,1,1)
                self.add(self.grid)
                self.main_box.show()

        
                self.connect("destroy", Gtk.main_quit)  # fixed the exit stalling problem
                self.main_box.play_button.connect("clicked", self.main_play_clicked)
                if resume:
                        self.main_box.resume_button.connect("clicked", self.main_resume_clicked)

        def main_play_clicked(self, button):
                print('Play was chosen')
                self.main_box.hide()
                self.game_choice_box.show()

        def main_resume_clicked(self, button):
                print('This should go to resumed game') 
                return



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

                chess_button = Gtk.Button.new_with_label("Chess")
                chess_button.connect("clicked", self.chess_clicked)
                chess_button.set_property("width-request", 300)
                chess_button.set_property("height-request", 100)
                self.pack_start(chess_button, True, True, 0)

                checkers_button = Gtk.Button.new_with_label("Checkers")
                checkers_button.connect("clicked", self.checkers_clicked)
                checkers_button.set_property("width-request", 300)
                checkers_button.set_property("height-request", 100)
                self.pack_start(checkers_button, True, True, 0)

                back_button = Gtk.Button.new_with_label("Back")
                back_button.connect("clicked", self.back_clicked)
                self.pack_start(back_button, True, True, 0)

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
        col = Gdk.Color(2000, 6000, 200)  # dark green
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

        back_button = Gtk.Button.new_with_mnemonic("_Back")
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
        col = Gdk.Color(2000, 6000, 200)  # dark green
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

        label_piece = Gtk.Label()
        label_piece.set_markup("<b>Pieces</b>")
        # label_piece.set_justify(Gtk.Justification.CENTER)
        label_piece.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach(label_piece, 1, 1, 1, 1)

        label_board = Gtk.Label()
        label_board.set_markup("<b>Board</b>")
        label_board.set_justify(Gtk.Justification.CENTER)
        label_board.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach(label_board, 4, 1, 1, 1)

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

        b_light_dark_brown = Gtk.RadioButton.new_with_label_from_widget(b_black_white, "Light Brown and Dark Brown")
        b_light_dark_brown.connect("toggled", self.on_button_toggled, "Light Brown and Dark Brown")
        b_light_dark_brown.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))
        customization.attach_next_to(b_light_dark_brown, b_green_yellow, Gtk.PositionType.BOTTOM, 2, 1)

        back_button = Gtk.Button.new_with_label("Back")
        back_button.connect("clicked", self.back_clicked)
        customization.attach(back_button, 0, 8, 1, 1)

        start_button = Gtk.Button.new_with_label("Start")
        back_button.connect("clicked", self.start_clicked)
        customization.attach(start_button, 4, 8, 1, 1)

        self.connect("destroy", Gtk.main_quit)  # fixed the exit stalling problem

    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "on"
        else:
            state = "off"
        print(name, "was turned", state)

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
        self.set_border_width(200)
        self.set_position(Gtk.WindowPosition.CENTER)
        col = Gdk.Color(2000, 6000, 200)  # dark green
        self.modify_bg(Gtk.StateType.NORMAL, col)
        grid = Gtk.Grid()
        self.add(grid)

        row_1_0 = Gtk.Button(label=" ")
        row_1_0 = Gtk.Button(label=" ")

        single_button = Gtk.Button.new_with_label("Single-Player")
        single_button.connect("clicked", self.single_clicked)
        single_button.set_property("width-request", 300)
        single_button.set_property("height-request", 100)
        # flowbox.pack_start(single_button, True, True, 0)

        # look at EventBox() to see if that works for this

        self.connect("destroy", Gtk.main_quit)

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


class HowToPlayMenu(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="How to Play ")
        self.set_border_width(50)
        self.set_position(Gtk.WindowPosition.CENTER)
        col = Gdk.Color(2000, 6000, 200)  # dark green
        self.modify_bg(Gtk.StateType.NORMAL, col)
        player_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.add(player_box)
        # if we want there to be text in the window

        # scrolled = Gtk.ScrolledWindow()
        # scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        label = Gtk.Label()
        label.set_markup("<a href='https://www.chess.com/learn-how-to-play-chess'"
                         "title='Click to find out more'>Chess Rules</a>")

        label1 = Gtk.Label()
        label1.set_markup("<a href='https://www.fgbradleys.com/rules/Checkers.pdf'"
                          "title='Click to find out more'>Checkers Rules</a>")
        player_box.add(label)
        player_box.add(label1)

        self.connect("destroy", Gtk.main_quit)  # fixed the exit stalling problem


class PlayAgainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Play Again?")
        self.set_border_width(70)
        self.set_position(Gtk.WindowPosition.CENTER)
        col = Gdk.Color(2000, 6000, 200)  # dark green
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
    win = TheWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
