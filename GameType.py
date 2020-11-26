# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from enum import IntEnum


class GameType(IntEnum):
    """
    This enum defines the possible game types.
    Note: Adding additional game types may require significant system additions.
    """
    CHESS = 0
    CHECKERS = 1


class GamePlayerMode(IntEnum):
    """
    This enum defines the possible player modes.
    Note: Adding additional game modes may require significant system additions.
    """
    SINGLEPLAYER = 0  # A single player playing against a computer engine
    LOCAL_MULTIPLAYER = 1  # Both players using the same set of computer peripherals
