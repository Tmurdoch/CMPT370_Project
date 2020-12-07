# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import GameSquare as Gs


class Board:
    """
    Square checkers board.  Board is made up of a 2D list of game squares.

    Attributes:
        __size: int: Board size, board is always square so length and width are the same.
        __gameBoard: 2D list of GameSquares.
    """

    def __init__(self, size):
        """
        This will initialize the gameBoard as a square 2D list of GameSquares.  GameSquare gameBoard[size][size].
        :param size: int: Board size, must be positive
        """
        if not isinstance(size, int):
            raise TypeError("Board size must be an Integer")
        if size <= 0:
            raise TypeError("Board size must be a Positive Integer")

        self.__size = size
        self.__gameBoard = []
        for r in range(size):
            row = []
            for c in range(size):
                row.append(Gs.GameSquare(r, c))
            self.__gameBoard.append(row)

    def get_game_square(self, row, col):
        """
        :param row: int: Row of the game board (first index of 2D board list)
        :param col: int: Column of the game board (second index of 2D board list)
        :return: GameSquare: the game square at coordinate (row, col) on the board.
        """
        if not isinstance(row, int):
            raise TypeError("Row must be an Integer")
        if not isinstance(col, int):
            raise TypeError("Col must be an Integer")
        if row < 0 or row > self.__size:
            raise IndexError(
                "Row must be a within the bounds of 0 to " + str(self.__size))
        if col < 0 or col > self.__size:
            raise IndexError(
                "Col must be a within the bounds of 0 to " + str(self.__size))

        return self.__gameBoard[row][col]

    def get_game_board(self):
        """ :return: GameBoard: The game board as a 2D list of game squares. """
        return self.__gameBoard

    def get_size(self):
        """ :return: int: Board size """
        return self.__size

    def build_chess_board(self, player1_pieces, player2_pieces):
        """
        Set up chess pieces in their staring positions on the board
        :param player1_pieces: Piece[]: A list of player 1's live pieces
        :param player2_pieces: Piece[]: A list of player 2's live pieces
        """
        spec_piece = [4, 3, 0, 7, 2, 5, 1, 6]  # indexes of pieces based on where they are on the board

        # Put the first players pieces on the board
        i = 0
        for col in spec_piece:
            self.__gameBoard[7][col].put_piece_here(player1_pieces[i])
            i += 1
        for col in range(8):
            self.__gameBoard[6][col].put_piece_here(player1_pieces[i])
            i += 1

        # Put the second players pieces on the board
        i = 0
        for col in spec_piece:
            self.__gameBoard[0][col].put_piece_here(player2_pieces[i])
            i += 1
        for col in range(8):
            self.__gameBoard[1][col].put_piece_here(player2_pieces[i])
            i += 1

    def build_checkers_board(self, player1_pieces, player2_pieces):
        """
        Set up checkers pieces in their staring positions on the board
        :param player1_pieces: Piece[]: A list of player 1's live pieces
        :param player2_pieces: Piece[]: A list of player 2's live pieces
        """
        # Put the first players pieces on the board
        self.__gameBoard[7][0].put_piece_here(player1_pieces[0])
        self.__gameBoard[7][2].put_piece_here(player1_pieces[1])
        self.__gameBoard[7][4].put_piece_here(player1_pieces[2])
        self.__gameBoard[7][6].put_piece_here(player1_pieces[3])
        self.__gameBoard[6][1].put_piece_here(player1_pieces[4])
        self.__gameBoard[6][3].put_piece_here(player1_pieces[5])
        self.__gameBoard[6][5].put_piece_here(player1_pieces[6])
        self.__gameBoard[6][7].put_piece_here(player1_pieces[7])
        self.__gameBoard[5][0].put_piece_here(player1_pieces[8])
        self.__gameBoard[5][2].put_piece_here(player1_pieces[9])
        self.__gameBoard[5][4].put_piece_here(player1_pieces[10])
        self.__gameBoard[5][6].put_piece_here(player1_pieces[11])

        # Put the second players pieces on the board
        self.__gameBoard[0][1].put_piece_here(player2_pieces[0])
        self.__gameBoard[0][3].put_piece_here(player2_pieces[1])
        self.__gameBoard[0][5].put_piece_here(player2_pieces[2])
        self.__gameBoard[0][7].put_piece_here(player2_pieces[3])
        self.__gameBoard[1][0].put_piece_here(player2_pieces[4])
        self.__gameBoard[1][2].put_piece_here(player2_pieces[5])
        self.__gameBoard[1][4].put_piece_here(player2_pieces[6])
        self.__gameBoard[1][6].put_piece_here(player2_pieces[7])
        self.__gameBoard[2][1].put_piece_here(player2_pieces[8])
        self.__gameBoard[2][3].put_piece_here(player2_pieces[9])
        self.__gameBoard[2][5].put_piece_here(player2_pieces[10])
        self.__gameBoard[2][7].put_piece_here(player2_pieces[11])

    def switch_sides(self):
        """
        Rotates the board as if it is being physically rotated 180 degrees Board needs to rotate so the current
        player is at the bottom of the board.  This is needed to make possible move logic to unidirectional
        """
        new_board = []
        for r in range(self.__size):
            row = []
            for c in range(self.__size):
                # switch row and col so it would have the same root (0,0) at top left
                new_gamesquare = self.__gameBoard[r][c]
                new_gamesquare.set_row(self.__size - 1 - r)
                new_gamesquare.set_col(self.__size - 1 - c)
                row.insert(0, new_gamesquare)

            new_board.insert(0, row)

        self.__gameBoard = new_board

    def print_game_board(self):
        """
        - This method is just for testing -
        For visual representation of the board. This prints the coordinates of the board squares
        and any game pieces currently on the board.
        """

        # Creates a 2d list of (row, col) of the board
        board_row_col = []
        for r in self.__gameBoard:
            column = []
            for c in r:
                column.append((c.get_row(), c.get_col()))
            board_row_col.append(column)

        # Creates a 2d list of pieces of the board
        board_pieces = []
        empty_string = "E            "
        for r in self.__gameBoard:
            column = []
            for c in r:
                if c.get_occupying_piece() is None:
                    column.append([empty_string])
                else:
                    if type(c.get_occupying_piece()).__name__ == "CheckersCoin":
                        column.append(
                            [type(c.get_occupying_piece()).__name__ + " "])
                    elif type(c.get_occupying_piece()).__name__ == "Pawn":
                        column.append(
                            [type(c.get_occupying_piece()).__name__+"  "])
                        empty_string = "E     "
                    elif type(c.get_occupying_piece()).__name__ == "Rook":
                        column.append(
                            [type(c.get_occupying_piece()).__name__ + "  "])
                        empty_string = "E     "
                    elif type(c.get_occupying_piece()).__name__ == "King":
                        column.append(
                            [type(c.get_occupying_piece()).__name__ + "  "])
                        empty_string = "E     "
                    elif type(c.get_occupying_piece()).__name__ == "Queen":
                        column.append(
                            [type(c.get_occupying_piece()).__name__ + " "])
                        empty_string = "E     "
                    else:
                        column.append([type(c.get_occupying_piece()).__name__])

            board_pieces.append(column)

        # Creates a 2d list of colour of the pieces on the board
        board_pieces_colour = []
        empty_string = "     "
        for r in self.__gameBoard:
            column = []
            for c in r:
                if c.get_occupying_piece() is None:
                    column.append([empty_string])
                else:
                    if c.get_occupying_piece().get_colour() is "Red":
                        column.append(
                            [c.get_occupying_piece().get_colour()+"  "])
                    else:
                        column.append([c.get_occupying_piece().get_colour()])
            board_pieces_colour.append(column)

        print("\nBoard Initialized\n\nBoard Squares Coordinates:")
        [print(row) for row in board_row_col]
        print("\nBoard Squares Occupied_Pieces")
        [print(row) for row in board_pieces]
        print("\nBoard Pieces Colour")
        [print(row) for row in board_pieces_colour]
