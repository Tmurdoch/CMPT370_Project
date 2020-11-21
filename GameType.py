# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from enum import IntEnum


class GameType(IntEnum):
    CHESS = 0
    CHECKERS = 1

class GamePlayerMode(IntEnum):
    SINGLEPLAYER = 0
    LOCAL_MULTIPLAYER =1
