# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Rsvg", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Rsvg, GLib
from GameType import GameType, GAME_TYPE_STRING_LOOK_UP_TABLE


class HowToPlayWindow(Gtk.Window):
    """
       The HowToPlayWindow initializes a Gtk Window to hold a Gtk Box that holds a Gtk Scrolled Window that displays the
       rules of the chosen game.
       Attributes:
           help_box: A Gtk Box used to hold a Gtk Scrolled Window.
           scrolled: A Gtk Scrolled Window that displays the txt files for the rules of chess and checkers.
    """

    def __init__(self, game):
        Gtk.Window.__init__(self, title="How to Play " + GAME_TYPE_STRING_LOOK_UP_TABLE[game])
        self.set_border_width(50)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_size_request(200, 400)
        col = Gdk.Color(2000, 6000, 200)
        self.modify_bg(Gtk.StateType.NORMAL, col)
        self.help_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.help_box)

        self.scrolled = Gtk.ScrolledWindow(vexpand=True)
        self.scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        label = Gtk.Label()
        if game == GameType.CHESS:
            try:
                fp = open("chessrules.txt", "r", encoding="utf8")
                chess_rules = fp.read()
                fp.close()
                label.set_markup(chess_rules)
            except:
                label.set_markup("Something went wrong reading How to Play")
        elif game == GameType.CHECKERS:
            try:
                fp = open("checkersrules.txt", "r", encoding="utf8")
                checkers_rules = fp.read()
                fp.close()
                label.set_markup(checkers_rules)
            except:
                label.set_markup("Something went wrong reading How to Play")
        else:
            label.set_markup("Congratulations you won! (you broke this really badly)")
        label.override_color(Gtk.StateFlags.NORMAL,
                             Gdk.RGBA(1.0, 1.0, 1.0, 1.0))

        self.scrolled.add(label)
        self.help_box.add(self.scrolled)
