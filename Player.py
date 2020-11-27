# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from PieceSet import PieceSet
from Pieces import King, Rook
from build_list_of_moves import build_list_of_moves
from GameType import GameType


class Player(object):
    """
    The player represents a game player, every game has two players.  The players use helper functions to build the
    list of possible moves and then make the move.

    Attributes:
        __piece_set: PieceSet: The players piece set
        __name: String: The players name
        __player_type: PlayerType.AI or PlayerType.HUMAN, whether the player is a human or computer engine
        __timer: Timer: The players timer object
        __castled: Bool: Whether or not the player has castled
        __last_move: Tuple of Tuples of Integer: ((origin row, origin col), (dest row, dest col)). This is only 
                    used for the en passant move in chess. This is not used in checkers
    """

    def __init__(self, name, colour, game_type, player_type, timer):
        """
        Initializes a Player object.
        :param name: string: The name of a Player.
        :param colour: string: Player colour as a string.
        :param game_type: GameType:
        :param: player_type: PlayerType: The type of Player the Player is PlayerType.AI or PlayerType.HUMAN
        :param timer: Timer: The Timer object for a Player
        """
        self.__piece_set = PieceSet(game_type, colour)
        self.__name = name
        self.__player_type = player_type
        self.__timer = timer
        self.__castled = False
        self.__last_move = None

    @staticmethod
    def build_possible_moves_for_single_square(game_square, game):
        """
        Generates and returns a list of possible moves for a single game square.
        :param: GameSquare: For getting game square to build list of moves for
        :param: Game: For getting player and board.
        :return: List of GameSquares for a single square.
        """
        return build_list_of_moves(game_square, game)

    @staticmethod
    def build_possible_moves_for_all_pieces(game):
        """
        Generates and returns all possible moves for all current player's pieces on the board.
        :param: Game: The current game, need to get the player and board.
        :return: List of GameSquares for all the current player's pieces.
        """
        game_squares_movable_to = []
        for row in range(game.get_board().get_size()):
            for col in range(game.get_board().get_size()):
                square_here = game.get_board().get_game_square(row, col)
                if (square_here.get_occupying_piece() is not None) and (square_here.get_occupying_piece().get_colour()):
                    game_squares_movable_to.append(
                        build_list_of_moves(square_here, game))
        return game_squares_movable_to

    def make_move(self, origin_square, dest_square, game):
        """
        Actually executes a move (and capture) also registers what the player last move was
        Precondition: Assuming that dest_square is a legal move for the origin_square
        :param origin_square: GameSquare: Where we are moving from
        :param dest_square: GameSquare: Where we are moving to
        :param game: Game: Needed to look at the squares we are jumping to for checkers and for castling in chess
        """
        board = game.get_board()
        if self is game.get_light_player():
            other_player = game.get_dark_player()
        else:
            other_player = game.get_light_player()

        if origin_square.get_occupying_piece() is None:
            # There is no piece here, raise an exception
            raise Exception("There is not piece on this square")

        if self.__piece_set.get_piece_set_type() == GameType.CHECKERS:
            if dest_square.get_occupying_piece() is not None:
                # This move shouldn't have been generated
                raise Exception(
                    "Illegal move, this move shouldn't have been generated")
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
                            dest_square.put_piece_here(
                                origin_square.get_occupying_piece())
                            origin_square.remove_occupying_piece()

                            print(square_of_capture.get_occupying_piece())
                            print("")
                            print(other_player.get_piece_set().get_live_pieces())

                            if not other_player.get_piece_set().capture_piece(square_of_capture.get_occupying_piece()):
                                raise Exception("Unable to capture piece")
                            square_of_capture.remove_occupying_piece()
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
                            dest_square.put_piece_here(
                                origin_square.get_occupying_piece())
                            origin_square.remove_occupying_piece()
                            if not other_player.get_piece_set().capture_piece(square_of_capture.get_occupying_piece()):
                                raise Exception("Unable to capture piece")
                            square_of_capture.remove_occupying_piece()
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
                            dest_square.put_piece_here(
                                origin_square.get_occupying_piece())
                            origin_square.remove_occupying_piece()
                            if not other_player.get_piece_set().capture_piece(square_of_capture.get_occupying_piece()):
                                raise Exception("Unable to capture piece")
                            square_of_capture.remove_occupying_piece()
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
                            dest_square.put_piece_here(
                                origin_square.get_occupying_piece())
                            origin_square.remove_occupying_piece()
                            if not other_player.get_piece_set().capture_piece(square_of_capture.get_occupying_piece()):
                                raise Exception("Unable to capture piece")
                            square_of_capture.remove_occupying_piece()
                        else:
                            # You are trying to jump your own piece
                            raise Exception("You are trying to jump your own piece, trying to jump bottom "
                                            "right hand corner piece")
                else:
                    # There are more than one jumps needing to take place
                    raise Exception(
                        "Cannot handle more than one jump right now")

            # If the checkers coin has reached the far side of the board (and is not yet promoted) then promote
            if dest_square.get_row() == 0 and not origin_square.get_occupying_piece().is_promoted():
                origin_square.get_occupying_piece().promote()

        elif self.__piece_set.get_piece_set_type() == GameType.CHESS:

            # First check if the move is a castle
            if origin_square.get_row() == 7 and origin_square.get_col() == 4 \
                    and isinstance(origin_square.get_occupying_piece(), King):
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
                            king_dest_square.put_piece_here(
                                origin_square.get_occupying_piece())
                            rook_dest_square.put_piece_here(
                                dest_square.get_occupying_piece())
                            origin_square.remove_occupying_piece()
                            dest_square.remove_occupying_piece()
                            self.castle()
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
                        king_dest_square = board.get_game_square(7, 3)
                        rook_dest_square = board.get_game_square(7, 2)

                        # These destination squares should be empty, but let's check
                        if king_dest_square.get_occupying_piece() is None \
                                and rook_dest_square.get_occupying_piece() is None:
                            # We are good to go, execute the castle
                            king_dest_square.put_piece_here(
                                origin_square.get_occupying_piece())
                            rook_dest_square.put_piece_here(
                                dest_square.get_occupying_piece())
                            origin_square.remove_occupying_piece()
                            dest_square.remove_occupying_piece()
                            self.castle()
                        else:
                            raise Exception("The castle move should not have been generated because there are pieces "
                                            "in the way, Queen-side error")
                # register the castle move
                self.__last_move = ((7 - origin_square.get_row(), 7 - origin_square.get_col()),
                                    (7 - dest_square.get_row(), 7 - dest_square.get_col()))

            # Else it is just a normal move
            else:
                if dest_square.get_occupying_piece() is None:
                    # We can go ahead and make the move
                    dest_square.put_piece_here(
                        origin_square.get_occupying_piece())
                    origin_square.remove_occupying_piece()
                elif dest_square.get_occupying_piece().get_colour() != origin_square.get_occupying_piece().get_colour():
                    # Enemy piece there, make the capture move
                    if not other_player.__piece_set.capture_piece(dest_square.get_occupying_piece()):
                        raise Exception("Unable to capture piece.")
                    dest_square.remove_occupying_piece()
                    dest_square.put_piece_here(origin_square.get_occupying_piece())
                    origin_square.remove_occupying_piece()
                else:
                    # Illegal move, trying to move a square that has a friendly piece
                    raise Exception(
                        "Illegal move, trying to move a square that has a friendly piece")
                # Register this to be that last move
                self.__last_move = ((7 - origin_square.get_row(), 7 - origin_square.get_col()),
                                    (7 - dest_square.get_row(), 7 - dest_square.get_col()))

        else:
            # Couldn't identify the type of game
            raise Exception(
                "The players piece set is neither of type checkers or type chess")

    def get_piece_set(self):
        """ :return: PieceSet: The player's piece set """
        return self.__piece_set

    def get_colour(self):
        """ :return: the colour of the player """
        return self.__piece_set.get_colour()

    def get_name(self):
        """ :return: string: The player's name """
        return self.__name

    def get_player_type(self):
        """" :return: type of PlayerType object for a Player, AI(0) or Human(1) """
        return self.__player_type.value

    def get_timer(self):
        """ :return: Timer object of a Player """
        return self.__timer

    def get_castled(self):
        """ :return: Bool: True if the player has already castled, False otherwise """
        return self.__castled

    def castle(self):
        """
        Marks that the player has castled so we can make sure they don't castle again
        Can only be called in make_move() when executing the castle
        """
        self.__castled = True

    def get_last_move(self):
        """ :return: Tuple of 2 Tuples of 2 Integer, ((origin row, origin col), (dest row, dest col)) """
        return self.__last_move
