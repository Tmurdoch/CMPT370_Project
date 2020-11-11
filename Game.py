import Colours
from PlayerType import PlayerType
from Player import Player
from Board import Board
import pytest
from PieceSet import PieceSet
from Pieces import King, Queen, Knight, Bishop, Rook, Pawn, CheckersCoin
from Move import CheckersMove, ChessMove
from PossibleMoves import PossibleMoves
from Timer import Timer
import struct

MAGIC = b"cmpt370checkerschess"
CURRENT_FILE_VERSION = 0
FILENAME = "test_save.bin"

# assuming 8 bits/timer and 2 timers
# TODO verify these assumptions
FILE_VER_ZERO_HEADER_SIZE = 31
GAME_TYPE_CHESS = 0
GAME_TYPE_CHECKERS = 1
GAME_TYPE_STRING_LOOK_UP_TABLE = ["Chess","Checkers"]
# make the c-stdlib style deffinitions so
# the code is readable and not full
# of magic numbers
SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2


class Game:

    def __init__(self, game_type, colour_mode):
        
        # I think based on PieceSet.py and the domain model
        # that this is going to be a string but i'm not
        # sure
        if (game_type.lower() == "chess"):
            self.__game_type = GAME_TYPE_CHESS
        elif (game_type.lower() == "checkers"):
            self.__game_type = GAME_TYPE_CHECKERS
        else:
            # something went wrong here and it wasn't the users fault
            # so don't show an error, whatever tried to create a game
            # object will probably crash now
            raise GameTypeErrorOrSomethingFigureOutHowPeopleWantThisTOWOrk
        # common for both chess and checkers
        if ((colour_mode) >= len(Colours.COLOUR_STRING_LOOK_UP_TABLE)):
            raise wrongColourOrSomethingFigurOutLAter
        self.__colour_mode = colour_mode
        self.__board = Board(8)
        return

    def get_light_player(self):
        """Return the light player object"""
        return self.__light_player

    def build_light_player(self,name,player_type,timer,castled):
        self.__light_player = Player(name,player_type,timer,castled)
        self.__light_player.set_piece_set(
            PieceSet(GAME_TYPE_STRING_LOOK_UP_TABLE[self.__game_type],
                     Colours.COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode]
                     [Colours.Colour_Offset.OFFSET_LIGHT]))
        return

    def build_dark_player(self,name,player_type,timer,castled):
        self.__dark_player = Player(name,player_type,timer,castled)
        self.__light_player.set_piece_set(
            PieceSet(GAME_TYPE_STRING_LOOK_UP_TABLE[self.__game_type],
                     Colours.COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode]
                     [Colours.Colour_Offset.OFFSET_DARK]))
        return

    def get_dark_player(self):
        """Return the dark player object"""
        return self.__dark_player

    def start(self):
        return

    def abort(self):
        return

    def get_board(self):
        """Return the board object"""
        return self.__board

    def get_current_player(self):
        return

    def save_to_file(self):
        """Save the current game state to a file"""
        """TODO: The file location is unknown at this time"""
        """expected *nix = ~/.cmpt370checkerschess/savegame.370checkerschess"""
        """expected windows = ????"""
        """Returns None"""
        # caller of save_to_file()
        # is responsible for the try except
        # error handling
        fp = open(FILENAME, "wb")
        # write magic
        fp.write(MAGIC)
        # TODO ensure this decoding works
        # since this may be implemented using
        # different methods
        game_mode = self.__game_type  # good
        ai_in_game = 0 # TODO
        dark_player_is_ai = not (self.__dark_player.get_player_type())  # good
        dark_player_turn = 1  # TODO
        board_height = self.get_board().get_size()  # good
        board_width = board_height  # good
        colours = self.__colour_mode  # good
        # TODO decode timer_mode
        timer_mode = 0
        # write the header struct
        # with the exception of the timer data
        # TODO figure out how timer works
        # /what it does
        fp.write(struct.pack(">BBBBBBBB", CURRENT_FILE_VERSION, game_mode,
                             dark_player_is_ai, dark_player_turn, board_height,
                             board_width, colours, timer_mode))
        # data = struct.pack(">BBBBBBBBBII", VERSION, game_mode,
        # player_b_is_ai, player_b_is_dark, player_a_turn, board_height,
        # board_width, colours, timer_mode, player_a_timer, player_b_time)
        # work on board
        row = 0

        while (row != board_height):
            col = 0
            while (col != board_width):
                cur_piece = self.__board.get_game_square(row,col).get_occupying_piece()
                if (cur_piece is None):
                    fp.write((0).to_bytes(1, byteorder="big"))
                    col +=1
                    continue
                # check if it is dark and set the dark bit
                if (cur_piece.get_colour() == Colours.COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][Colours.Colour_Offset.OFFSET_DARK]):
                    output_piece = 0b100000
                else:
                    output_piece = 0
                # decode object to char
                if (self.__game_type == GAME_TYPE_CHESS):
                    if (isinstance(cur_piece, King)):
                        output_piece += ord("K")
                    elif (isinstance(cur_piece, Queen)):
                        output_piece += ord("Q")
                    elif (isinstance(cur_piece, Knight)):
                        output_piece += ord("N")
                    elif (isinstance(cur_piece, Bishop)):
                        output_piece += ord("B")
                    elif (isinstance(cur_piece, Rook)):
                        output_piece += ord("R")
                    elif (isinstance(cur_piece, Pawn)):
                        output_piece += ord("P")
                    else:
                        # oh no
                        fp.close()
                        assert(0)
                elif (self.__game_type == GAME_TYPE_CHECKERS):
                    output_piece += (1 + cur_piece.get_promotion_status())
                else:
                    # oh no
                    fp.close()
                    assert(0)
                # write data
                fp.write(output_piece.to_bytes(1, byteorder="big"))
                print(row, col)
                col += 1
            row += 1
        fp.close()

    def load_from_file(self):
        """Load game state from file"""
        """This is expected to be called from the ui object"""
        """Which has already checked for the existance of the save game"""
        """Return None"""
        # caller of load_from_file()
        # is responsible for the try except
        # error handling
        fp = open(FILENAME, "rb")
        read_magic = fp.read(20)
        if (read_magic != MAGIC):
            raise ChessFileErrorOrSomethingFigureOutHowPeopleWantThisTOWOrk
        file_version = int.from_bytes(fp.read(1),
                                      byteorder="big", signed=False)
        if (file_version == 0):
            # Do stuff for file version 0
            # if the file version changes
            # add an "elif" after this
            # with the new code
            fp.seek(0, SEEK_END)
            file_size = fp.tell()
            fp.seek(0, SEEK_SET)
            if (file_size < FILE_VER_ZERO_HEADER_SIZE):
                fp.close()
                raise ChessFileErrorOrSomethingFigureOutHowPeopleWantThisTOWOrk
            if (self.__game_type != int.from_bytes(fp.read(1),
                                                  byteorder=big,
                                                  signed=False)):
                # TODO user not at fault
                # somebody set us up the bomb
                # the game object was created with a different type than the
                # file trying to be loaded
                # my lord is that legal?
                raise someExceptionIDK
            ai_in_game = int.from_bytes(fp.read(1), byteorder=big,
                                               signed=False)
            dark_player_is_ai = int.from_bytes(fp.read(1), byteorder=big,
                                               signed=False)
            dark_player_turn = int.from_bytes(fp.read(1), byteorder=big,
                                              signed=False)
            # setup game object turn state here
            board_height = int.from_bytes(fp.read(1), byteorder=big,
                                          signed=False)
            board_width = int.from_bytes(fp.read(1), byteorder=big,
                                         signed=False)
            if (board_height != board_width):
                # should work according to domain model
                # but won't work as built
                fp.close()
                raise BoardWrongOrSomethingIDK
            self.__board = Board(board_height)
            self.__colour_mode = int.from_bytes(fp.read(1), byteorder=big, signed=False)
            self.build_light_player("NotUsedInThisVersionOfSaves", (not (ai_in_game and (not dark_player_is_ai))),
                                    timer_stuf, light_player_castled)
            self.build_dark_player("NotUsedInThisVersionOfSaves", (not (ai_in_game and (dark_player_is_ai))),
                                    timer_stuf, light_player_castled)
            timer_mode = int.from_bytes(fp.read(1), byteorder=big,
                                        signed=False)
            # TODO figure out how timer works
        else:
            fp.close()
            ui.showError("File version " + str(file_version) +
                         " unsupported in this version, update the game")
            raise ChessFileErrorOrSomethingFigureOutHowPeopleWantThisTOWOrk

    def get_result(self):
        return

    def declare_result(self):
        return

    def build_result(self):
        return

    def show_instructions(self):
        """This might be part of UI?"""
        return

    def get_game_type(self):
        return

    def set_game_type(self, game_type):
        """this might be part of init() cant think of when you would"""
        """need to change game partway through"""
        """I expect UI would just dump this game object and make a new one"""
        return

    def change_current_player(self):
        return

    def check_for_game_over(self):
        return


if (__name__ == "__main__"):
	"""
    uio = UI()
    uio.doStuff()
    print("done")
	"""
	game_obj = Game("chess", Colours.Colour_Codes.RED_BLACK)

	piece_obj = King("Red")	

	game_obj.get_board().get_game_square(0, 0).put_piece_here(piece_obj)
	game_obj.get_board().print_game_board()
	timer_obj = Timer(10, 20, 0) 
	game_obj.build_light_player("tom", PlayerType.human, timer_obj, 1)
	game_obj.build_dark_player("tom", PlayerType.human, timer_obj, 1)
	game_obj.save_to_file()

