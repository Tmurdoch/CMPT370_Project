# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch


class GameSquare:
    """
    Game square are the fundamental building blocks that make up a game board.  They have a position
    and may be occupied by a game piece.

    Attributes:
        __row: int: row coordinate in the board list (first index of 2D board list)
        __col: int: column coordinate in the board list (second index of 2D board list)
        __occupyingPiece: A type piece currently occupying the square
    """

    def __init__(self, row, col):
        """
        This will initialize a GameSquare.  Initially game squares have no pieces occupying them.
        :param row: int: row coordinate of the game square (first index of 2D board list)
        :param col: int: column coordinate  of the game square (second index of 2D board list)
        """
        if not isinstance(row, int):
            raise TypeError("Row must be an Integer")
        if not isinstance(col, int):
            raise TypeError("Col must be an Integer")
        if row < 0:
            raise IndexError("Row must be a Positive Integer")
        if col < 0:
            raise IndexError("Col must be a Positive Integer")

        self.__row = row
        self.__col = col
        self.__occupyingPiece = None

    def set_row(self, row):
        """
        Sets the gameSquare row to a new row
        :param row: int: New game square row, must be positive
        """
        if not isinstance(row, int):
            raise TypeError("Row must be an Integer")
        if row < 0:
            raise IndexError("Row must be a Positive Integer")

        self.__row = row

    def set_col(self, col):
        """
        Sets the gameSquare col to a new col
        :param col: int: New game square column, must be positive
        """
        if not isinstance(col, int):
            raise TypeError("Col must be an Integer")
        if col < 0:
            raise IndexError("Col must be a Positive Integer")

        self.__col = col

    def get_row(self):
        """ :return: Game square row """
        return self.__row

    def get_col(self):
        """ :return: Game square column """
        return self.__col

    def put_piece_here(self, piece):
        """
        Replace the current occupyingPiece to a new piece
        :param piece: Piece: The game piece you would like to put on this game square
        :return: Piece: The current occupying piece (may be None)
        """
        if self.__occupyingPiece is not None:
            # Take the current occupying piece and then replace it with the new piece.
            return_piece = self.__occupyingPiece
            self.__occupyingPiece = piece
            return return_piece
        else:
            self.__occupyingPiece = piece
            return None

    def get_occupying_piece(self):
        """ :return: Piece: The current occupying game piece """
        return self.__occupyingPiece

    def remove_occupying_piece(self):
        """ Removes the piece on the game square """
        self.__occupyingPiece = None

    def set_row_and_column(self, row, col):
        """
        Sets both the row and the column
        Required for testing purposes
        :param row: int: the new row coordinate of the game square (first index of 2D board list)
        :param col: int: the new column coordinate of the game square (second index of 2D board list)
        """
        self.__row = row
        self.__col = col

    def get_row_and_column(self):
        """ :returns: Game Square row and column as a tuple """
        return self.__row, self.__col
