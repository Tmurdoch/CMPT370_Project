# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from enum import IntEnum


class ColourCodes(IntEnum):
    """
    This enum contains constants that indicate what type of colours the players will have.
     Format: LIGHT_DARK.
    """
    BROWN_GREY = 0
    PINK_BLUE = 1


class ColourBoardCodes(IntEnum):
    """
    This enum contains constants that indicate what type of colours the board will have.
     Format: LIGHT_DARK.
    """
    WHITE_BLACK = 0
    RED_GREEN = 1
    YELLOW_BLUE = 3


class ColourOffset(IntEnum):
    """
    This enum contains offset information for the smaller array inside the LUTs found in
    this file, so far the just the light and dark colour strings are in the LUTs, however
    in the future if so desired the hex values for specific colours may be added necessitating
    the addition of OFFSET_LIGHT_HEX etc...
    """
    OFFSET_LIGHT = 0
    OFFSET_DARK = 1
    OFFSET_LIGHT_HEX = 2
    OFFSET_DARK_HEX = 3


COLOUR_STRING_LOOK_UP_TABLE = [("Brown", "Grey", b"88654E", b"606060"),
                               ("HotPink", "Blue", b"FF69B4", b"005FFF")]

COLOUR_BOARD_STRING_LOOK_UP_TABLE = [("White", "Black", b"FFFFFF", b"000000"),
                                     ("Red", "LightGreen",  b"FF3333", b"99FFAA"),
                                     ("LightYellow", "Aquamarine", b"FFCC99", b"66DDAA")]
