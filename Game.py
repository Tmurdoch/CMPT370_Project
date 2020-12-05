# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from Colours import ColourOffset, COLOUR_STRING_LOOK_UP_TABLE, COLOUR_BOARD_STRING_LOOK_UP_TABLE
from GameType import GameType
from Player import Player
from Board import Board
from GameStatus import GameStatus
from load_from_file import load_from_file
from save_to_file import save_to_file


class Game:
    """
    The game object is relates the players and the board together.
    The game has two players and one board.  The game can save itself to or load itself in from file.

    Attributes:
        __game_type: int: GameType enum
        __colour_mode: A ColourCodes enum that encodes the players colours
        __board_colour_mode: A ColourCodes enum that encodes the board colours
        __light_player: Player: The light player object
        __dark_player: Player: The dark player object
        __board: Board: The game board
        __game_status: GameStatus: The current status of the game
    """

    def __init__(self, game_type, colour_mode, board_colour_mode):
        """
        Initialize the game object, players are built later
        :param game_type: GameType: The type of game (chess or checkes)
        :param colour_mode: Colour: The game colour mode
        """
        self.__light_player = None  # Will be build later
        self.__dark_player = None  # Will be build later
        self.__current_player = None
        self.__game_status = GameStatus.IN_PROGRESS
        if game_type >= 2:
            # something went wrong here and it wasn't the users fault
            # so don't show an error, whatever tried to create a game
            # object will probably crash now
            raise Exception(
                "GameTypeErrorOrSomethingFigureOutHowPeopleWantThisTOWOrk")
        self.__game_type = game_type
        # common for both chess and checkers
        if colour_mode >= len(COLOUR_STRING_LOOK_UP_TABLE):
            raise Exception("wrongColourOrSomethingFigureOutLater")
        self.__colour_mode = colour_mode
        if board_colour_mode >= len(COLOUR_BOARD_STRING_LOOK_UP_TABLE):
            raise Exception("wrongColourOrSomethingFigureOutLater")
        self.__board_colour_mode = board_colour_mode
        # if board_colour_mode == colour_mode:
        #    #hard to see checkers pieces, perfect camoflage
        #    assert(0)
        self.__board = Board(8)  # TODO: Should this board size be hard coded?
        return

    def set_board(self, board):
        """ :param board: The game board, probably coming from file """
        self.__board = board

    def get_light_player(self):
        """:return: Player: The light player object"""
        return self.__light_player

    def get_dark_player(self):
        """:return: Player: The dark player object"""
        return self.__dark_player

    def build_light_player(self, name, player_type, timer):
        """
        Build the light coloured player object.
        :param name: string: Player name
        :param player_type: int: The type of PlayerType enum of what type of player they ar
        :param timer: Timer: The player's timer object
        """
        self.__light_player = Player(name, COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][ColourOffset.OFFSET_LIGHT],
                                     self.__game_type, player_type, timer)
        self.__current_player = self.__light_player  # Light colour goes first

    def build_dark_player(self, name, player_type, timer):
        """
        Build the dark coloured player object.
        :param name: string: Player name
        :param player_type: PlayerType: The type of Player the Player is, can be AI or Human
        :param timer: Timer: The player's timer object
        """
        self.__dark_player = Player(name, COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][ColourOffset.OFFSET_DARK],
                                    self.__game_type, player_type, timer)

    def get_board(self):
        """:return: the board object"""
        return self.__board

    def get_current_player(self):
        """:return: The current player """
        return self.__current_player

    def save_to_file(self, path):
        """
        Save the current game state to a file.
        Caller is responsible for try catch error handling.
        :param path: string: Describing file path to save too
        :return: None
        """
        save_to_file(self, path)

    def load_from_file(self, path):
        """
        Loads the current game in from file.
        Caller is responsible for try catch error handling.
        DELETES THE FILE IF IT IS SUCCESSFULLY LOADED.
        :param path: string: Describing file path to save too.
        :return: None
        """
        load_from_file(self, path)

    def get_result(self):
        # TODO: Not sure if this makes sense
        return self.__current_player

    def get_game_type(self):
        return self.__game_type

    def change_current_player(self):
        """Thought to be executed after a turn to switch to the other player"""
        if self.__current_player is self.__dark_player:
            self.__current_player = self.__light_player
        else:
            self.__current_player = self.__dark_player
        return

    def check_for_game_over(self):
        """
        Checks to see if the game is over
        :return: GameStatus: Current Game Status"""

        if self.__current_player is self.__light_player:
            light_player_moves = self.__light_player.build_possible_moves_for_all_pieces(self)
            self.get_board().switch_sides()
            dark_player_moves = self.__dark_player.build_possible_moves_for_all_pieces(self)
            self.get_board().switch_sides()
        else:
            dark_player_moves = self.__dark_player.build_possible_moves_for_all_pieces(self)
            self.get_board().switch_sides()
            light_player_moves = self.__light_player.build_possible_moves_for_all_pieces(self)
            self.get_board().switch_sides()

        if self.__game_type == GameType.CHECKERS:
            if len(light_player_moves) == 0:
                return GameStatus.DARK_VICTORIOUS
            elif len(dark_player_moves) == 0:
                return GameStatus.LIGHT_VICTORIOUS
            else:
                return GameStatus.IN_PROGRESS

        elif self.__game_type == GameType.CHESS:
            # TODO: Just checks for stalemate
            if len(light_player_moves) == 0:
                return GameStatus.DARK_VICTORIOUS
            elif len(dark_player_moves) == 0:
                return GameStatus.LIGHT_VICTORIOUS
            else:
                return GameStatus.IN_PROGRESS

        else:
            raise Exception("Can't check for game over, game is neither type chess nor checkers")

    def get_colour_mode(self):
        """
        Get the colour mode enum for the current game
        :return: IntEnum of the current player colour
        """
        return self.__colour_mode

    def set_colour_mode(self, colour_mode):
        """ :param colour_mode: The board colour mode. """
        self.__colour_mode = colour_mode

    def get_board_colour_mode(self):
        """
        Get the colour mode enum for the current game
        :return: IntEnum of the current player colour
        """
        return self.__board_colour_mode

    def set_board_colour_mode(self, board_colour_mode):
        """ :param board_colour_mode: The board colour mode. """
        self.__board_colour_mode = board_colour_mode
