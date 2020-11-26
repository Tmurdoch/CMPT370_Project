# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from enum import IntEnum


class GameStatus(IntEnum):
    """
    This enum defines the possible game statuses.
    """
    IN_PROGRESS = 0
    LIGHT_VICTORIOUS = 1
    DARK_VICTORIOUS = 2
