# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch

from Pieces import *
import pytest
from Game import Game
from Board import Board


class PossibleMoves:
    """
    The class defining possible moves for a piece
    Attributes:
    __Piece: piece object wishing to move, moves to be calculated
    __moves: List of end locations possible to move to
    __game: game object to get player locations, etc
    __board: board object, created during initialization
    """

    def __init__(self, game_square, game_obj):
        self.__game_square = game_square
        self.__Piece = game_square.get_piece()
        self.__moves = []
        self.__game = game_obj
        self.__row = game_square.get_row()
        self.__col = game_square.get_col()
        self.__game_type = game_obj.get_game_type()  # will come back as either "chess" or "checkers"
        self.__board = self.__game.get_board()

    def build_list_of_moves(self):
        """
        Determine based on the piece where it can potentially move
        :return: 0 on success, -1 on failure
        """
        if self.__game_type.lower() == "checkers":
            list_of_candidate_game_squares = []
            # Generate possible moves for checkers
            if 0 < self.__row-1 < self.__board.get_size()-1 or 0 < self.__col-1 < self.__board.get_size()-1:
                top_left = self.__board.get_game_square(self.__row-1, self.__col-1)
                list_of_candidate_game_squares.append(top_left)
            if 0 < self.__row-1 < self.__board.get_size()-1 or 0 < self.__col+1 < self.__board.get_size()-1:
                top_right = self.__board.get_game_square(self.__row-1, self.__col+1)
                list_of_candidate_game_squares.append(top_right)

            if self.__Piece.get_promotion_status():
                # Promoted checkers coins can also move backwards
                if 0 < self.__row+1 < self.__board.get_size()-1 or 0 < self.__col-1 < self.__board.get_size()-1:
                    bot_left = self.__board.get_game_square(self.__row+1, self.__col-1)
                    list_of_candidate_game_squares.append(bot_left)
                if 0 < self.__row+1 < self.__board.get_size()-1 or 0 < self.__col+1 < self.__board.get_size()-1:
                    bot_right = self.__board.get_game_square(self.__row+1, self.__col+1)
                    list_of_candidate_game_squares.append(bot_right)

            for square in list_of_candidate_game_squares:
                dest_piece = square.get_occupying_piece()
                if dest_piece is None:
                    continue
                    # Do nothing, the square is a valid move
                else:
                    # There is a piece there, compare the colour
                    if self.__game_square().get_occupying_piece().get_colour() == dest_piece.get_colour():
                        # Pieces are the same colour, cannot make this move
                        list_of_candidate_game_squares.remove(square)
                    else:
                        # Piece is an opponent piece, we need to go look at what is on the other side of it.
                        if self.__game_square().get_col() < square.get_col():
                            # We are to the right
                            if self.__game_square().get_row() < square.get_row():
                                # Bottom right
                                if 0 < self.__row + 2 < self.__board.get_size() - 1 or 0 < self.__col + 2 < self.__board.get_size() - 1:
                                    new_bot_right = self.__board.get_game_square(self.__row + 2, self.__col + 2)
                                    if new_bot_right.get_occupying_piece() is None:
                                        list_of_candidate_game_squares.append(new_bot_right)
                                        # TODO: Right now this only allows for one jump, need to check to see if
                                        #  there are multi-jump moves available
                            else:
                                # Top right
                                if 0 < self.__row - 2 < self.__board.get_size() - 1 or 0 < self.__col + 2 < self.__board.get_size() - 1:
                                    new_top_right = self.__board.get_game_square(self.__row - 2, self.__col + 2)
                                    if new_top_right.get_occupying_piece() is None:
                                        list_of_candidate_game_squares.append(new_top_right)
                                        # TODO: Right now this only allows for one jump, need to check to see if
                                        #  there are multi-jump moves available
                        else:
                            # Destination square we are comparing to is to the left of our originally clicked on square
                            if self.__game_square().get_row() < square.get_row():
                                # Bottom left
                                if 0 < self.__row + 2 < self.__board.get_size() - 1 or 0 < self.__col - 2 < self.__board.get_size() - 1:
                                    new_bot_left = self.__board.get_game_square(self.__row + 2, self.__col - 2)
                                    if new_bot_left.get_occupying_piece() is None:
                                        list_of_candidate_game_squares.append(new_bot_left)
                                        # TODO: Right now this only allows for one jump, need to check to see if
                                        #  there are multi-jump moves available
                            else:
                                # Top Left
                                if 0 < self.__row - 2 < self.__board.get_size() - 1 or 0 < self.__col - 2 < self.__board.get_size() - 1:
                                    new_top_left = self.__board.get_game_square(self.__row - 2, self.__col - 2)
                                    if new_top_left.get_occupying_piece() is None:
                                        list_of_candidate_game_squares.append(new_top_left)
                                        # TODO: Right now this only allows for one jump, need to check to see if
                                        #  there are multi-jump moves available

                        list_of_candidate_game_squares.remove(square)

            self.__moves = list_of_candidate_game_squares
            return 0

        elif self.__game_type == "chess":
            if type(self.__Piece).__name__ == "King":
                # TODO: generate possible moves for King
                pass
            elif type(self.__Piece).__name__ == "Queen":
                # TODO: generate possible moves for Queen
                pass
            elif type(self.__Piece).__name__ == "Bishop":
                # TODO: generate possible moves for Bishop
                pass
            elif type(self.__Piece).__name__ == "Knight":
                # TODO: generate possible moves for Knight
                pass
            elif type(self.__Piece).__name__ == "Rook":
                # TODO: generate possible moves for Rook
                pass
            elif type(self.__Piece).__name__ == "Pawn":
                # TODO: generate possible moves for Pawn
                pass
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
        return self.__moves

    def display_options(self):
        """
        Display on the board the list of Possible moves for the piece
        """
        pass
