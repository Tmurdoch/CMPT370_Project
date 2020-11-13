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
        __squares_you_can_move_to: List of gamesquares you can to move to
        __game: game object to get player locations, etc
        __board: board object, created during initialization
    """

    def __init__(self, game_square, game_obj):
        self.__game_square = game_square
        self.__Piece = game_square.get_piece()
        self.__squares_you_can_move_to = []  # Will be a list of GameSquare Objects
        self.__game = game_obj
        self.__row = game_square.get_row()
        self.__col = game_square.get_col()
        self.__game_type = game_obj.get_game_type()  # will come back as either "chess" or "checkers"
        self.__board = self.__game.get_board()

    def build_list_of_moves(self):
        """
        Determine based on the piece where it can potentially move and load it into the __squares_you_can_move_to attribute
        Note: Even on success, the list of possible moves for a game-square might be an empty list
        :return: 0 on success, -1 on failure
        """
        list_of_candidate_game_squares = []
        if self.__game_type.lower() == "checkers":
            # Generate possible moves for checkers
            if 0 <= self.__row-1 < self.__board.get_size() or 0 <= self.__col-1 < self.__board.get_size():
                top_left = self.__board.get_game_square(self.__row-1, self.__col-1)
                list_of_candidate_game_squares.append(top_left)
            if 0 <= self.__row-1 < self.__board.get_size() or 0 <= self.__col+1 < self.__board.get_size():
                top_right = self.__board.get_game_square(self.__row-1, self.__col+1)
                list_of_candidate_game_squares.append(top_right)

            if self.__Piece.get_promotion_status():
                # Promoted checkers coins can also move backwards
                if 0 <= self.__row+1 < self.__board.get_size() or 0 <= self.__col-1 < self.__board.get_size():
                    bot_left = self.__board.get_game_square(self.__row+1, self.__col-1)
                    list_of_candidate_game_squares.append(bot_left)
                if 0 <= self.__row+1 < self.__board.get_size() or 0 <= self.__col+1 < self.__board.get_size():
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
                                if 0 <= self.__row + 2 < self.__board.get_size() or 0 <= self.__col + 2 < self.__board.get_size():
                                    new_bot_right = self.__board.get_game_square(self.__row + 2, self.__col + 2)
                                    if new_bot_right.get_occupying_piece() is None:
                                        list_of_candidate_game_squares.append(new_bot_right)
                                        # TODO: Right now this only allows for one jump, need to check to see if
                                        #  there are multi-jump moves available
                            else:
                                # Top right
                                if 0 <= self.__row - 2 < self.__board.get_size() or 0 <= self.__col + 2 < self.__board.get_size():
                                    new_top_right = self.__board.get_game_square(self.__row - 2, self.__col + 2)
                                    if new_top_right.get_occupying_piece() is None:
                                        list_of_candidate_game_squares.append(new_top_right)
                                        # TODO: Right now this only allows for one jump, need to check to see if
                                        #  there are multi-jump moves available
                        else:
                            # Destination square we are comparing to is to the left of our originally clicked on square
                            if self.__game_square().get_row() < square.get_row():
                                # Bottom left
                                if 0 <= self.__row + 2 < self.__board.get_size() or 0 <= self.__col - 2 < self.__board.get_size():
                                    new_bot_left = self.__board.get_game_square(self.__row + 2, self.__col - 2)
                                    if new_bot_left.get_occupying_piece() is None:
                                        list_of_candidate_game_squares.append(new_bot_left)
                                        # TODO: Right now this only allows for one jump, need to check to see if
                                        #  there are multi-jump moves available
                            else:
                                # Top Left
                                if 0 <= self.__row - 2 < self.__board.get_size() or 0 <= self.__col - 2 < self.__board.get_size():
                                    new_top_left = self.__board.get_game_square(self.__row - 2, self.__col - 2)
                                    if new_top_left.get_occupying_piece() is None:
                                        list_of_candidate_game_squares.append(new_top_left)
                                        # TODO: Right now this only allows for one jump, need to check to see if
                                        #  there are multi-jump moves available

                        list_of_candidate_game_squares.remove(square)

            self.__squares_you_can_move_to = list_of_candidate_game_squares
            return 0

        elif self.__game_type == "chess":
            if type(self.__Piece).__name__ == "King":
                # TODO: generate possible moves for King
                pass
            elif type(self.__Piece).__name__ == "Queen":
                # The queen can be moved any number of unoccupied squares in a straight line
                # vertically, horizontally, or diagonally, thus combining the moves of the rook and bishop
                # Vertical movements
                for row_of_game_square in self.__board.get_game_board():
                    if row_of_game_square[self.__col].get_occupying_piece() is None:
                        list_of_candidate_game_squares.append(row_of_game_square[self.__col])
                    elif row_of_game_square[self.__col].get_occupying_piece().get_colour() != self.__Piece.get_colour():
                        list_of_candidate_game_squares.append(row_of_game_square[self.__col])
                # Horizontal movemetns
                for col_of_game_square in range(self.__board.get_size()):
                    if self.__board.get_game_board[self.__row][col_of_game_square] is None:
                        list_of_candidate_game_squares.append(
                            self.__board.get_game_board[self.__row][col_of_game_square])
                    elif self.__board.get_game_board[self.__row][col_of_game_square].get_occupying_piece().get_colour()\
                            != self.__Piece.get_colour():
                        list_of_candidate_game_squares.append(
                            self.__board.get_game_board[self.__row][col_of_game_square])
                # Diagonal movements
                for row in range(self.__board.get_size()):
                    for col in range(self.__board.get_size()):
                        if abs(self.__row - row) == abs(self.__col - col):
                            # on the diagonal
                            if self.__board.get_game_board().get_game_square(row, col) is None:
                                list_of_candidate_game_squares\
                                    .append(self.__board.get_game_board().get_game_square(row, col))
                            if self.__board.get_game_board().get_game_square(row, col).get_occupying_piece().get_colour() != self.__Piece.get_colour():
                                list_of_candidate_game_squares \
                                    .append(self.__board.get_game_board().get_game_square(row, col))

            elif type(self.__Piece).__name__ == "Bishop":
                # The bishop can be moved any number of unoccupied squares in a straight line diagonally
                for row in range(self.__board.get_size()):
                    for col in range(self.__board.get_size()):
                        if abs(self.__row - row) == abs(self.__col - col):
                            # on the diagonal
                            if self.__board.get_game_board().get_game_square(row, col) is None:
                                list_of_candidate_game_squares \
                                    .append(self.__board.get_game_board().get_game_square(row, col))
                            if self.__board.get_game_board().get_game_square(row,
                                                                             col).get_occupying_piece().get_colour() != self.__Piece.get_colour():
                                list_of_candidate_game_squares \
                                    .append(self.__board.get_game_board().get_game_square(row, col))

            elif type(self.__Piece).__name__ == "Knight":
                # moves up and to the right
                if (self.__board.get_game_square(self.__row - 2, self.__col + 1).get_colour()
                        is not self.__piece.get_colour()):
                    # if spot has enemy piece on it
                    if self.__board.get_game_square(self.__row - 2, self.__col + 1) is not None:
                        # need to find out how to capture a piece
                        up_right_square = self.__board.get_game_square(self.__row - 2, self.__col + 1)
                        list_of_candidate_game_squares.append(up_right_square)
                # moves up and to the left
                elif (self.__board.get_game_square(self.__row - 2, self.__col - 1).get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row - 2, self.__col - 1) is not None:
                        # need to find out how to capture a piece
                        up_left_square = self.__board.get_game_square(self.__row - 2, self.__col - 1)
                        list_of_candidate_game_squares.append(up_left_square)
                # moves down and to the right
                elif (self.__board.get_game_square(self.__row + 2, self.__col + 1).get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row + 2, self.__col + 1) is not None:
                        # need to find out how to capture a piece
                        down_right_square = self.__board.get_game_square(self.__row + 2, self.__col + 1)
                        list_of_candidate_game_squares.append(down_right_square)
                # moves down and to the left
                elif (self.__board.get_game_square(self.__row + 2, self.__col - 1).get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row + 2, self.__col - 1) is not None:
                        # need to find out how to capture a piece
                        down_left_square = self.__board.get_game_square(self.__row + 2, self.__col - 1)
                        list_of_candidate_game_squares.append(down_left_square)
                # moves right and up
                elif (self.__board.get_game_square(self.__row - 1, self.__col + 2).get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row - 1, self.__col + 2) is not None:
                        # need to find out how to capture a piece
                        right_up_square = self.__board.get_game_square(self.__row - 1, self.__col + 2)
                        list_of_candidate_game_squares.append(right_up_square)
                # moves right and down
                elif (self.__board.get_game_square(self.__row + 1, self.__col + 2).get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row + 1, self.__col + 2) is not None:
                        # need to find out how to capture a piece
                        right_down_square = self.__board.get_game_square(self.__row + 1, self.__col + 2)
                        list_of_candidate_game_squares.append(right_down_square)
                # moves left and up
                elif (self.__board.get_game_square(self.__row - 1, self.__col - 2).get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row - 1, self.__col - 2) is not None:
                        # need to find out how to capture a piece
                        left_up_square = self.__board.get_game_square(self.__row - 1, self.__col - 2)
                        list_of_candidate_game_squares.append(left_up_square)
                # moves left and down
                elif (self.__board.get_game_square(self.__row + 1, self.__col - 2).get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row + 1, self.__col - 2) is not None:
                        # need to find out how to capture a piece
                        left_down_square = self.__board.get_game_square(self.__row + 1, self.__col - 2)
                        list_of_candidate_game_squares.append(left_down_square)

            elif type(self.__Piece).__name__ == "Rook":
                # The rook can be moved any number of unoccupied squares in a straight line vertically or horizontally
                # Vertical movements
                for row_of_game_square in self.__board.get_game_board():
                    if row_of_game_square[self.__col].get_occupying_piece() is None:
                        list_of_candidate_game_squares.append(row_of_game_square[self.__col])
                    elif row_of_game_square[self.__col].get_occupying_piece().get_colour() != self.__Piece.get_colour():
                        list_of_candidate_game_squares.append(row_of_game_square[self.__col])
                # Horizontal movemetns
                for col_of_game_square in range(self.__board.get_size()):
                    if self.__board.get_game_board[self.__row][col_of_game_square] is None:
                        list_of_candidate_game_squares.append(
                            self.__board.get_game_board[self.__row][col_of_game_square])
                    elif self.__board.get_game_board[self.__row][col_of_game_square].get_occupying_piece().get_colour() \
                            != self.__Piece.get_colour():
                        list_of_candidate_game_squares.append(
                            self.__board.get_game_board[self.__row][col_of_game_square])

            elif type(self.__Piece).__name__ == "Pawn":
                # Normally a pawn moves by advancing a single square,
                #  but the first time a pawn moves, it has the option of advancing two squares. Pawns may not use the
                #  initial two-square advance to jump over an occupied square, or to capture. Any piece immediately 
                #  in front of a pawn, friend or foe, blocks its advance. 
                if 0 <= self.__row - 1 < self.__board.get_size():
                    immediately_in_front = self.__board.get_game_square(self.__row-1, self.__col)
                    if immediately_in_front.get_occupying_piece() is None:
                        list_of_candidate_game_squares.append(immediately_in_front)
                        # Since there is no piece immediately in front, we can check to see if we can move 2 up
                        if not self.__game_square.get_occupying_piece().get_moved_yet_status():
                            # Pawn has not moved yet so it can also move 2 squares forward
                            # This will always be on the board
                            two_in_front = self.__board.get_game_square(self.__row - 2, self.__col)
                            if two_in_front.get_occupying_piece() is None:
                                list_of_candidate_game_squares.append(two_in_front)

                # A pawn captures diagonally forward one square to the left or right
                if 0 <= self.__row - 1 < self.__board.get_size() or 0 <= self.__col - 1 < self.__board.get_size():
                    top_left = self.__board.get_game_square(self.__row - 1, self.__col - 1)
                    if top_left.get_occupying_piece() is not None:
                        # Then there is a piece there, look at what colour it is
                        if self.__game_square().get_occupying_piece().get_colour() != top_left.get_occupying_piece().get_colour():
                            # It is an opponent piece, go ahead and add this as a square they can move to
                            list_of_candidate_game_squares.append(top_left)
                if 0 <= self.__row - 1 < self.__board.get_size() or 0 <= self.__col + 1 < self.__board.get_size():
                    top_right = self.__board.get_game_square(self.__row - 1, self.__col + 1)
                    if top_right.get_occupying_piece() is not None:
                        # Then there is a piece there, look at what colour it is
                        if self.__game_square().get_occupying_piece().get_colour() != top_right.get_occupying_piece().get_colour():
                            # It is an opponent piece, go ahead and add this as a square they can move to
                            list_of_candidate_game_squares.append(top_right)

                self.__squares_you_can_move_to = list_of_candidate_game_squares
                return 0
            else:
                # Could not identify the type of piece
                return -1
        else:
            # Game mode is neither "chess" nor "checkers"
            return -1
    
    def select_best(self):
        """
        Chooses and return the best game squre to move to
        :return: GameSquare, the best game square to move to. Returns None if there are no moves for that square
        """
        if not self.__squares_you_can_move_to:
            # List of moves is empty
            return None
        elif len(self.__squares_you_can_move_to) == 1:
            # The is only one move, it has to be the best
            return self.__squares_you_can_move_to[0]
        else:
            # TODO: Some AI code to evaluate the list of moves to choose the best one, in the mean time we are jsut
            #  returning the first one in the list
            return self.__squares_you_can_move_to[0]

    def get_moves(self):
        """
        :return: GameSquare[]: A list of game squares that are legal to move to
        """
        return self.__squares_you_can_move_to

    def display_options(self):
        """
        Display on the board the list of Possible moves for the piece
        """
        pass
