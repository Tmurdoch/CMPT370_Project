# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

from Colours import ColourOffset, COLOUR_STRING_LOOK_UP_TABLE
from Pieces import King, Queen, Knight, Bishop, Rook, Pawn
import struct
from GameType import GameType

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


def save_to_file(game, path):
    """
    Saves the current game state to a file
    path: string describing file path to save too
    :return: None
    """
    fp = open(path+"/save-game.cmpt370" +
              GAME_TYPE_STRING_LOOK_UP_TABLE[self.__game_type], "wb")
    # write magic
    fp.write(MAGIC)
    game_mode = game.__game_type  # TODO: Isn't this a string? "chess" or "checkers"
    ai_in_game = not ((game.__light_player.get_player_type()) and (
        game.__dark_player.get_player_type()))  # good
    dark_player_is_ai = not (game.__dark_player.get_player_type())  # good
    dark_player_turn = game.__dark_player is game.__current_player  # good
    board_height = game.get_board().get_size()  # good
    board_width = board_height  # good
    colours = game.__colour_mode  # good
    timer_enabled = game.__dark_player.get_timer().get_enabled()  # good
    light_player_time = game.__light_player.get_timer().get_time_remaining_s()  # good
    dark_player_time = game.__dark_player.get_timer().get_time_remaining_s()  # good
    board_colour = game.__board_colour_mode
    unused_reserved = 117
    # write the header struct
    fp.write(struct.pack(">BBBBBBBBBBBff", CURRENT_FILE_VERSION, game_mode,
                         ai_in_game, dark_player_is_ai, dark_player_turn,
                         board_height, board_width, colours, timer_enabled,
                         board_colour, unused_reserved,
                         light_player_time, dark_player_time))
    row = 0
    while row != board_height:
        col = 0
        while col != board_width:
            cur_piece = game.__board.get_game_square(
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
            if game.__game_type == GameType.CHESS:
                if isinstance(cur_piece, King):
                    if cur_piece.get_moved_yet_status():
                        # moved king
                        output_piece += ord("L")
                    else:
                        # Regular king
                        output_piece += ord("K")
                elif isinstance(cur_piece, Queen):
                    output_piece += ord("Q")
                elif isinstance(cur_piece, Knight):
                    output_piece += ord("N")
                elif isinstance(cur_piece, Bishop):
                    output_piece += ord("B")
                elif isinstance(cur_piece, Rook):
                    if cur_piece.get_moved_yet_status():
                        output_piece += ord("S")
                    else:
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
            elif game.__game_type == GameType.CHECKERS:
                output_piece += (1 + cur_piece.is_promoted())
            else:
                # unidentified game, shouldn't be possible
                fp.close()
                assert 0
            # write data
            fp.write(output_piece.to_bytes(1, byteorder="big"))
            col += 1
        row += 1
    fp.close()
