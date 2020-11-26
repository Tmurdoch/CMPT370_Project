# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from enum import IntEnum


class ColourCodes(IntEnum):
    """This enum contains constants that indicate
    what type of colours the players will have in
    the game in the formate LIGHT_DARK"""
    WHITE_BLACK = 0
    RED_BLACK = 1

class ColourBoardCodes(IntEnum):
    """This enum contains constants that indicate
    what type of colours the board will have in
    the game in the formate LIGHT_DARK"""
    WHITE_BLACK = 0
    RED_BLACK = 1

class ColourOffset(IntEnum):
    """This enum contains offset information for
    the smaller array inside the LUTs found in
    this file, so far the just the light and
    dark colour strings are in the LUTs, however
    in the future if so desired the hex values
    for specific colours may be added necessetating
    the adition of OFFSET_LIGHT_HEX etc..."""
    OFFSET_LIGHT = 0
    OFFSET_DARK = 1
    OFFSET_LIGHT_HEX = 2
    OFFSET_DARK_HEX = 3


COLOUR_STRING_LOOK_UP_TABLE = [("White", "Black", b"FFFFFF", b"000000"),
                               ("Red", "Black", b"FF0000", b"000000")]

COLOUR_BOARD_STRING_LOOK_UP_TABLE = [("White", "Black", b"FFFFFF", b"000000"),
                                     ("Red", "Black",  b"FF0000", b"000000"),
                                     ("Yellow", "Blue", b"FFFF00", b"0000FF")]
