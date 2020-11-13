# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch

from Pieces import *
import pytest
from Game import Game
from Board import Board


class PossibleMoves():
    """
    The class defining possible moves for a piece
    Attributes:
    __Piece: piece object wishing to move, moves to be calculated
    __move: List of end locations possible to move to
    __game: game object to get player locations, etc
    __board: board object, created during initialization
    """

    def __init__(self, piece, game_obj):
        self.__Piece = piece
        self.__move = []
        self.__game = game_obj
        #self.__board = self.__game.get_board()

    def build_list_of_moves(self, array_location):
        """
        Determine based on the piece where it can potentially move
        :return: 0 on success, -1 on failure
        """
        #TODO: implement this function
        #following is for TESTING ONLY
        if type(self.__Piece).__name__ == "King":
	    #check surrounding squares 
            #generate_king_moves(starting_location, is_castled) something like this -> in Pieces, returns list of tuples denoting possible moves without blocking considered
            print("is king")
            return 0
        else:
            return -1

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
