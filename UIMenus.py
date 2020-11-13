import gi
from gi.repository import Gtk, Gdk, GdkPixbuf
from Player import Player
from PlayerType import PlayerType
from Game import Game
from PieceSet import PieceSet
from Timer import Timer
gi.require_version("Gtk", "3.0")
resume = True
checkers = False
chess = False


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")

        self.button = Gtk.Button(label="Click Here")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_button_clicked(self, widget):
        Gtk.Window.__init__(self, title="Hello ")
        print("Hello World")


class MainMenuWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Main Menu")
        self.set_border_width(70)
        self.set_position(Gtk.WindowPosition.CENTER)
        col = Gdk.Color(2000, 6000, 200)  # dark green
        self.modify_bg(Gtk.StateType.NORMAL, col)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_box)
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

        back_button = Gtk.Button.new_with_mnemonic("_Exit")
        back_button.connect("clicked", self.exit_clicked)
        main_box.pack_start(back_button, True, True, 0)

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
        col = Gdk.Color(2000, 6000, 200)  # dark green
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

        back_button = Gtk.Button.new_with_mnemonic("_Back")
        back_button.connect("clicked", self.back_clicked)
        game_box.pack_start(back_button, True, True, 0)

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
        self.set_border_width(100)
        self.set_default_size(200,200)
        self.set_position(Gtk.WindowPosition.CENTER)
        customization = Gtk.Box(spacing=6)
        self.add(customization)

        red = Gtk.RadioButton.new_with_label_from_widget(None, "Red")
        red.connect("toggled", self.on_button_toggled, "Red")
        customization.pack_start(red, False, False, 0)

        blue = Gtk.RadioButton.new_with_label_from_widget(red, "Blue")
        blue.connect("toggled", self.on_button_toggled, "Blue")
        customization.pack_start(blue, False, False, 0)

        green = Gtk.RadioButton.new_with_mnemonic_from_widget(red, "Green")
        green.connect("toggled", self.on_button_toggled, "Green")
        customization.pack_start(green, False, False, 0)

        back_button = Gtk.Button.new_with_mnemonic("_Back")
        back_button.connect("clicked", self.back_clicked)
        customization.pack_start(back_button, True, True, 0)

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


if __name__ == "__main__":
    win = MainMenuWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
