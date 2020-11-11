# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch

from Pieces import *
import pytest


class PossibleMoves():
    """
    The class defining possible moves for a piece
    Attributes:
    __Piece: piece object wishing to move, moves to be calculated
    __move: List of end locations possible to move to
    """

    def __init__(self, piece):
        self.__Piece = piece
        self.__move = []

    def build_list_of_moves(self):
        """
        Determine based on the piece where it can potentially move
        """
        self.__move = []

    def select_best(self):
        """
        Return to the Ai the best potential move
        """
        pass

    def get_moves(self):
        """
        return: a list of moves that are legal
        """
        return self.__move

    def display_options(self):
        """
        Display on the board the list of Possible moves for the piece
        """
        pass
