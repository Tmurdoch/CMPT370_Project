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
        """
        if self.__game_type == "chess":
            list_of_candidate_game_squares = []
            if 0 < self.__row - 1 < self.__board.get_size() - 1 or 0 < self.__col - 1 < self.__board.get_size() - 1:
                top_left = self.__board.get_game_square(self.__row - 1, self.__col - 1)
                list_of_candidate_game_squares.append(top_left)
            if 0 < self.__row - 1 < self.__board.get_size() - 1 or 0 < self.__col + 1 < self.__board.get_size() - 1:
                top_right = self.__board.get_game_square(self.__row - 1, self.__col + 1)
                list_of_candidate_game_squares.append(top_right)

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
                # moves up and to the right
                if (self.__board.get_game_square(self.__row + 2, self.__col + 1).get_colour()
                        is not self.__piece.get_colour()):
                    # if spot has enemy piece on it
                    if self.__board.get_game_square(self.__row + 2, self.__col + 1) is not None:
                        # need to find out how to capture a piece
                        up_right_square = self.__board.get_game_square(self.__row + 2, self.__col + 1)
                        list_of_candidate_game_squares.append(up_right_square)
                # moves up and to the left
                elif (self.__board.get_game_square(self.__row + 2, self.__col - 1).get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row + 2, self.__col - 1) is not None:
                        # need to find out how to capture a piece
                        up_left_square = self.__board.get_game_square(self.__row + 2, self.__col - 1)
                        list_of_candidate_game_squares.append(up_left_square)
                # moves down and to the right
                elif (self.__board.get_game_square(self.__row - 2, self.__col + 1).get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row - 2, self.__col + 1) is not None:
                        # need to find out how to capture a piece
                        down_right_square = self.__board.get_game_square(self.__row - 2, self.__col + 1)
                        list_of_candidate_game_squares.append(down_right_square)
                # moves down and to the left
                elif (self.__board.get_game_square(self.__row - 2, self.__col - 1).get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row - 2, self.__col - 1) is not None:
                        # need to find out how to capture a piece
                        down_left_square = self.__board.get_game_square(self.__row - 2, self.__col - 1)
                        list_of_candidate_game_squares.append(down_left_square)
                # moves right and up
                elif (self.__board.get_game_square(self.__row + 1, self.__col + 2).get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row + 1, self.__col + 2) is not None:
                        # need to find out how to capture a piece
                        right_up_square = self.__board.get_game_square(self.__row + 1, self.__col + 2)
                        list_of_candidate_game_squares.append(right_up_square)
                # moves right and down
                elif (self.__board.get_game_square(self.__row - 1, self.__col + 2).get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row - 1, self.__col + 2) is not None:
                        # need to find out how to capture a piece
                        right_down_square = self.__board.get_game_square(self.__row - 1, self.__col + 2)
                        list_of_candidate_game_squares.append(right_down_square)
                # moves left and up
                elif (self.__board.get_game_square(self.__row + 1, self.__col - 2).get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row + 1, self.__col - 2) is not None:
                        # need to find out how to capture a piece
                        left_up_square = self.__board.get_game_square(self.__row + 1, self.__col - 2)
                        list_of_candidate_game_squares.append(left_up_square)
                # moves left and down
                elif (self.__board.get_game_square(self.__row - 1, self.__col - 2) .get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row - 1, self.__col - 2) is not None:
                        # need to find out how to capture a piece
                        left_down_square = self.__board.get_game_square(self.__row - 1, self.__col - 2)
                        list_of_candidate_game_squares.append(left_down_square)

                pass
            elif type(self.__Piece).__name__ == "Rook":
                # TODO: generate possible moves for Rook

                pass
            elif type(self.__Piece).__name__ == "Pawn":
                # TODO: generate possible moves for Pawn
                if self.__board.get_game_square(self.__row + 1, self.__col) is None:
                    front_square = self.__board.get_game_square(self.__row + 1, self.__col)
                    list_of_candidate_game_squares.append(front_square)

                # check if possible to move 2 square in front and pawn has not move yet
                elif self.__board.get_game_square(self.__row + 2 , self.__col) is None and not self.__Piece.get_moved_yet_status():
                    front_square2 = self.__board.get_game_square(self.__row + 2, self.__col)
                    list_of_candidate_game_squares.append(front_square2)

                # check if enemy piece on top right of piece to capture and move
                elif self.__board.get_game_square(self.__row + 1, self.__col +1) is not None and \
                        (self.__board.get_game_square(self.__row + 1, self.__col +1).get_colour() is not self.__piece.get_colour):
                    if (self.__row == self.__board.get_size() - 2):
                        #  promote + capture
                        capture_piece_move = self.__board.get_game_square(self.__row + 1, self.__col + 1)
                        list_of_candidate_game_squares.append(capture_piece_move)
                        self.__Piece.promote()
                    else:
                        # just capture
                        capture_piece_move = self.__board.get_game_square(self.__row + 1, self.__col + 1)
                        list_of_candidate_game_squares.append(capture_piece_move)

                # check if enemy piece on top left of piece to capture and move
                elif self.__board.get_game_square(self.__row + 1, self.__col - 1) is not None and \
                        (self.__board.get_game_square(self.__row + 1, self.__col - 1).get_colour() is not self.__piece.get_colour):
                    if (self.__row == self.__board.get_size() - 2):
                        #  promote + capture
                        capture_piece_move = self.__board.get_game_square(self.__row + 1, self.__col - 1)
                        list_of_candidate_game_squares.append(capture_piece_move)
                        self.__Piece.promote()

                    else:
                        # just capture
                        capture_piece_move = self.__board.get_game_square(self.__row + 1, self.__col - 1)
                        list_of_candidate_game_squares.append(capture_piece_move)

                pass


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
