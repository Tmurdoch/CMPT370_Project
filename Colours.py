# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from enum import Enum


class ColourCodes(Enum):
    WHITE_BLACK = 0
    RED_BLACK = 1


class ColourOffset(Enum):
    OFFSET_LIGHT = 0
    OFFSET_DARK = 1


COLOUR_STRING_LOOK_UP_TABLE = [("White", "Black"),
                               ("Red", "Black")]
