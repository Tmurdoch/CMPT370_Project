# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from Pieces import King, Rook, Pawn


def chess_move_maker(origin_square, dest_square, board, other_player_piece_set, player, game):
    """
    A helper function to actually execute a chess move.
    :param origin_square: GameSquare: Where we are moving from
    :param dest_square: GameSquare: Where we are moving to
    :param board: Board: Our game board, needed in case of a castle
    :param other_player_piece_set: The other player's piece set, we need it to capture their pieces
    :param player: The player who is actually making the move, needed to update the last move
    :param game: The game to know what player is currently at the bottom of the board
    """

    castle_move = False

    # First check if the move is a castle
    if origin_square.get_row() == 7 and origin_square.get_col() == 4 \
            and isinstance(origin_square.get_occupying_piece(), King) and player is game.get_light_player():
        # The king was chosen, check to see if the destination squares were rooks

        # Check king-side
        if dest_square.get_row() == 7 and dest_square.get_col() == 7 \
                and isinstance(dest_square.get_occupying_piece(), Rook):
            # We have the right pieces, let's confirm that neither piece have moved yet
            if not origin_square.get_occupying_piece().get_moved_yet_status() \
                    and not dest_square.get_occupying_piece().get_moved_yet_status():
                # We are good to go ahead and make the king-side castle
                king_dest_square = board.get_game_square(7, 6)
                rook_dest_square = board.get_game_square(7, 5)

                # These destination squares should be empty, but let's check
                if king_dest_square.get_occupying_piece() is None \
                        and rook_dest_square.get_occupying_piece() is None:
                    # We are good to go, execute the castle
                    king_dest_square.put_piece_here(origin_square.get_occupying_piece())
                    rook_dest_square.put_piece_here(dest_square.get_occupying_piece())
                    origin_square.remove_occupying_piece()
                    dest_square.remove_occupying_piece()
                    castle_move = True
                    rook_dest_square.get_occupying_piece.move()  # Update that our rook has moved
                else:
                    raise Exception("The castle move should not have been generated because there are pieces "
                                    "in the way, King-side error")

        # Check queen-side
        if dest_square.get_row() == 7 and dest_square.get_col() == 0 and \
                isinstance(dest_square.get_occupying_piece(), Rook):
            # We have the right pieces, let's confirm that neither piece have moved yet
            if not origin_square.get_occupying_piece().get_moved_yet_status() and \
                    not dest_square.get_occupying_piece().get_moved_yet_status():
                # We are good to go ahead and make the queen-side castle
                king_dest_square = board.get_game_square(7, 2)
                rook_dest_square = board.get_game_square(7, 3)

                # These destination squares should be empty, but let's check
                if king_dest_square.get_occupying_piece() is None \
                        and rook_dest_square.get_occupying_piece() is None:
                    # We are good to go, execute the castle
                    king_dest_square.put_piece_here(origin_square.get_occupying_piece())
                    rook_dest_square.put_piece_here(dest_square.get_occupying_piece())
                    origin_square.remove_occupying_piece()
                    dest_square.remove_occupying_piece()
                    castle_move = True
                    rook_dest_square.get_occupying_piece().move()  # Update that our rook has moved
                else:
                    raise Exception("The castle move should not have been generated because there are pieces "
                                    "in the way, Queen-side error")

    elif origin_square.get_row() == 7 and origin_square.get_col() == 3 \
            and isinstance(origin_square.get_occupying_piece(), King) and player is game.get_dark_player():
        # The king was chosen, check to see if the destination squares were rooks

        # Check king-side
        if dest_square.get_row() == 7 and dest_square.get_col() == 0 \
                and isinstance(dest_square.get_occupying_piece(), Rook):
            # We have the right pieces, let's confirm that neither piece have moved yet
            if not origin_square.get_occupying_piece().get_moved_yet_status() \
                    and not dest_square.get_occupying_piece().get_moved_yet_status():
                # We are good to go ahead and make the king-side castle
                king_dest_square = board.get_game_square(7, 1)
                rook_dest_square = board.get_game_square(7, 2)

                # These destination squares should be empty, but let's check
                if king_dest_square.get_occupying_piece() is None \
                        and rook_dest_square.get_occupying_piece() is None:
                    # We are good to go, execute the castle
                    king_dest_square.put_piece_here(origin_square.get_occupying_piece())
                    rook_dest_square.put_piece_here(dest_square.get_occupying_piece())
                    origin_square.remove_occupying_piece()
                    dest_square.remove_occupying_piece()
                    castle_move = True
                    rook_dest_square.get_occupying_piece().move()  # Update that our rook has moved
                else:
                    raise Exception("The castle move should not have been generated because there are pieces "
                                    "in the way, King-side error")

        # Check queen-side
        if dest_square.get_row() == 7 and dest_square.get_col() == 7 and \
                isinstance(dest_square.get_occupying_piece(), Rook):
            # We have the right pieces, let's confirm that neither piece have moved yet
            if not origin_square.get_occupying_piece().get_moved_yet_status() and \
                    not dest_square.get_occupying_piece().get_moved_yet_status():
                # We are good to go ahead and make the queen-side castle
                king_dest_square = board.get_game_square(7, 5)
                rook_dest_square = board.get_game_square(7, 4)

                # These destination squares should be empty, but let's check
                if king_dest_square.get_occupying_piece() is None \
                        and rook_dest_square.get_occupying_piece() is None:
                    # We are good to go, execute the castle
                    king_dest_square.put_piece_here(origin_square.get_occupying_piece())
                    rook_dest_square.put_piece_here(dest_square.get_occupying_piece())
                    origin_square.remove_occupying_piece()
                    dest_square.remove_occupying_piece()
                    castle_move = True
                    rook_dest_square.get_occupying_piece.move()  # Update that our rook has moved
                else:
                    raise Exception("The castle move should not have been generated because there are pieces "
                                    "in the way, Queen-side error")
    if not castle_move:

        # Then check for en passant move
        if origin_square.get_row() == 3 and isinstance(origin_square.get_occupying_piece(), Pawn):
            # square where enemy pawn made 2 step move last turn
            adj_square = board.get_game_square(origin_square.get_row(), dest_square.get_col())
            # make sure enemy at adjacent
            if adj_square.get_occupying_piece() is not None:
                if adj_square.get_occupying_piece().get_colour() != \
                        origin_square.get_occupying_piece().get_colour():
                    # capture adj enemy and move diagonaly behind the enemy pawn
                    if not other_player_piece_set.capture_piece(adj_square.get_occupying_piece()):
                        raise Exception("Unable to capture piece via En passant")
                    adj_square.remove_occupying_piece()
                    dest_square.put_piece_here(origin_square.get_occupying_piece())
                    origin_square.remove_occupying_piece()

        elif dest_square.get_occupying_piece() is None:
            # We can go ahead and make the move
            dest_square.put_piece_here(origin_square.get_occupying_piece())
            origin_square.remove_occupying_piece()
        elif dest_square.get_occupying_piece().get_colour() != origin_square.get_occupying_piece().get_colour():
            # Enemy piece there, make the capture move
            if not other_player_piece_set.capture_piece(dest_square.get_occupying_piece()):
                raise Exception("Unable to capture piece.")
            dest_square.remove_occupying_piece()
            dest_square.put_piece_here(origin_square.get_occupying_piece())
            origin_square.remove_occupying_piece()
        else:
            # Illegal move, trying to move a square that has a friendly piece
            raise Exception("Illegal move, trying to move a square that has a friendly piece")

    player.set_last_move(((7 - origin_square.get_row(), 7 - origin_square.get_col()),
                          (7 - dest_square.get_row(), 7 - dest_square.get_col())))

    # Update that the piece has moved, this will prevent special moves from being generated when not appropriate.
    piece_moved = dest_square.get_occupying_piece()
    if isinstance(piece_moved, King) or isinstance(piece_moved, Rook) or isinstance(piece_moved, Pawn):
        piece_moved.move()
