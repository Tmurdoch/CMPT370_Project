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

    def __init__(self, game_square, game_obj):
        self.__game_square = game_square
        self.__Piece = game_square.get_piece()
        self.__move = []
        self.__game = game_obj
        self.__row = game_square.get_row()
        self.__col = game_square.get_col()
        self.__game_type = game_obj.get_game_type() #will come back as either chess or checkers
        self.__board = self.__game.get_board()

    def build_list_of_moves(self):
        """
        Determine based on the piece where it can potentially move
        :return: 0 on success, -1 on failure
        """
        if self.game_type == "checkers":
            #generate possible moves for checkers
            if 0 < self.__row-1 < self.__board.get_size()-1 or 0 < self.__col-1 < self.__board.get_size()-1:
                top_left =  self.__board.get_game_square(self.__row-1, self.__col-1)
            if self.__row+1 > self.__board.get_size()-1 or self.__col+1 > self.__board.get_size()-1:
                top_left =  self.__board.get_game_square(self.__row-1, self.__col-1)
            if self.__Piece.get_promotion_status():
                #is promoted
                #check bounds of array
                if 0 < self.__row-1 < self.__board.get_size()-1 or 0 < self.__col-1 < self.__board.get_size()-1:
                    top_left =  self.__board.get_game_square(self.__row-1, self.__col-1)
                if self.__row-1 > self.__board.get_size()-1 or self.__col-1 > self.__board.get_size()-1:
                    top_left =  self.__board.get_game_square(self.__row-1, self.__col-1)
                top_right = self.__board.get_game_square(self.__row-1, self.__col+1)
                
            else:

                #is not promoted  


                top_left =  self.__board.get_game_square(self.__row-1, self.__col-1)
                top_right = self.__board.get_game_square(self.__row-1, self.__col+1)
                bot_left = self.__board.get_game_square(self.__row+1, self.__col-1)
                bot_right = self.__board.get_game_square(self.__row+1. self.__col+1)

        elif self.game_type == "chess":
            #generate possible moves for a chess piece
        else:
            return -1
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
