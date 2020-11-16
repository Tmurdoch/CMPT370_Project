# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from PieceSet import PieceSet
from PossibleMoves import PossibleMoves


class Player(object):
    """
    A Player is an object that has a name, a colour and controls pieces inside a piece set by making moves
    to play a game of Chess or Checkers. ????

    Attributes:
        __piece_set: PieceSet: The players piece set
        __name: String: The players name
        __player_type: PlayerType.AI or PlayerType.HUMAN, whether the player is a human or computer engine
        __timer: Timer: The players timer object
        __castled: Bool: Whether or not the player has castled
    """

    def __init__(self, name, colour, game_type, player_type, timer):
        """
        Initializes a Player object.
        :param: string: name: The name of a Player.
        :param: PlayerType: player_type: The type of Player the Player is PlayerType.AI or PlayerType.HUMAN
        :param: Timer: timer: The Timer object for a Player
        :param: Boolean: castled: A boolean to see if the player has been castled or not.
        """
        self.__piece_set = PieceSet(game_type, colour)
        self.__name = name
        self.__player_type = player_type
        self.__timer = timer
        self.__castled = False

    def build_possible_moves_for_single_square(self, game_square, game):
        """
        Generates and returns a list of possible moves for a single game square.
        :param: GameSquare object, for getting game square to build list of moves for
        :param: Game object, for getting player and board
        :return: List of GameSquares for a single square
        """
        possible_moves_for_square_here = PossibleMoves(game_square, game)
        possible_moves_for_square_here.build_list_of_moves()
        return possible_moves_for_square_here.get_list_of_squares_you_can_move_to()

    def build_possible_moves_for_all_pieces(self, game):
        """Generates and returns all possible moves for all current player's pieces on the board.
            :param: Game object, for getting player and board
            :return: List of GameSquares for all the current player's pieces"""
        game_squares_movable_to = []
        for row in range(game.get_board().get_size()):
            for col in range(game.get_board().get_size()):
                square_here = game.get_board().get_game_square(row, col)
                if not (square_here.get_occupying_piece() is None and square_here.get_occupying_piece().get_colour()
                        == game.get_current_player().get_piece_set().get_colour()):
                    possible_moves_for_square_here = PossibleMoves(square_here, game)
                    possible_moves_for_square_here.build_list_of_moves()
                    game_squares_movable_to.append(possible_moves_for_square_here.get_list_of_squares_you_can_move_to())
        return game_squares_movable_to

    def make_move(self, origin_square, dest_square, board):
        """
        Actually executes a move (and capture)
        Precondition: Assuming that dest_square is a legal move for the origin_square
        :param: origin_square: GameSquare we are moving from
        :param: dest_square: GameSquare we are moving to
        :param: board: Board object, need to look at the squares we are jumping for checkers
        """
        if origin_square.get_occupying_piece() is None:
            # There is no piece here, raise an exception
            raise Exception("There is not piece on this square")

        if self.__piece_set.get_piece_set_type().lower() == "checkers":
            if dest_square.get_occupying_piece() is not None:
                # This move shouldn't have been generated
                raise Exception("Illegal move, this move shouldn't have been generated")
            else:
                if abs(origin_square.get_row() - dest_square().get_row()) == 1:
                    # Squares are immediately adjacent, no jumping
                    dest_square.put_piece_here(origin_square.get_occupying_piece())
                    origin_square.remove_occupying_piece()
                elif abs(origin_square.get_row() - dest_square().get_row()) == 2:
                    # Single jump

                    # Now, we also need to make the capture, need to find which of the four ways we moved
                    if ((origin_square.get_row() - dest_square().get_row()) > 0 and
                            (origin_square.get_col() - dest_square().get_col()) > 0):
                        # Piece we are trying to jump is in the immediate top left hand corner of the origin square
                        square_of_capture = board.get_game_square(origin_square.get_row() - 1,
                                                                  origin_square.get_col() - 1)
                        if (square_of_capture.get_occupying_piece().get_colour()
                                != origin_square.get_occupying_piece().get_colour()):
                            # The piece we are trying to jump is an enemy piece, go ahead and make the move
                            dest_square.put_piece_here(origin_square.get_occupying_piece())
                            origin_square.remove_occupying_piece()
                            square_of_capture.get_occupying_piece().capture()
                            square_of_capture.remove_occupying_piece()
                        else:
                            # You are trying to jump your own piece
                            raise Exception("You are trying to jump your own piece, trying to jump top left hand "
                                            "corner piece")

                    if ((origin_square.get_col() - dest_square().get_col())
                            < 0 < (origin_square.get_row() - dest_square().get_row())):
                        # Piece we are trying to jump is in the immediate top right hand corner of the origin square
                        square_of_capture = board.get_game_square(origin_square.get_row() - 1,
                                                                  origin_square.get_col() + 1)
                        if (square_of_capture.get_occupying_piece().get_colour()
                                != origin_square.get_occupying_piece().get_colour()):
                            # The piece we are trying to jump is an enemy piece, go ahead and make the move
                            dest_square.put_piece_here(origin_square.get_occupying_piece())
                            origin_square.remove_occupying_piece()
                            square_of_capture.get_occupying_piece().capture()
                            square_of_capture.remove_occupying_piece()
                        else:
                            # You are trying to jump your own piece
                            raise Exception("You are trying to jump your own piece, tyring to jump top right hand "
                                            "corner piece")

                    if ((origin_square.get_row() - dest_square().get_row())
                            < 0 < (origin_square.get_col() - dest_square().get_col())):
                        # Piece we are trying to jump is in the immediate bottom left hand corner of the origin
                        # square
                        square_of_capture = board.get_game_square(origin_square.get_row() + 1,
                                                                  origin_square.get_col() - 1)
                        if (square_of_capture.get_occupying_piece().get_colour()
                                != origin_square.get_occupying_piece().get_colour()):
                            # The piece we are trying to jump is an enemy piece, go ahead and make the move
                            dest_square.put_piece_here(origin_square.get_occupying_piece())
                            origin_square.remove_occupying_piece()
                            square_of_capture.get_occupying_piece().capture()
                            square_of_capture.remove_occupying_piece()
                        else:
                            # You are trying to jump your own piece
                            raise Exception("You are trying to jump your own piece, trying to jump bottom left "
                                            "hand corner piece")

                    if ((origin_square.get_row() - dest_square().get_row()) < 0 and
                            (origin_square.get_col() - dest_square().get_col()) < 0):
                        # Piece we are trying to jump is in the immediate bottom right hand corner of the origin
                        # square
                        square_of_capture = board.get_game_square(origin_square.get_row() + 1,
                                                                  origin_square.get_col() + 1)
                        if (square_of_capture.get_occupying_piece().get_colour()
                                != origin_square.get_occupying_piece().get_colour()):
                            # The piece we are trying to jump is an enemy piece, go ahead and make the move
                            dest_square.put_piece_here(origin_square.get_occupying_piece())
                            origin_square.remove_occupying_piece()
                            square_of_capture.get_occupying_piece().capture()
                            square_of_capture.remove_occupying_piece()
                        else:
                            # You are trying to jump your own piece
                            raise Exception("You are trying to jump your own piece, trying to jump bottom "
                                            "right hand corner piece")
                else:
                    # There are more than one jumps needing to take place
                    raise Exception("Cannot handle more than one jump right now")

        elif self.__piece_set.get_piece_set_type().lower() == "chess":
            if dest_square.get_occupying_piece() is None:
                # We can go ahead and make the move
                dest_square.put_piece_here(origin_square.get_occupying_piece())
                origin_square.remove_occupying_piece()
            elif dest_square.get_occupying_piece().get_colour() != origin_square.get_occupying_piece().get_colour():
                # Enemy piece there, make the capture move
                dest_square.get_occupying_piece().capture_piece()
                dest_square.put_piece_here(origin_square.get_occupying_piece())
                origin_square.remove_occupying_piece()
            else:
                # Illegal move, trying to move a square that has a friendly piece
                raise Exception("Illegal move, trying to move a square that has a friendly piece")
        else:
            # Couldn't identify the type of game
            raise Exception("Piece set is neither of type checkers or type chess")

    def get_piece_set(self):
        """:return: The players PieceSet"""
        return self.__piece_set

    def get_colour(self):
        """:return: the colour of the player"""
        return self.__piece_set.get_colour()

    def get_name(self):
        """:return: The players name"""
        return self.__name

    def get_player_type(self):
        """":return: type of PlayerType object for a Player, AI(0) or Human(1)"""
        return self.__player_type.value

    def get_timer(self):
        """:return: Timer object of a Player"""
        return self.__timer

    def get_castled(self):
        """:return: Bool, True if the player has already castled, False otherwise"""
        return self.__castled

    def castle(self):
        """Marks that the player has castled so we can make sure they don't castle again"""
        self.__castled = True
