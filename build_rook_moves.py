# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere,
# Michael Luciuk, Thomas Murdoch


def build_rook_moves(input_game_square, input_game):
    """
    Build the list of possible moves for a Rook
    :param input_game_square: GameSquare: The origin game square that you want to build a list of moves for.
    :param input_game: The input game, required to get the game board and game type
    :return list_of_candidate_game_squares: GameSquare[]: List of destination squares the rook can legally move to
    """
    input_piece = input_game_square.get_occupying_piece()
    input_row = input_game_square.get_row()
    input_col = input_game_square.get_col()
    input_board = input_game.get_board()
    candidate_game_squares = []

    # The rook can be moved any number of unoccupied squares in a straight line vertically or horizontally

    # Vertical UP, check from the piece to top row -- (row, col) -> (0, col)
    row_riser = input_row - 1
    while row_riser >= 0:
        if not rook_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), row_riser, input_col):
            # If we get a false back from the rook adder, we hit a piece and should stop looping
            break
        else:
            row_riser -= 1

    # Vertical DOWN, check from piece to bot row -- (row, col) -> (7, col)
    row_faller = input_row + 1
    while row_faller <= input_board.get_size() - 1:
        if not rook_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), row_faller, input_col):
            # If we get a false back from the rook adder, we hit a piece and should stop looping
            break
        else:
            row_faller += 1

    # Horizontal RIGHT, check from piece to right col -- (row, col) -> (row, 7)
    col_riser = input_col + 1
    while col_riser <= input_board.get_size() - 1:
        if not rook_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row, col_riser):
            # If we get a false back from the rook adder, we hit a piece and should stop looping
            break
        else:
            col_riser += 1

    # Horizontal LEFT, check from piece to left col -- (row, col) -> (row, 0)
    col_faller = input_col - 1
    while col_faller >= 0:
        if not rook_move_adder(input_board, candidate_game_squares, input_piece.get_colour(), input_row, col_faller):
            # If we get a false back from the rook adder, we hit a piece and should stop looping
            break
        else:
            col_faller -= 1

    return candidate_game_squares


def rook_move_adder(input_board, candidate_game_squares, input_piece_colour, candidate_row, candidate_col):
    """
    The rook move adder evaluates game squares in the rooks path.  Possible moves are appended to the list.
    :param input_piece_colour: string: The colour of the input piece, used to check if other pieces are friendly
    :param candidate_game_squares:  GameSquare[]: The running list of candidate game squares
    :param input_board: Board: The game board we are working with
    :param candidate_row: int: The row of the square we are considering moving to
    :param candidate_col: int: The col of the square we are considering moving to
    :return: Bool: True until a piece is encountered, and then false once a piece has been encountered
    """
    if input_board.get_game_board()[candidate_row][candidate_col].get_occupying_piece() is not None:
        if input_board.get_game_board()[candidate_row][candidate_col].get_occupying_piece().get_colour() == \
                input_piece_colour:
            # We hit a piece, signal to stop looping
            return False
        if input_board.get_game_board()[candidate_row][candidate_col].get_occupying_piece().get_colour() != \
                input_piece_colour:
            # Capture move, add it to the list and signal to stop looping
            candidate_game_squares.append(input_board.get_game_board()[candidate_row][candidate_col])
            return False
    else:
        # Square was empty, add it to the list and keep going
        candidate_game_squares.append(input_board.get_game_board()[candidate_row][candidate_col])
        return True
