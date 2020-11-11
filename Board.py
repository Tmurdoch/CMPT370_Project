# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from enum import Enum
import GameSquare as Gs
import random
from unittest import mock


class Board:
    """
    Board is where the a particular game board is created based on the size it's given to.
     - size: size of the board in int. used to create the dimension of the board
     - gameBoard: 2D array of GameSquares.
     - boardTheme: color scheme of the board
    """
    def __init__(self, size):
        """
        This will initialize the gameBoard as a square 2D array of GameSquares.
        GameSquare gameBoard[size][size]
        The size param will only take in positive integer numbers
        """
        if not isinstance(size, int):
            raise TypeError("Size must be an Integer")
        if size <= 0:
            raise TypeError("Size must be a Positive Integer")

        self.__size = size
        self.__gameBoard = [[Gs.GameSquare(row, col) for col in range(size)] for row in range(size)]
        self.__boardTheme = BoardTheme.BlackWhite

    # not in the domain model. from get_game_squares() which returns multiple game squares
    # this will only return one game square
    def get_game_square(self, row, col):
        """
        Returns the game square at coordinate (row,col) on the board.
        Row and Col must be within the boundaries of the size of the board and
        an integer.
        return: gameBoard[row][col]
        """
        if not isinstance(row, int):
            raise TypeError("Row must be an Integer")
        if not isinstance(col, int):
            raise TypeError("Col must be an Integer")
        if row < 0 or row > self.__size:
            raise IndexError("Row must be a within the bounds of 0 to " + str(self.__size))
        if col < 0 or col > self.__size:
            raise IndexError("Col must be a within the bounds of 0 to " + str(self.__size))

        return self.__gameBoard[row][col]

    # renamed this from get_game_squares() to be more clear
    # there should be no reason to get multiple game squares at once
    # unless its the whole board game
    def get_game_board(self):
        """
        Returns the gameBoard.
        return: 2D array of gameSquare
        """
        return self.__gameBoard

    def get_board_theme(self):
        """
        Returns boards current theme which is a type BoardTheme enum
        return BoardTheme.Type
        """
        return self.__boardTheme

    def set_board_theme(self, theme):
        """
        Changes the boardTheme to a new one
        The parameter theme is required to be a BoardTheme enum
        """
        if not isinstance(theme, BoardTheme):
            raise TypeError("Theme must be a type BoardTheme enum")

        self.__boardTheme = theme

    # Added functions not in domain model
    def get_size(self):
        """
        returns the size of the board
        return: Integer
        """
        return self.__size

    def print_game_board(self):
        """
        For visual representation of the board. prints the coordinates of the board square
        and current pieces in the board.
        """
        board_row_col = [[(col.get_row(), col.get_col()) for col in row] for row in self.__gameBoard]
        board_pieces = [[col.get_occupying_piece() for col in row] for row in self.__gameBoard]
        print("Board Initialized")
        [print(row) for row in board_row_col]
        [print(row) for row in board_pieces]
        mock_piece = mock.Mock()
        mock_piece.method = mock.MagicMock(name="Piece")
        
        board_row_col = [[(col.get_row(), col.get_col()) for col in row] for row in self.__gameBoard]
        board_pieces = [[col.get_occupying_piece() for col in row] for row in self.__gameBoard]
        print("\nBoard added mock piece")
        [print(row) for row in board_row_col]
        [print(row) for row in board_pieces]


class BoardTheme(Enum):
    """
    Enum for a list of color that the board can change into.

    """
    BlackWhite = 1
    GreenYellow = 2
    DarkBrownLightBrown = 3


def test_board():
    for x in range(1, 101):
        my_board = Board(x)
        row = random.randint(0, x-1)
        col = random.randint(0, x-1)
        # test size of the board
        assert my_board.get_size() == x
        # test if row and col are correct
        assert len(my_board.get_game_board()) == x
        assert len(my_board.get_game_board()[x-1]) == x
        # test if a random game square that is within the bounds of the board is
        # in the right row and right col
        assert my_board.get_game_square(row, col) in my_board.get_game_board()[row]
        assert my_board.get_game_square(row, col) in [r for r in my_board.get_game_board()[row]]
        # test if the initialized board square in board has None for occupying_piece
        assert my_board.get_game_square(row, col).get_occupying_piece() is None
        # test theme is black white at default
        assert my_board.get_board_theme() is BoardTheme.BlackWhite
        # test if changing theme of board works
        new_board_theme = random.choice(list(BoardTheme))
        my_board.set_board_theme(new_board_theme)
        assert my_board.get_board_theme() is new_board_theme


if __name__ == '__main__':
    myBoard = Board(5)
    myBoard.print_game_board()
