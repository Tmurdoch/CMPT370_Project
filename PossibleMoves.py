# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch

import random


class PossibleMoves:
    """
    The class defining possible moves for a piece
    Attributes:
        __piece: piece object wishing to move, moves to be calculated
        __squares_you_can_move_to: List of GameSquares you can to move to
        __game: game object to get player locations, etc
        __board: board object, created during initialization
    """
    def __init__(self, game_square, game_obj):
        self.__game_square = game_square
        self.__piece = game_square.get_occupying_piece()
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

            if self.__piece.get_promotion_status():
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

        elif self.__game_type.lower() == "chess":

            if type(self.__piece).__name__ == "King":
                # A king can move one square in any direction (horizontally,
                #  vertically, or diagonally), unless the square is already occupied by a friendly piece, or the move
                #  would place the king in check

                # Check one square left
                if 0 <= self.__col - 1 < self.__board.get_size():
                    one_square_left = self.__board.get_game_square(self.__row, self.__col - 1)
                    if one_square_left.get_occupying_piece() is None:
                        # Empty, we can move there
                        list_of_candidate_game_squares.append(one_square_left)
                    elif one_square_left.get_occupying_piece().get_colour() != self.__piece.get_colour():
                        # Opponent piece there
                        list_of_candidate_game_squares.append(one_square_left)

                # Check one square right
                if 0 <= self.__col + 1 < self.__board.get_size():
                    one_square_right = self.__board.get_game_square(self.__row, self.__col + 1)
                    if one_square_right.get_occupying_piece() is None:
                        # Empty, we can move there
                        list_of_candidate_game_squares.append(one_square_right)
                    elif one_square_right.get_occupying_piece().get_colour() != self.__piece.get_colour():
                        # Opponent piece there
                        list_of_candidate_game_squares.append(one_square_right)

                # Check one square forward
                if 0 <= self.__row - 1 < self.__board.get_size():
                    one_square_forward = self.__board.get_game_square(self.__row - 1, self.__col)
                    if one_square_forward.get_occupying_piece() is None:
                        # Empty, we can move there
                        list_of_candidate_game_squares.append(one_square_forward)
                    elif one_square_forward.get_occupying_piece().get_colour() != self.__piece.get_colour():
                        # Opponent piece there
                        list_of_candidate_game_squares.append(one_square_forward)

                # Check one square backwards
                if 0 <= self.__row + 1 < self.__board.get_size():
                    one_square_backward = self.__board.get_game_square(self.__row + 1, self.__col)
                    if one_square_backward.get_occupying_piece() is None:
                        # Empty, we can move there
                        list_of_candidate_game_squares.append(one_square_backward)
                    elif one_square_backward.get_occupying_piece().get_colour() != self.__piece.get_colour():
                        # Opponent piece there
                        list_of_candidate_game_squares.append(one_square_backward)

                # Check top left corner
                if 0 <= self.__row - 1 < self.__board.get_size() or 0 <= self.__col - 1 < self.__board.get_size():
                    top_left = self.__board.get_game_square(self.__row - 1, self.__col - 1)
                    if top_left.get_occupying_piece() is None:
                        # Empty, we can move there
                        list_of_candidate_game_squares.append(top_left)
                    elif top_left.get_occupying_piece().get_colour() != self.__piece.get_colour():
                        # Opponent piece there
                        list_of_candidate_game_squares.append(top_left)

                # Check top right corner
                if 0 <= self.__row - 1 < self.__board.get_size() or 0 <= self.__col + 1 < self.__board.get_size():
                    top_right = self.__board.get_game_square(self.__row - 1, self.__col + 1)
                    if top_right.get_occupying_piece() is None:
                        # Empty, we can move there
                        list_of_candidate_game_squares.append(top_right)
                    elif top_right.get_occupying_piece().get_colour() != self.__piece.get_colour():
                        # Opponent piece there
                        list_of_candidate_game_squares.append(top_right)

                # Check bottom left corner
                if 0 <= self.__row + 1 < self.__board.get_size() or 0 <= self.__col - 1 < self.__board.get_size():
                    bottom_left = self.__board.get_game_square(self.__row + 1, self.__col - 1)
                    if bottom_left.get_occupying_piece() is None:
                        # Empty, we can move there
                        list_of_candidate_game_squares.append(bottom_left)
                    elif bottom_left.get_occupying_piece().get_colour() != self.__piece.get_colour():
                        # Opponent piece there
                        list_of_candidate_game_squares.append(bottom_left)

                # Check bottom right corner
                if 0 <= self.__row + 1 < self.__board.get_size() or 0 <= self.__col + 1 < self.__board.get_size():
                    bottom_right = self.__board.get_game_square(self.__row + 1, self.__col + 1)
                    if bottom_right.get_occupying_piece() is None:
                        # Empty, we can move there
                        list_of_candidate_game_squares.append(bottom_right)
                    elif bottom_right.get_occupying_piece().get_colour() != self.__piece.get_colour():
                        # Opponent piece there
                        list_of_candidate_game_squares.append(bottom_right)

                # TODO: Identify castle as one of the possible moves Castling is permissible provided all of the
                #  following conditions hold:
                # The castling must be kingside or queenside.
                # Neither the king nor the chosen rook has previously moved.
                # There are no pieces between the king and the chosen rook.
                # The king is not currently in check.
                # The king does not pass through a square that is attacked by an enemy piece.
                # The king does not end up in check. (True of any legal move.)

            elif type(self.__piece).__name__ == "Queen":
                # The queen can be moved any number of unoccupied squares in a straight line
                # vertically, horizontally, or diagonally, thus combining the moves of the rook and bishop
                # Vertical movements
                for row_of_game_square in self.__board.get_game_board():
                    if row_of_game_square[self.__col].get_occupying_piece() is None:
                        list_of_candidate_game_squares.append(row_of_game_square[self.__col])
                    elif row_of_game_square[self.__col].get_occupying_piece().get_colour() != self.__piece.get_colour():
                        list_of_candidate_game_squares.append(row_of_game_square[self.__col])

                # Horizontal movements
                for col_of_game_square in range(self.__board.get_size()):
                    if self.__board.get_game_board[self.__row][col_of_game_square] is None:
                        list_of_candidate_game_squares.append(
                            self.__board.get_game_board[self.__row][col_of_game_square])
                    elif self.__board.get_game_board[self.__row][col_of_game_square].get_occupying_piece().get_colour()\
                            != self.__piece.get_colour():
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
                            if self.__board.get_game_board().get_game_square(row, col).get_occupying_piece()\
                                    .get_colour() != self.__piece.get_colour():
                                list_of_candidate_game_squares \
                                    .append(self.__board.get_game_board().get_game_square(row, col))

            elif type(self.__piece).__name__ == "Bishop":
                # The bishop can be moved any number of unoccupied squares in a straight line diagonally
                for row in range(self.__board.get_size()):
                    for col in range(self.__board.get_size()):
                        if abs(self.__row - row) == abs(self.__col - col):
                            # on the diagonal
                            if self.__board.get_game_board().get_game_square(row, col) is None:
                                list_of_candidate_game_squares \
                                    .append(self.__board.get_game_board().get_game_square(row, col))
                            if self.__board.get_game_board().get_game_square(row, col).get_occupying_piece()\
                                    .get_colour() != self.__piece.get_colour():
                                list_of_candidate_game_squares \
                                    .append(self.__board.get_game_board().get_game_square(row, col))

            elif type(self.__piece).__name__ == "Knight":

                # moves up and to the right

                if (self.__board.get_game_square(self.__row - 2, self.__col + 1).get_occupying_piece().get_colour()
                        is not self.__piece.get_colour()):
                    # if spot has enemy piece on it
                    if self.__board.get_game_square(self.__row - 2, self.__col + 1) is not None:
                        # need to find out how to capture a piece
                        up_right_square = self.__board.get_game_square(self.__row - 2, self.__col + 1)
                        list_of_candidate_game_squares.append(up_right_square)

                # moves up and to the left
                elif (self.__board.get_game_square(self.__row - 2, self.__col - 1).get_occupying_piece().get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row - 2, self.__col - 1) is not None:
                        # need to find out how to capture a piece
                        up_left_square = self.__board.get_game_square(self.__row - 2, self.__col - 1)
                        list_of_candidate_game_squares.append(up_left_square)

                # moves down and to the right
                elif (self.__board.get_game_square(self.__row + 2, self.__col + 1).get_occupying_piece().get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row + 2, self.__col + 1) is not None:
                        # need to find out how to capture a piece
                        down_right_square = self.__board.get_game_square(self.__row + 2, self.__col + 1)
                        list_of_candidate_game_squares.append(down_right_square)

                # moves down and to the left
                elif (self.__board.get_game_square(self.__row + 2, self.__col - 1).get_occupying_piece().get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row + 2, self.__col - 1) is not None:
                        # need to find out how to capture a piece
                        down_left_square = self.__board.get_game_square(self.__row + 2, self.__col - 1)
                        list_of_candidate_game_squares.append(down_left_square)

                # moves right and up
                elif (self.__board.get_game_square(self.__row - 1, self.__col + 2).get_occupying_piece().get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row - 1, self.__col + 2) is not None:
                        # need to find out how to capture a piece
                        right_up_square = self.__board.get_game_square(self.__row - 1, self.__col + 2)
                        list_of_candidate_game_squares.append(right_up_square)

                # moves right and down
                elif (self.__board.get_game_square(self.__row + 1, self.__col + 2).get_occupying_piece().get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row + 1, self.__col + 2) is not None:
                        # need to find out how to capture a piece
                        right_down_square = self.__board.get_game_square(self.__row + 1, self.__col + 2)
                        list_of_candidate_game_squares.append(right_down_square)

                # moves left and up
                elif (self.__board.get_game_square(self.__row - 1, self.__col - 2).get_occupying_piece().get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row - 1, self.__col - 2) is not None:
                        # need to find out how to capture a piece
                        left_up_square = self.__board.get_game_square(self.__row - 1, self.__col - 2)
                        list_of_candidate_game_squares.append(left_up_square)

                # moves left and down
                elif (self.__board.get_game_square(self.__row + 1, self.__col - 2).get_occupying_piece().get_colour()
                      is not self.__piece.get_colour()):
                    if self.__board.get_game_square(self.__row + 1, self.__col - 2) is not None:
                        # need to find out how to capture a piece
                        left_down_square = self.__board.get_game_square(self.__row + 1, self.__col - 2)
                        list_of_candidate_game_squares.append(left_down_square)

            elif type(self.__piece).__name__ == "Rook":
                # The rook can be moved any number of unoccupied squares in a straight line vertically or horizontally

                # Vertical movements

                # check from piece to top row -- (row, col) -> (0, col)
                # will stop until sees a peace
                # if piece friendly stop
                # if non friendly add add (row, col) to possible moves but also stops
                row_pos = self.__row
                while row_pos != 0:
                    row_pos -= 1
                    if self.__board.get_game_board()[row_pos][self.__col].get_occupying_piece() is not None:
                        if self.__board.get_game_board()[row_pos][self.__col].get_occupying_piece().get_colour() == \
                                self.__piece.get_colour():
                            break
                        if self.__board.get_game_board()[row_pos][self.__col].get_occupying_piece().get_colour() != \
                                self.__piece.get_colour():
                            list_of_candidate_game_squares.append(self.__board.get_game_board()[row_pos][self.__col])
                            break
                    else:
                        list_of_candidate_game_squares.append(self.__board.get_game_board()[row_pos][self.__col])

                # check from piece to bot row -- (row, col) -> (7, col)
                # will stop until sees a peace
                # if piece friendly stop
                # if non friendly add add (row, col) to possible moves but also stops
                row_neg = self.__row
                while row_neg != 7:
                    row_pos += 1
                    if self.__board.get_game_board()[row_neg][self.__col].get_occupying_piece() is not None:
                        if self.__board.get_game_board()[row_neg][self.__col].get_occupying_piece().get_colour() == \
                                self.__piece.get_colour():
                            break
                        if self.__board.get_game_board()[row_neg][self.__col].get_occupying_piece().get_colour() != \
                                self.__piece.get_colour():
                            list_of_candidate_game_squares.append(self.__board.get_game_board()[row_neg][self.__col])
                            break
                    else:
                        list_of_candidate_game_squares.append(self.__board.get_game_board()[row_neg][self.__col])

                # Horizontal movements

                # check from piece to left col -- (row, col) -> (row, 0)
                # will stop until sees a peace
                # if piece friendly stop
                # if non friendly add add (row, col) to possible moves but also stops
                col_pos = self.__col
                while col_pos != 0:
                    col_pos -= 1
                    if self.__board.get_game_board()[self.__row][col_pos].get_occupying_piece() is not None:
                        if self.__board.get_game_board()[self.__row][col_pos].get_occupying_piece().get_colour() == \
                                self.__piece.get_colour():
                            break
                        if self.__board.get_game_board()[self.__row][col_pos].get_occupying_piece().get_colour() != \
                                self.__piece.get_colour():
                            list_of_candidate_game_squares.append(self.__board.get_game_board()[self.__row][col_pos])
                            break
                    else:
                        list_of_candidate_game_squares.append(self.__board.get_game_board()[self.__row][col_pos])

                # check from piece to right col -- (row, col) -> (row, 7)
                # will stop until sees a peace
                # if piece friendly stop
                # if non friendly add add (row, col) to possible moves but also stops
                col_pos = self.__col
                while col_pos != 7:
                    col_pos += 1
                    if self.__board.get_game_board()[self.__row][col_pos].get_occupying_piece() is not None:
                        if self.__board.get_game_board()[self.__row][
                            col_pos].get_occupying_piece().get_colour() == \
                                self.__piece.get_colour():
                            break
                        if self.__board.get_game_board()[self.__row][
                            col_pos].get_occupying_piece().get_colour() != \
                                self.__piece.get_colour():
                            list_of_candidate_game_squares.append(
                                self.__board.get_game_board()[self.__row][col_pos])
                            break
                    else:
                        list_of_candidate_game_squares.append(
                            self.__board.get_game_board()[self.__row][col_pos])
                """
            for row_of_game_square in self.__board.get_game_board():
                    if row_of_game_square[self.__col].get_occupying_piece() is None:
                        list_of_candidate_game_squares.append(row_of_game_square[self.__col])
                    elif row_of_game_square[self.__col].get_occupying_piece().get_colour() != self.__piece.get_colour():
                        list_of_candidate_game_squares.append(row_of_game_square[self.__col])

                # Horizontal movements
                # horizontal stop
                h_stop = False
                for col_of_game_square in range(self.__board.get_size()):
                    if self.__board.get_game_board()[self.__row][col_of_game_square] is None and not h_stop:
                        list_of_candidate_game_squares.append(
                            self.__board.get_game_board()[self.__row][col_of_game_square])
                    elif self.__board.get_game_board()[self.__row][col_of_game_square].get_occupying_piece()\
                            .get_colour() == self.__piece.get_colour():
                        h_stop = True
                    elif self.__board.get_game_board()[self.__row][col_of_game_square].get_occupying_piece()\
                            .get_colour() != self.__piece.get_colour() and not h_stop:
                        list_of_candidate_game_squares.append(
                            self.__board.get_game_board()[self.__row][col_of_game_square])
                """

            elif type(self.__piece).__name__ == "Pawn":
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
                # Top left corner
                if 0 <= self.__row - 1 < self.__board.get_size() or 0 <= self.__col - 1 < self.__board.get_size():
                    top_left = self.__board.get_game_square(self.__row - 1, self.__col - 1)
                    if top_left.get_occupying_piece() is not None:
                        # Then there is a piece there, look at what colour it is
                        if self.__game_square().get_occupying_piece().get_colour() != top_left\
                                .get_occupying_piece().get_colour():
                            # It is an opponent piece, go ahead and add this as a square they can move to
                            list_of_candidate_game_squares.append(top_left)

                # Top right corner
                if 0 <= self.__row - 1 < self.__board.get_size() or 0 <= self.__col + 1 < self.__board.get_size():
                    top_right = self.__board.get_game_square(self.__row - 1, self.__col + 1)
                    if top_right.get_occupying_piece() is not None:
                        # Then there is a piece there, look at what colour it is
                        if self.__game_square().get_occupying_piece().get_colour() != top_right.get_occupying_piece()\
                                .get_colour():
                            # It is an opponent piece, go ahead and add this as a square they can move to
                            list_of_candidate_game_squares.append(top_right)

                self.__squares_you_can_move_to = list_of_candidate_game_squares
            else:
                # Could not identify the type of piece
                return -1

            return list_of_candidate_game_squares

        else:
            # Game mode is neither "chess" nor "checkers"
            return self.__game_type.lower()

    def select_best(self, candidate_game_squares):
        """
        Chooses and return the best game square to move to from a list of candidate squares
        :param: List of GameSquares to choose from
        :return: GameSquare, the best game square to move to. Returns None if there are no moves for that square
        """
        if not candidate_game_squares:
            # List of moves is empty
            return None
        elif len(candidate_game_squares) == 1:
            # The is only one move, it has to be the best
            return candidate_game_squares[0]
        else:
            # TODO: Some AI code to evaluate the list of moves to choose the best one, in the mean time we are jsut
            #  returning the first one in the list
            # Right now we will just return a random one
            random_index = (random.randrange(0, len(candidate_game_squares), 1))
            return candidate_game_squares[random_index]

    def get_list_of_squares_you_can_move_to(self):
        """
        :return: GameSquare[]: A list of game squares that are legal to move to
        """
        return self.__squares_you_can_move_to
