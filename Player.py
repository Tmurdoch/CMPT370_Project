# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from group4.PlayerType import PlayerType
from group4.Timer import Timer
#from PieceSet import PieceSet


class Player(object):
    """
    A Player is an object that has a name, a colour and controls pieces inside a piece set by making moves
    to play a game of Chess or Checkers. ????
    """
    def __init__(self, name, player_type, timer, castled):
        """
        Initializes a Player object.
        :param: piece_set: The piece set for a Player.
        :param: colour: The colour of pieces for a Player.
        :param name: The name of a Player.
        :param: player_type: The type of Player the Player is, can be AI or Human
        :param: timer: The Timer object for a Player
        :param castled: A boolean to see if the player has been castled or not.
        """
        #self.__piece_set = piece_set
        #self.__colour = colour
        self.__name = name
        self.__player_type = player_type
        self.__timer = timer
        self.__castled = castled

    def make_move(self):
        """Allows a Player to move a piece???"""
        """TO DO"""

    def get_piece_set(self):
        """Returns the PieceSet object of a Player"""
        return self.piece_set

    def set_piece_set(self, piece_set):
        """Sets a Player's piece set to a PieceSet object"""
        self.piece_set = piece_set

    def get_colour(self):
        """Returns the PieceSet object colour of a Player"""
        return self.colour

    def set_colour(self, colour):
        """Sets a Player's piece colour to a PieceSet object's colour"""
        self.colour = colour

    def get_name(self):
        """Returns the name of a Player"""
        return self.name

    def set_name(self, name):
        """Sets a Player's name"""
        self.name = name

    def get_player_type(self):
        """Returns the type of PlayerType object for a Player, AI(0) or Human(1)"""
        return self.player_type.value

    def set_player_type(self, player_type):
        """Sets a Player's PlayerType object to either AI(0) or Human(1)"""
        self.player_type = player_type

    def get_timer(self):
        """Returns the Timer object of a Player"""
        return self.timer

    def set_timer(self, timer):
        """Sets a Player's timer to a Timer object"""
        self.timer = timer

    def get_castled(self):
        """Checks if the Player has castled or not"""
        return self.castled

    def set_castled(self,castled):
        """Sets the Player's castled to True or False based on if they have been castled or not"""
        self.castled = castled


def test_player():
    pt = PlayerType.computer_engine
    t = Timer(300, 300, False)
    t1 = Timer(30, 30, False)
    p = Player("Joel", pt, t, False)
    assert(p.get_name() == 'Joel')
    p.set_name("Brian")
    assert(p.get_name() == "Brian")
    assert(p.get_player_type() == 0)
    p.set_player_type(PlayerType.human)
    assert(p.get_player_type() == 1)
    assert(p.get_timer() == t)
    p.set_timer(t1)
    assert(p.get_timer() == t1)
    assert(not p.get_castled())
    p.set_castled(True)
    assert(p.get_castled())
