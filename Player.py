# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from PieceSet import PieceSet
from build_list_of_moves import build_list_of_moves
from GameType import GameType
from checkers_move_maker import checkers_move_maker
from chess_move_maker import chess_move_maker


class Player(object):
    """
    The player represents a game player, every game has two players.  The players use helper functions to build the
    list of possible moves and then make the move.

    Attributes:
        __piece_set: PieceSet: The players piece set
        __name: String: The players name
        __player_type: PlayerType.AI or PlayerType.HUMAN, whether the player is a human or computer engine
        __timer: Timer: The players timer object
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

    def build_possible_moves_for_all_pieces(self, game):
        """
        Generates and returns all possible moves for all current player's pieces on the board.
        :param: game: The current game, need to get the player and board.
        :return: 2D List of GameSquares for all the current player's pieces.
                first element is origin square
        """
        game_squares_movable_to = []

        # Look thorough the whole board and look for this players pieces
        for row in range(game.get_board().get_size()):
            for col in range(game.get_board().get_size()):
                square_here = game.get_board().get_game_square(row, col)
                if (square_here.get_occupying_piece() is not None) and \
                        (square_here.get_occupying_piece().get_colour() == self.get_piece_set().get_colour()):
                    # Then this is one of the current players pieces and we need to compute a list of moves for it
                    list_of_moves_for_this_square = build_list_of_moves(square_here, game)
                    if len(list_of_moves_for_this_square) > 0:
                        for dest_square in list_of_moves_for_this_square:
                            game_squares_movable_to.append([square_here, dest_square])

        print("The AI has " + str(len(game_squares_movable_to)) + " moves available to it.")
        return game_squares_movable_to

    def make_move(self, origin_square, dest_square, game):
        """
        Actually executes a move (and capture) also registers what the player last move was
        Precondition: Assuming that dest_square is a legal move for the origin_square
        :param origin_square: GameSquare: Where we are moving from
        :param dest_square: GameSquare: Where we are moving to
        :param game: Game: Needed to look at the squares we are jumping to for checkers and for castling in chess
        """
        if type(origin_square).__name__ != "GameSquare":

            raise Exception("The origin square passed to make_move() is not a Game Square object." +
                            type(origin_square).__name__)

        if type(dest_square).__name__ != "GameSquare":
            raise Exception("The destination square passed to make_move() is not a Game Square object.")

        if type(game).__name__ != "Game":
            raise Exception("The game square passed to make_move() is not a Game Square object.")

        board = game.get_board()
        if self is game.get_light_player():
            other_player = game.get_dark_player()
        else:
            other_player = game.get_light_player()

        if origin_square.get_occupying_piece() is None:
            # There is no piece here, raise an exception
            raise Exception("There is not piece on the origin square")

        if self.__piece_set.get_piece_set_type() == GameType.CHECKERS:
            checkers_move_maker(origin_square, dest_square,
                                board, other_player.get_piece_set())

        elif self.__piece_set.get_piece_set_type() == GameType.CHESS:
            chess_move_maker(origin_square, dest_square, board,
                             other_player.get_piece_set(), self, game)

        else:
            # Couldn't identify the type of game
            raise Exception(
                "The player's piece set is neither of type checkers or type chess")

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
        return self.__player_type

    def get_timer(self):
        """ :return: Timer object of a Player """
        return self.__timer

    def get_last_move(self):
        """ :return: Tuple of 2 Tuples of 2 Integer, ((origin row, origin col), (dest row, dest col)) """
        return self.__last_move

    def set_last_move(self, last_move):
        """ :param last_move: The player's last move, ((origin row, origin col), (dest row, dest col)) """
        self.__last_move = last_move
