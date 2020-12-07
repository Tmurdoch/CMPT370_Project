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

# make the c-stdlib style definitions
SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2


def save_to_file(game, path):
    """
    Saves the current game state to file.
    :param game: The game you would like to save to file
    :param path: string: describing file path to save too
    :return: None
    """
    fp = open(path+"/save-game.cmpt370" +
              GAME_TYPE_STRING_LOOK_UP_TABLE[game.get_game_type()], "wb")
    fp.write(MAGIC)
    game_mode = game.get_game_type()
    ai_in_game = not ((game.get_light_player().get_player_type()) and (
        game.get_dark_player().get_player_type()))
    dark_player_is_ai = not (game.get_dark_player().get_player_type())
    dark_player_turn = game.get_dark_player() is game.get_current_player()
    board_height = game.get_board().get_size()
    board_width = board_height
    colours = game.get_colour_mode()
    timer_enabled = game.get_dark_player().get_timer().get_enabled()
    light_player_time = game.get_light_player().get_timer().get_time_remaining_s()
    dark_player_time = game.get_dark_player().get_timer().get_time_remaining_s()
    board_colour = game.get_board_colour_mode()
    unused_reserved = 117

    # Write the header struct
    fp.write(struct.pack(">BBBBBBBBBBBff", CURRENT_FILE_VERSION, game_mode,
                         ai_in_game, dark_player_is_ai, dark_player_turn,
                         board_height, board_width, colours, timer_enabled,
                         board_colour, unused_reserved,
                         light_player_time, dark_player_time))

    row = 0
    while row != board_height:
        col = 0
        while col != board_width:
            cur_piece = game.get_board().get_game_square(
                row, col).get_occupying_piece()
            if cur_piece is None:
                fp.write((0).to_bytes(1, byteorder="big"))
                col += 1
                continue
            # Check if it is dark and set the dark bit
            if cur_piece.get_colour() == COLOUR_STRING_LOOK_UP_TABLE[game.get_colour_mode()][ColourOffset.OFFSET_DARK]:
                output_piece = 0b100000
            else:
                output_piece = 0
            # Decode object to char
            if game.get_game_type() == GameType.CHESS:
                if isinstance(cur_piece, King):
                    if cur_piece.get_moved_yet_status():
                        output_piece += ord("L")  # moved king
                    else:
                        output_piece += ord("K")  # Regular king
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
                        output_piece += ord("M")  # The pawn is a moved pawn
                    else:
                        output_piece += ord("P")  # The pawn is an unmoved pawn
                else:
                    # unidentified piece, shouldn't be possible
                    fp.close()
                    assert 0

            elif game.get_game_type() == GameType.CHECKERS:
                output_piece += (1 + cur_piece.is_promoted())

            else:
                # Unidentified game, shouldn't be possible
                fp.close()
                assert 0

            fp.write(output_piece.to_bytes(1, byteorder="big"))
            col += 1
        row += 1
    fp.close()
