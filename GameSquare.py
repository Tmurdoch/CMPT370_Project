# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch


class GameSquare:
    """
    GameSquare is an object that will contain the index of where it will be
    located in the board. It will also have an object that is currently occupying
    in the gameSquare.
     - row: Integer value that is row coordinate in the board array
     - col: Integer value that is col coordinate in the board array
     - occupyingPiece: A type piece currently occupying the square
    """

    def __init__(self, row, col):
        """
        This will initialize the GameSquare.
        Will contain 2 integer attribute row and col.
        The 2 integers can only be positive integers
        The occupyingPiece starts as None
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
        row: Positive Integer
        """
        if not isinstance(row, int):
            raise TypeError("Row must be an Integer")
        if row < 0:
            raise IndexError("Row must be a Positive Integer")

        self.__row = row

    def set_col(self, col):
        """
        Sets the gameSquare col to a new col
        col: Positive Integer
        """
        if not isinstance(col, int):
            raise TypeError("Col must be an Integer")
        if col < 0:
            raise IndexError("Col must be a Positive Integer")

        self.__col = col

    def get_row(self):
        """
        Returns the gameSquare row
        return: Positive Integer
        """
        return self.__row

    def get_col(self):
        """
        Returns the gameSquare col
        return: Positive Integer
         """
        return self.__col

    def put_piece_here(self, piece):
        """
        Replace the current occupyingPiece to a new piece
        piece must be a Type Piece
        returns current occupying piece if not None
        """

        """
        At the event when occupying piece is not None
        we take the current occupying piece and then replace
        it with the new piece. 
        """
        if self.__occupyingPiece is not None:
            return_piece = self.__occupyingPiece
            self.__occupyingPiece = piece
            return return_piece
        else:
            self.__occupyingPiece = piece
            return None

    def get_occupying_piece(self):
        """
        Returns piece that is occupying the gameSquare
        return: Piece occupyingPiece
        """
        return self.__occupyingPiece

    # Added functions might not be in the domain model yet
    # ------------------------------------------------------------------------------------------------
    # added this because there is no other way to remove a
    # piece on a square
    def remove_occupying_piece(self):
        """
        Sets the occupyingPiece to None
        """
        self.__occupyingPiece = None

    # testing purposes
    def set_row_and_column(self, row, col):
        self.__row = row
        self.__col = col

    # testing purposes
    def get_row_and_column(self):
        return self.__row, self.__col

    # ---------------------------------------------------------------------------------------------------


"""
def test_fail():
    gs_test_fail_1 = GameSquare(8.5, 8)
    gs_test_fail_2 = GameSquare(-1, 5)

    gs_test_1 = GameSquare(6, 6)
    gs_test_1.set_col(7)
    gs_test_1.set_row(7)
    gs_test_1.set_col(-1)
    gs_test_1.set_row(2.5)
    
    assert gs_test_1.get_col() == 8
    assert gs_test_1.get_row() == 8
    assert gs_test_1.get_occupying_piece() is None
    #gs_test_fail = GameSquare(random.uniform(0, 100))
    #gs_test_fail_2 = GameSquare(random.randRange(-100, -1))
    #gs_test = [[GameSquare(row, col) for col in range(100)] for row in range(100)]
"""
