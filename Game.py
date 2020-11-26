# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from Colours import ColourOffset, COLOUR_STRING_LOOK_UP_TABLE
from Player import Player
from Board import Board
from Pieces import King, Queen, Knight, Bishop, Rook, Pawn
from Timer import Timer
from GameStatus import GameStatus
import struct
import os

MAGIC = b"cmpt370checkerschess"
CURRENT_FILE_VERSION = 0
FILENAME = "test_save.bin"
FILE_VER_ZERO_HEADER_SIZE = 39
GAME_TYPE_STRING_LOOK_UP_TABLE = ["Chess", "Checkers"]
# make the c-stdlib style definitions so
# the code is readable and not full
# of magic numbers
SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2


class Game:
    """
    The game object is relates the players and the board together.
    The game has two players and one board.  The game can save itself to or load itself in from file.

    Attributes:
        __game_type: int: GameType enum
        __colour_mode: A ColourCodes enum that encodes the players colours
        __light_player: Player: The light player object
        __dark_player: Player: The dark player object
        __board: Board: The game board
        __game_status: GameStatus: The current status of the game
    """

    def __init__(self, game_type, colour_mode):
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
        self.__board = Board(8)  # TODO: Should this board size be hard coded?
        return

    def get_light_player(self):
        """:return: Player: The light player object"""
        return self.__light_player

    def get_dark_player(self):
        """:return: Player: The dark player object"""
        return self.__dark_player

    def build_light_player(self, name, player_type, timer):
        """
        Build the light coloured object.
        :param name: string: Player name
        :param player_type: int: The type of PlayerType enum of what type of player they ar
        :param timer: Timer: The player's timer object
        """
        self.__light_player = Player(name, COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][ColourOffset.OFFSET_LIGHT],
                                     self.__game_type, player_type, timer)
        self.__current_player = self.__light_player  # Light colour goes first

    def build_dark_player(self, name, player_type, timer):
        """
        Build the light coloured object.
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
        Save the current game state to a file
        path: string describing file path to save too
        :return: None
        """
        # caller of save_to_file()
        # is responsible for the try except
        # error handling
        fp = open(path+"/save-game.370"+GAME_TYPE_STRING_LOOK_UP_TABLE[self.__game_type], "wb")
        # write magic
        fp.write(MAGIC)
        game_mode = self.__game_type  # TODO: Isn't this a string? "chess" or "checkers"
        ai_in_game = not ((self.__light_player.get_player_type()) and (
            self.__dark_player.get_player_type()))  # good
        dark_player_is_ai = not (self.__dark_player.get_player_type())  # good
        dark_player_turn = self.__dark_player is self.__current_player  # good
        board_height = self.get_board().get_size()  # good
        board_width = board_height  # good
        colours = self.__colour_mode  # good
        timer_enabled = self.__dark_player.get_timer().get_enabled()  # good
        light_player_time = self.__light_player.get_timer().get_time_remaining_s()  # good
        dark_player_time = self.__dark_player.get_timer().get_time_remaining_s()  # good
        light_player_castled = self.__light_player.get_castled()
        dark_player_castled = self.__dark_player.get_castled()
        # write the header struct
        fp.write(struct.pack(">BBBBBBBBBBBff", CURRENT_FILE_VERSION, game_mode,
                             ai_in_game, dark_player_is_ai, dark_player_turn,
                             board_height, board_width, colours, timer_enabled,
                             light_player_castled, dark_player_castled,
                             light_player_time, dark_player_time))
        row = 0
        while row != board_height:
            col = 0
            while col != board_width:
                cur_piece = self.__board.get_game_square(
                    row, col).get_occupying_piece()
                if cur_piece is None:
                    fp.write((0).to_bytes(1, byteorder="big"))
                    col += 1
                    continue
                # check if it is dark and set the dark bit
                if cur_piece.get_colour() == COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][ColourOffset.OFFSET_DARK]:
                    output_piece = 0b100000
                else:
                    output_piece = 0
                # decode object to char
                if self.__game_type == GameType.CHESS:
                    if isinstance(cur_piece, King):
                        output_piece += ord("K")
                    elif isinstance(cur_piece, Queen):
                        output_piece += ord("Q")
                    elif isinstance(cur_piece, Knight):
                        output_piece += ord("N")
                    elif isinstance(cur_piece, Bishop):
                        output_piece += ord("B")
                    elif isinstance(cur_piece, Rook):
                        output_piece += ord("R")
                    elif isinstance(cur_piece, Pawn):
                        if cur_piece.get_moved_yet_status():
                            # The pawn is a moved pawn
                            output_piece += ord("M")
                        else:
                            # The pawn is an unmoved pawn
                            output_piece += ord("P")
                    else:
                        # unidentified piece, shouldn't be possible
                        fp.close()
                        assert 0
                elif self.__game_type == GameType.CHECKERS:
                    output_piece += (1 + cur_piece.get_promotion_status())
                else:
                    # unidentified game, shouldn't be possible
                    fp.close()
                    assert 0
                # write data
                fp.write(output_piece.to_bytes(1, byteorder="big"))
                col += 1
            row += 1
        fp.close()

    def load_from_file(self, path):
        """
        Load game state from file
        This is expected to be called from the ui object
        Which has already checked for the existence of the save game
        DELETES THE FILE IF IT IS SUCCESSFULLY LOADED AS DISCUSSED
        AT SOME POINT IN OUR MEETINGS
        path: string describing file path to save too
        :return: None
        # TODO: Reconstruct piece set from the file
        """
        # caller of load_from_file()
        # is responsible for the try except
        # error handling
        fp = open(path+"/save-game.370"+GAME_TYPE_STRING_LOOK_UP_TABLE[self.__game_type], "rb")
        read_magic = fp.read(20)
        if read_magic != MAGIC:
            raise Exception(
                "ChessFileErrorOrSomethingFigureOutHowPeopleWantThisTOWOrk")

        file_version = int.from_bytes(
            fp.read(1), byteorder="big", signed=False)
        if file_version == 0:
            # Do stuff for file version 0
            # if the file version changes
            # add an "elif" after this
            # with the new code
            fp.seek(0, SEEK_END)
            file_size = fp.tell()
            fp.seek(0, SEEK_SET)
            # check if file is at least big enough to hold the header
            if file_size < FILE_VER_ZERO_HEADER_SIZE:
                fp.close()
                raise Exception(
                    "ChessFileErrorOrSomethingFigureOutHowPeopleWantThisTOWOrk")
            fp.seek(20, SEEK_SET)
            f = fp.read(FILE_VER_ZERO_HEADER_SIZE-20)
            CURRENT_FILE_VERSION, game_mode, ai_in_game, dark_player_is_ai, dark_player_turn, board_height, \
                board_width, colours, timer_enabled, light_player_castled, dark_player_castled, light_player_time, \
                dark_player_time = struct.unpack(">BBBBBBBBBBBff", f)

            if file_size < (FILE_VER_ZERO_HEADER_SIZE + (board_width * board_height)):
                # file too small
                fp.close()
                raise Exception("something")
            board_data = fp.read(board_height*board_width)
            fp.close()

            if self.__game_type != game_mode:
                # somebody set us up the bomb
                # the game object was created with a different type than the
                # file trying to be loaded
                # my lord is that legal?
                raise Exception("someExceptionIDK")

            if board_height != board_width:
                # should work according to domain model
                # but won't work as built
                fp.close()
                raise Exception("BoardWrongOrSomethingIDK")

            self.__board = Board(board_height)
            self.__colour_mode = colours

            self.build_light_player("NotUsedInThisVersionOfSaves",
                                    (not (ai_in_game and (not dark_player_is_ai))),
                                    Timer(light_player_time, timer_enabled))

            if light_player_castled:
                self.__light_player.castle()

            self.build_dark_player("NotUsedInThisVersionOfSaves",
                                   (not (ai_in_game and dark_player_is_ai)),
                                   Timer(dark_player_time, timer_enabled))
            if dark_player_castled:
                self.__dark_player.castle()

            # For now assume they are ideal piece sets
            self.__light_player.build_piece_set(
                GAME_TYPE_STRING_LOOK_UP_TABLE[game_mode], COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][0])
            self.__dark_player.build_piece_set(
                GAME_TYPE_STRING_LOOK_UP_TABLE[game_mode], COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][1])
            # TODO: Right now we are just putting random chess pieces on the board, we need to put on pieces from the
            #  pieceset onto the board and then capture all the pieces that we didn't find on the board

            # setup board here
            board_data_index = 0
            found_dark_checkers_pieces = 0
            found_light_checkers_pieces = 0
            row = 0
            while row != board_height:
                col = 0
                while col != board_width:
                    cur_square = self.__board.get_game_square(row, col)
                    if board_data[board_data_index] == 0:
                        cur_square.put_piece_here(None)
                        board_data_index += 1
                        col += 1
                        continue

                    # If we get here we are looking at a non-empty board square
                    # check if it is dark and set the dark bit
                    if board_data[board_data_index] & 0b100000:
                        is_dark = 1
                    else:
                        is_dark = 0

                    # decode object to char
                    if self.__game_type == GameType.CHESS:
                        if chr(board_data[board_data_index]).lower() == "k":
                            cur_square.put_piece_here(
                                King(COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][is_dark]))
                        elif chr(board_data[board_data_index]).lower() == "q":
                            cur_square.put_piece_here(
                                Queen(COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][is_dark]))
                        elif chr(board_data[board_data_index]).lower() == "n":
                            cur_square.put_piece_here(
                                Knight(COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][is_dark]))
                        elif chr(board_data[board_data_index]).lower() == "b":
                            cur_square.put_piece_here(
                                Bishop(COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][is_dark]))
                        elif chr(board_data[board_data_index]).lower() == "r":
                            cur_square.put_piece_here(
                                Rook(COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][is_dark]))
                        elif chr(board_data[board_data_index]).lower() == "p":
                            # The pawn is an unmoved pawn
                            cur_square.put_piece_here(
                                Pawn(COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][is_dark]))
                        elif chr(board_data[board_data_index]).lower() == "m":
                            # The pawn is an moved pawn
                            cur_square.put_piece_here(
                                Pawn(COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][is_dark]))
                            cur_square.get_occupying_piece().move()
                        else:
                            # unidentified piece, shouldn't be possible
                            assert 0

                    elif self.__game_type == GameType.CHECKERS:
                        if is_dark:
                            cur_square.put_piece_here(
                                self.__dark_player.get_piece_set().get_live_pieces()[
                                    found_dark_checkers_pieces]
                            )
                            found_dark_checkers_pieces += 1
                        else:
                            cur_square.put_piece_here(
                                self.__light_player.get_piece_set().get_live_pieces()[
                                    found_light_checkers_pieces]
                            )
                            found_light_checkers_pieces += 1

                        if board_data[board_data_index] & 0b10:
                            cur_square.get_occupying_piece().promote()
                    else:
                        # unidentified game, shouldn't be possible
                        assert 0
                    board_data_index += 1
                    col += 1
                row += 1

            # put all the pieces that were not placed on the board into the captured lists
            if self.__game_type == GameType.CHECKERS:
                # Start at the back of the list of live pieces not placed on the board and capture them
                for i in range(16-found_dark_checkers_pieces):
                    self.__dark_player.get_piece_set().capture_piece(
                        self.__dark_player.get_piece_set().get_live_pieces()[
                            15-i]
                    )
            elif self.__game_type == GameType.CHESS:
                pass
            # delete the file after loading
            os.remove(path+"/save-game.370"+GAME_TYPE_STRING_LOOK_UP_TABLE[self.__game_type])
            return

        else:
            fp.close()
            # ui.showError("File version " + str(file_version) + " unsupported in this version, update the game")
            raise Exception(
                "ChessFileErrorOrSomethingFigureOutHowPeopleWantThisTOWOrk")

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
        if self.__game_type == GameType.CHECKERS:
            if 0 == len(self.__current_player.build_possible_moves_for_all_pieces(self)):
                if self.__current_player is self.__light_player:
                    self.__game_status = GameStatus.DARK_VICTORIOUS
                else:
                    self.__game_status = GameStatus.LIGHT_VICTORIOUS
        elif self.__game_type == GameType.CHESS:
            # TODO CHESS
            print("do stuff")
        else:
            # unknown game
            assert 0
        return

    def check_for_game_over(self):
        """
        Checks to see if the game is over
        :return: Bool: if the game is over"""
        return bool(self.__game_status)

    def get_colour_mode(self):
        """
        Get the colour mode enum for the current game
        :return: IntEnum of the current player colour
        """
        return self.__colour_mode


# if (__name__ == "__main__"):
#    game_obj = Game("chess", Colours.Colour_Codes.RED_BLACK)
#
#    piece_obj = King("Red")
#
#    game_obj.get_board().get_game_square(0, 0).put_piece_here(self.__dark_player.get_piece_set().)
#    game_obj.get_board().print_game_board()
#    timer_obj = Timer(10, 20, 0)
#    game_obj.build_light_player("tom", PlayerType.human, timer_obj, 1)
#    game_obj.build_dark_player("tom", PlayerType.human, timer_obj, 1)
#    game_obj.save_to_file()
