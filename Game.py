import Colours
from PlayerType import PlayerType
from Player import Player
from Board import Board
#import pytest
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
FILE_VER_ZERO_HEADER_SIZE = 38
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
        game_mode = self.__game_type  # good
        ai_in_game = not ((self.__light_player.get_player_type()) and (self.__dark_player.get_player_type())) # good
        dark_player_is_ai = not (self.__dark_player.get_player_type())  # good
        dark_player_turn = self.__dark_play is self.__current_player  # good
        board_height = self.get_board().get_size()  # good
        board_width = board_height  # good
        colours = self.__colour_mode  # good
        timer_enabled = self.__dark_player.get_timer().get_enabled()  # good
        light_player_time = self.__light_player.get_timer().get_time_remaining_s() # good
        dark_player_time = self.__dark_player.get_timer().get_time_remaining_s() # good
        light_player_castled = self.__light_player.get_castled()
        dark_player_castled = self.__dark_player.get_castled()
        # write the header struct
        fp.write(struct.pack(">BBBBBBBBBBff", CURRENT_FILE_VERSION, game_mode,
                             ai_in_game, dark_player_is_ai, dark_player_turn,
                             board_height, board_width, colours, timer_enabled,
                             light_player_castled, dark_player_castled,
                             light_player_time, dark_player_time))
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
                        # TODO see if this works (promotions)
                        output_piece += ord("P")
                    else:
                        # unidentified piece, shouldn't be possible
                        fp.close()
                        assert(0)
                elif (self.__game_type == GAME_TYPE_CHECKERS):
                    output_piece += (1 + cur_piece.get_promotion_status())
                else:
                    # unidentified game, shouldn't be possible
                    fp.close()
                    assert(0)
                # write data
                fp.write(output_piece.to_bytes(1, byteorder="big"))
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
            # check if file is at least big enough to hold the header
            if (file_size < FILE_VER_ZERO_HEADER_SIZE):
                fp.close()
                raise ChessFileErrorOrSomethingFigureOutHowPeopleWantThisTOWOrk
            CURRENT_FILE_VERSION, game_mode, ai_in_game, dark_player_is_ai, dark_player_turn, board_height, board_width, colours, timer_enabled, light_player_castled, dark_player_castled, light_player_time, dark_player_time = struct.unpack(">BBBBBBBBBBff",fp.read(FILE_VER_ZERO_HEADER_SIZE))
            if (file_size < (FILE_VER_ZERO_HEADER_SIZE + (board_width * board_height))):
                # file too small
                fp.close()
                raise somethign
            board_data = fp.read(board_height*board_width)
            fp.close()
            if (self.__game_type != game_mode):
                # somebody set us up the bomb
                # the game object was created with a different type than the
                # file trying to be loaded
                # my lord is that legal?
                raise someExceptionIDK
            if (board_height != board_width):
                # should work according to domain model
                # but won't work as built
                fp.close()
                raise BoardWrongOrSomethingIDK
            # create board
            self.__board = Board(board_height)
            self.__colour_mode = colours
            # build player
            self.build_light_player("NotUsedInThisVersionOfSaves",
                                    (not (ai_in_game and (not dark_player_is_ai))),
                                    Timer(light_player_time, timer_enabled), light_player_castled)
            self.build_dark_player("NotUsedInThisVersionOfSaves",
                                   (not (ai_in_game and (dark_player_is_ai))),
                                    Timer(dark_player_time, timer_enabled), dark_player_castled)
            # setup board here
            board_data_index = 0
            row = 0
            while (row != board_height):
                col = 0
                while (col != board_width):
                    cur_square = self.__board.get_game_square(row,col)
                    if (board_data[board_data_index] == 0):
                        cur_square.put_piece_here(None)
                        board_data_index += 1
                        col +=1
                        continue
                    # non-empty board square
                    # check if it is dark and set the dark bit
                    if (board_data[board_data_index] & 0b100000):
                        is_dark = 1
                    else:
                        is_dark = 0
                        # decode object to char
                    if (self.__game_type == GAME_TYPE_CHESS):
                        if (board_data[board_data_index].lower()=="k"):
                            cur_square.put_piece_here(King(Colours.COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][is_dark]))
                        elif (board_data[board_data_index].lower()=="q"):
                            cur_square.put_piece_here(Queen(Colours.COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][is_dark]))
                        elif (board_data[board_data_index].lower()=="n"):
                            cur_square.put_piece_here(Knight(Colours.COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][is_dark]))
                        elif (board_data[board_data_index].lower()=="b"):
                            cur_square.put_piece_here(Bishop(Colours.COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][is_dark]))
                        elif (board_data[board_data_index].lower()=="r"):
                            cur_square.put_piece_here(Rook(Colours.COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][is_dark]))
                        elif (board_data[board_data_index].lower()=="p"):
                            cur_square.put_piece_here(Pawn(Colours.COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][is_dark]))
                            # TODO see if this works (promotions)
                        else:
                            # unidentified piece, shouldn't be possible
                                assert(0)
                    elif (self.__game_type == GAME_TYPE_CHECKERS):
                        cur_square.put_piece_here(CheckersCoin(Colours.COLOUR_STRING_LOOK_UP_TABLE[self.__colour_mode][is_dark]))
                        if (board_data[board_data_index] & 0b10):
                            cur_square.get_occupying_piece().promote()
                    else:
                        # unidentified game, shouldn't be possible
                        assert(0)
                    board_index_data += 1
                    col += 1
                row += 1
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


#if (__name__ == "__main__"):
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

