# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from enum import IntEnum


class ColourCodes(IntEnum):
    WHITE_BLACK = 0
    RED_BLACK = 1

class ColourBoardCodes(IntEnum):
    WHITE_BLACK = 0
    RED_BLACK = 1

class ColourOffset(IntEnum):
    OFFSET_LIGHT = 0
    OFFSET_DARK = 1


COLOUR_STRING_LOOK_UP_TABLE = [("White", "Black"),
                               ("Red", "Black")]

COLOUR_BOARD_STRING_LOOK_UP_TABLE = [("White", "Black"),
                                     ("Red", "Black"),
                                     ("Yellow", "Blue")]
