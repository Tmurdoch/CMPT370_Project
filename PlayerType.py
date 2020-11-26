# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from enum import IntEnum


class PlayerType(IntEnum):
    """
    This enum defines the possible player types.
    The AI is used in single player mode, see the GameType enum for more.
    Note: Adding additional player types may require significant system additions.
    """
    AI = 0
    HUMAN = 1
