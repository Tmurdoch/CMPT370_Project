# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch
from Board import Board
from GameSquare import GameSquare
from PieceSet import PieceSet


def checkers_move_maker(origin_square, dest_square, board, other_player_piece_set):
    """
    A helper function to actually execute a checkers move.
    :param origin_square: GameSquare: Where we are moving from
    :param dest_square: GameSquare: Where we are moving to
    :param board: Board: Our game board, needed to identify the pieces we jumped over
    :param other_player_piece_set: The other player's piece set, we need it to capture their pieces
    """

    print("The checkers_move_maker has been called.")
    if not isinstance(origin_square, GameSquare):
        raise Exception("The origin square passed to the checkers_move_maker() was not of type GameSquare object.")

    if not isinstance(dest_square, GameSquare):
        raise Exception("The destination square passed to the checkers_move_maker() was not a GameSquare object.")

    if not isinstance(board, Board):
        raise Exception("The board passed to the checkers_move_maker() was not a Board object.")

    if not isinstance(other_player_piece_set, PieceSet):
        raise Exception("The piece set passed to the checkers_move_maker() was not a PieceSet object.")

    if dest_square.get_occupying_piece() is not None:
        # This move shouldn't have been generated
        raise Exception("Illegal move, this move shouldn't have been generated")
    else:
        if abs(origin_square.get_row() - dest_square.get_row()) == 1:
            # Squares are immediately adjacent, no jumping
            dest_square.put_piece_here(
                origin_square.get_occupying_piece())
            origin_square.remove_occupying_piece()
        elif abs(origin_square.get_row() - dest_square.get_row()) == 2:
            # Single jump

            # Now, we also need to make the capture, need to find which of the four ways we moved
            if ((origin_square.get_row() - dest_square.get_row()) > 0 and
                    (origin_square.get_col() - dest_square.get_col()) > 0):
                # Piece we are trying to jump is in the immediate top left hand corner of the origin square
                square_of_capture = board.get_game_square(origin_square.get_row() - 1,
                                                          origin_square.get_col() - 1)
                if (square_of_capture.get_occupying_piece().get_colour()
                        != origin_square.get_occupying_piece().get_colour()):
                    # The piece we are trying to jump is an enemy piece, go ahead and make the move
                    if other_player_piece_set.capture_piece(square_of_capture.get_occupying_piece()):
                        dest_square.put_piece_here(origin_square.get_occupying_piece())
                        origin_square.remove_occupying_piece()
                        square_of_capture.remove_occupying_piece()
                    else:
                        raise Exception("Unable to capture piece when trying to single up and to the left.")
                else:
                    # You are trying to jump your own piece
                    raise Exception("You are trying to jump your own piece, trying to jump top left hand "
                                    "corner piece")

            if ((origin_square.get_col() - dest_square.get_col())
                    < 0 < (origin_square.get_row() - dest_square.get_row())):
                # Piece we are trying to jump is in the immediate top right hand corner of the origin square
                square_of_capture = board.get_game_square(origin_square.get_row() - 1,
                                                          origin_square.get_col() + 1)
                if (square_of_capture.get_occupying_piece().get_colour()
                        != origin_square.get_occupying_piece().get_colour()):
                    # The piece we are trying to jump is an enemy piece, go ahead and make the move
                    if other_player_piece_set.capture_piece(square_of_capture.get_occupying_piece()):
                        dest_square.put_piece_here(origin_square.get_occupying_piece())
                        origin_square.remove_occupying_piece()
                        square_of_capture.remove_occupying_piece()
                    else:
                        raise Exception("Unable to capture piece when trying to single up and to the right.")
                else:
                    # You are trying to jump your own piece
                    raise Exception("You are trying to jump your own piece, tyring to jump top right hand "
                                    "corner piece")

            if ((origin_square.get_row() - dest_square.get_row())
                    < 0 < (origin_square.get_col() - dest_square.get_col())):
                # Piece we are trying to jump is in the immediate bottom left hand corner of the origin
                # square
                square_of_capture = board.get_game_square(origin_square.get_row() + 1,
                                                          origin_square.get_col() - 1)
                if (square_of_capture.get_occupying_piece().get_colour()
                        != origin_square.get_occupying_piece().get_colour()):
                    # The piece we are trying to jump is an enemy piece, go ahead and make the move
                    if other_player_piece_set.capture_piece(square_of_capture.get_occupying_piece()):
                        dest_square.put_piece_here(origin_square.get_occupying_piece())
                        origin_square.remove_occupying_piece()
                        square_of_capture.remove_occupying_piece()
                    else:
                        raise Exception("Unable to capture piece when trying to single jump down and to the left.")
                else:
                    # You are trying to jump your own piece
                    raise Exception("You are trying to jump your own piece, trying to jump bottom left "
                                    "hand corner piece")

            if ((origin_square.get_row() - dest_square.get_row()) < 0 and
                    (origin_square.get_col() - dest_square.get_col()) < 0):
                # Piece we are trying to jump is in the immediate bottom right hand corner of the origin
                # square
                square_of_capture = board.get_game_square(origin_square.get_row() + 1,
                                                          origin_square.get_col() + 1)
                if (square_of_capture.get_occupying_piece().get_colour()
                        != origin_square.get_occupying_piece().get_colour()):
                    # The piece we are trying to jump is an enemy piece, go ahead and make the move
                    if other_player_piece_set.capture_piece(square_of_capture.get_occupying_piece()):
                        dest_square.put_piece_here(origin_square.get_occupying_piece())
                        origin_square.remove_occupying_piece()
                        square_of_capture.remove_occupying_piece()
                    else:
                        raise Exception("Unable to capture piece when trying to single jump down and to the right.")
                else:
                    # You are trying to jump your own piece
                    raise Exception("You are trying to jump your own piece, trying to jump bottom "
                                    "right hand corner piece")
        else:
            # There are more than one jumps needing to take place
            raise Exception("Cannot handle more than one jump right now")

    # If the checkers coin has reached the far side of the board (and is not yet promoted) then promote
    if dest_square.get_row() == 0:
        print("The destination row is 0, so the checkers coin will now be promoted.")
        dest_square.get_occupying_piece().promote()
