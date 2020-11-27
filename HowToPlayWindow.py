# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Rsvg", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, Rsvg, GLib


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