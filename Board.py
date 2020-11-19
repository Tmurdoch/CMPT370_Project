# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from enum import Enum
import GameSquare as Gs


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
        # list comprehension of building board
        # self.__gameBoard = [[Gs.GameSquare(row, col) for col in range(size)] for row in range(size)]
        # for list building board
        self.__gameBoard = []
        for r in range(size):
            row = []
            for c in range(size):
                row.append(Gs.GameSquare(r, c))
            self.__gameBoard.append(row)
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

    # Added functions might not be in the domain model yet
    # ------------------------------------------------------------------------------------------------
    def get_size(self):
        """
        returns the size of the board
        return: Integer
        """
        return self.__size

    def build_chess_board(self, player1_pieces, player2_pieces):
        """
        set up chess pieces on the board
        Player1 on the bottom row 7 and 6 -> 
        row 7 where king, queen, rook... are
        row 6 where pawns are
        Player2 on the top row 0 and 1 -> 
        row 0 where king, queen, rook... are
        row 1 where pawns are
        player1_pieces: list of pieces in pieceSet for player 1
        player2_pieces: list of pieces in pieceSet for player 2
        """
        # indexes of pieces based on where they are on the board
        spec_piece = [4, 3, 0, 7, 2, 5, 1, 6]

        # set up board player 1 pieces
        i = 0
        for col in spec_piece:
            self.__gameBoard[7][col].put_piece_here(player1_pieces[i])
            i += 1
        for col in range(8):
            self.__gameBoard[6][col].put_piece_here(player1_pieces[i])
            i += 1

        # set up board player 2 pieces
        i = 0
        for col in spec_piece:
            self.__gameBoard[0][col].put_piece_here(player2_pieces[i])
            i += 1
        for col in range(8):
            self.__gameBoard[1][col].put_piece_here(player2_pieces[i])
            i += 1

    def build_checkers_board(self, player1_pieces, player2_pieces):
        """
        set up checkers pieces on the board
        Player1 on the bottom row 7, 6, and 5 ->
        row 7 and 5 starts from col index 0
        row 6 starts at index 1
        Player2 on the bottom row 2, 1, and 0 ->
        row 0 and 2 starts from col index 1
        row 1 starts at index 0
        player1_pieces: list of pieces in pieceSet for player 1
        player2_pieces: list of pieces in pieceSet for player 2
        """
        # list of index inside piece set for light player and dark player
        # 0, 4, 8 are indexes in the list of checkers pieces in pieceSet for a player
        # used so we can evenly take away checkers and put it in the board
        checker_indexes = [[0, 4, 8], [0, 4, 8]]
        # iterating through columns 0, 2, 4, 6
        # these are the column index where the piece will be set
        for col in range(0, 8, 2):
            # put the checkrs piece from player 1 and player 2 piece set using specific index
            # in specific row, col in board
            # 7, 5 are for the light player and 1 is for dark player these
            # these numbers are specific rows where player piece start from edge column
            self.__gameBoard[7][col].put_piece_here(player1_pieces[checker_indexes[0][0]])
            self.__gameBoard[5][col].put_piece_here(player1_pieces[checker_indexes[1][1]])
            self.__gameBoard[1][col].put_piece_here(player2_pieces[checker_indexes[0][2]])
            checker_indexes[0][0] += 1
            checker_indexes[1][1] += 1
            checker_indexes[0][2] += 1

        # iterating through columns 1, 3, 5, 7
        # these are the column index where the piece will be set
        for col in range(1, 8, 2):
            # put the checkrs piece from player 1 or player 2 piece set using specific index
            # in specific row, col in board
            # 6 is for the light player and 2, 0 are for dark player
            # these numbers are specific rows where player piece start from edge column
            self.__gameBoard[6][col].put_piece_here(player1_pieces[checker_indexes[0][1]])
            self.__gameBoard[2][col].put_piece_here(player2_pieces[checker_indexes[1][2]])
            self.__gameBoard[0][col].put_piece_here(player2_pieces[checker_indexes[1][0]])
            checker_indexes[0][1] += 1
            checker_indexes[1][2] += 1
            checker_indexes[1][0] += 1

    def switch_sides(self):
        """
        Rotates the board as if it is being rotated at 180 degrees
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
        For visual representation of the board. prints the coordinates of the board square
        and current pieces in the board.
        """
        # separating row and column to be able to print legibly
        # shows coordinates in tuples and shows pieces occupying the game squares
        # list comp
        # board_row_col = [[(col.get_row(), col.get_col()) for col in row] for row in self.__gameBoard]
        # board_pieces = [[col.get_occupying_piece() for col in row] for row in self.__gameBoard]
        # for list

        # creates a 2d list of (row, col) of the board
        board_row_col = []
        for r in self.__gameBoard:
            column = []
            for c in r:
                column.append((c.get_row(), c.get_col()))
            board_row_col.append(column)

        # creates a 2d list of pieces of the board
        board_pieces = []
        empty_string = "E            "
        for r in self.__gameBoard:
            column = []
            for c in r:
                if c.get_occupying_piece() is None:
                    column.append([empty_string])
                else:
                    if type(c.get_occupying_piece()).__name__ is "CheckersCoin":
                        column.append([type(c.get_occupying_piece()).__name__ + " "])
                    elif type(c.get_occupying_piece()).__name__ is "Pawn":
                        column.append([type(c.get_occupying_piece()).__name__+"  "])
                        empty_string = "E     "
                    elif type(c.get_occupying_piece()).__name__ is "Rook":
                        column.append([type(c.get_occupying_piece()).__name__ + "  "])
                        empty_string = "E     "
                    elif type(c.get_occupying_piece()).__name__ is "King":
                        column.append([type(c.get_occupying_piece()).__name__ + "  "])
                        empty_string = "E     "
                    elif type(c.get_occupying_piece()).__name__ is "Queen":
                        column.append([type(c.get_occupying_piece()).__name__ + " "])
                        empty_string = "E     "
                    else:
                        column.append([type(c.get_occupying_piece()).__name__])

            board_pieces.append(column)

        # creates a 2d list of colour of the pieces on the board
        board_pieces_colour = []
        empty_string = "     "
        for r in self.__gameBoard:
            column = []
            for c in r:
                if c.get_occupying_piece() is None:
                    column.append([empty_string])
                else:
                    if c.get_occupying_piece().get_colour() is "Red":
                        column.append([c.get_occupying_piece().get_colour()+"  "])
                    else:
                        column.append([c.get_occupying_piece().get_colour()])
            board_pieces_colour.append(column)

        print("\nBoard Initialized\n\nBoard Squares Coordinates:")
        [print(row) for row in board_row_col]
        print("\nBoard Squares Occupied_Pieces")
        [print(row) for row in board_pieces]
        print("\nBoard Pieces Colour")
        [print(row) for row in board_pieces_colour]
        
        # board_row_col = [[(col.get_row(), col.get_col()) for col in row] for row in self.__gameBoard]
        # board_pieces = [[col.get_occupying_piece() for col in row] for row in self.__gameBoard]
        # print("\nBoard added mock piece")
        # [print(row) for row in board_row_col]
        # [print(row) for row in board_pieces]

    # --------------------------------------------------------------------------------------------------


class BoardTheme(Enum):
    """
    Enum for a list of color that the board can change into.

    """
    BlackWhite = 1
    GreenYellow = 2
    DarkBrownLightBrown = 3

