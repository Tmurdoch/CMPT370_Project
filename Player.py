# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from PlayerType import PlayerType
from Timer import Timer
from PieceSet import PieceSet


class Player(object):
    """
    A Player is an object that has a name, a colour and controls pieces inside a piece set by making moves
    to play a game of Chess or Checkers. ????

    Attributes:
        __piece_set: PieceSet:
        __colour: TODO: Not sure if we want this in player?
        __name: String:
        __player_type:
        __timer: Timer:
        __castled: Bool:
    """
    def __init__(self, name, player_type, timer, castled):
        """
        Initializes a Player object.
        :param: string: name: The name of a Player.
        :param: PlayerType: player_type: The type of Player the Player is, can be AI or Human
            TODO: Not sure what type this is? ^
        :param: Timer: timer: The Timer object for a Player
        :param: Boolean: castled: A boolean to see if the player has been castled or not.
        """
        self.__piece_set = None
        self.__colour = None
        self.__name = name
        self.__player_type = player_type
        self.__timer = timer
        self.__castled = castled

    def make_move(self):
        """Allows a Player to move a piece???"""
        # TODO:
        pass

    def get_piece_set(self):
        """:return: The players PieceSet"""
        return self.__piece_set

    def build_piece_set(self, piece_set_type, colour):
        """Sets a Player's piece set to a PieceSet object"""
        self.__colour = colour
        self.__piece_set = PieceSet(piece_set_type, colour)

    def get_colour(self):
        """Returns the PieceSet object colour of a Player"""
        return self.__colour.get_colour()

    def set_colour(self, colour):
        """Sets a Player's piece colour to a PieceSet object's colour"""
        # TODO: Not sure we need this one?
        self.__colour = colour

    def get_name(self):
        """:return: The players name"""
        return self.__name

    def get_player_type(self):
        """":return: type of PlayerType object for a Player, AI(0) or Human(1)"""
        return self.__player_type.value

    def set_player_type(self, player_type):
        """Sets a Player's PlayerType object to either AI(0) or Human(1)"""
        self.__player_type = player_type

    def get_timer(self):
        """:return: Timer object of a Player"""
        return self.__timer

    def get_castled(self):
        """:return: Bool, True if the player has already castled, False otherwise"""
        return self.__castled

    def castle(self):
        """Marks that the player has castled so we can make sure they don't castle again"""
        self.__castled = True


def test_player():
    pt = PlayerType.computer_engine
    t = Timer(1, False)
    t1 = Timer(30, False)
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
