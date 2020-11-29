# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import os
from Board import Board
import struct
from GameType import GameType
from Timer import Timer

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


def load_from_file(game, path):
    """
    Load game state from file
    This is expected to be called from the ui object
    Which has already checked for the existence of the save game
    DELETES THE FILE IF IT IS SUCCESSFULLY LOADED
    :param game: Game: The game we are going to load in
    :param path: string describing file path to save too
    :return: None
    """
    fp = open(path+"/save-game.cmpt370" +
              GAME_TYPE_STRING_LOOK_UP_TABLE[game.get_game_type()], "rb")
    read_magic = fp.read(20)
    if read_magic != MAGIC:
        raise Exception(
            "ChessFileErrorOrSomethingFigureOutHowPeopleWantThisTOWOrk")

    file_version = int.from_bytes(
        fp.read(1), byteorder="big", signed=False)
    if file_version == 0:
        # Do stuff for file version 0 if the file version changes add an "elif" after this with the new code
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
            board_width, colours, timer_enabled, board_colour, unused_reserved, light_player_time, \
            dark_player_time = struct.unpack(">BBBBBBBBBBBff", f)

        if file_size < (FILE_VER_ZERO_HEADER_SIZE + (board_width * board_height)):
            # file too small
            fp.close()
            raise Exception("something")
        board_data = fp.read(board_height*board_width)
        fp.close()

        if game.get_game_type() != game_mode:
            # somebody set us up the bomb the game object was created with a different type than the
            # file trying to be loaded my lord is that legal?
            raise Exception("someExceptionIDK")

        if board_height != board_width:
            # should work according to domain model but won't work as built
            fp.close()
            raise Exception("BoardWrongOrSomethingIDK")

        game.set_board(Board(board_height))
        game.set_colour_mode(colours)
        game.set_board_colour_mode(board_colour)

        game.build_light_player("NotUsedInThisVersionOfSaves",
                                (not (ai_in_game and (not dark_player_is_ai))),
                                Timer(light_player_time, timer_enabled))

        game.build_dark_player("NotUsedInThisVersionOfSaves",
                               (not (ai_in_game and dark_player_is_ai)),
                               Timer(dark_player_time, timer_enabled))

        # Setup board here
        board_data_index = 0
        found_dark_checkers_pieces = 0
        found_light_checkers_pieces = 0
        found_light_king = 0
        found_light_queen = 0
        found_light_rook = 0
        found_light_bishop = 0
        found_light_knight = 0
        found_light_pawn = 0
        found_dark_king = 0
        found_dark_queen = 0
        found_dark_rook = 0
        found_dark_bishop = 0
        found_dark_knight = 0
        found_dark_pawn = 0
        row = 0
        while row != board_height:
            col = 0
            while col != board_width:
                cur_square = game.get_board().get_game_square(row, col)
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
                if game.get_game_type() == GameType.CHESS:
                    if chr(board_data[board_data_index]).lower() == "k":
                        if is_dark:
                            assert found_dark_king != 1
                            cur_square.put_piece_here(game.get_dark_player().get_piece_set().get_all_pieces()[0])
                            found_dark_king += 1
                        else:
                            assert found_light_king != 1
                            cur_square.put_piece_here(game.get_light_player().get_piece_set().get_all_pieces()[0])
                            found_light_king += 1
                    elif chr(board_data[board_data_index]).lower() == "l":  # lima - just in case your fonts suck Il1
                        if is_dark:
                            assert found_dark_king != 1
                            cur_square.put_piece_here(game.get_dark_player().get_piece_set().get_all_pieces()[0])
                            found_dark_king += 1
                        else:
                            assert found_light_king != 1
                            cur_square.put_piece_here(game.get_light_player().get_piece_set().get_all_pieces()[0])
                            found_light_king += 1
                        cur_square.get_occupying_piece().move()
                    elif chr(board_data[board_data_index]).lower() == "q":
                        if is_dark:
                            assert found_dark_queen != 1
                            cur_square.put_piece_here(game.get_dark_player().get_piece_set().get_all_pieces()[1])
                            found_dark_queen += 1
                        else:
                            assert found_light_queen != 1
                            cur_square.put_piece_here(game.get_light_player().get_piece_set().get_all_pieces()[1])
                            found_light_queen += 1
                    elif chr(board_data[board_data_index]).lower() == "n":
                        if is_dark:
                            assert (found_dark_knight != 2)
                            cur_square.put_piece_here(game.get_dark_player().get_piece_set().get_all_pieces()[6+found_dark_knight])
                            found_dark_knight += 1
                        else:
                            assert (found_light_knight != 2)
                            cur_square.put_piece_here(game.get_light_player().get_piece_set().get_all_pieces()[6+found_light_knight])
                            found_light_knight += 1
                    elif chr(board_data[board_data_index]).lower() == "b":
                        if is_dark:
                            assert (found_dark_bishop != 2)
                            cur_square.put_piece_here(game.get_dark_player().get_piece_set().get_all_pieces()[4+found_dark_bishop])
                            found_dark_bishop += 1
                        else:
                            assert (found_light_bishop != 2)
                            cur_square.put_piece_here(game.get_light_player().get_piece_set().get_all_pieces()[4+found_light_bishop])
                            found_light_bishop += 1
                    elif chr(board_data[board_data_index]).lower() == "r":
                        if is_dark:
                            assert (found_dark_rook != 2)
                            cur_square.put_piece_here(game.get_dark_player().get_piece_set().get_all_pieces()[2+found_dark_rook])
                            found_dark_rook += 1
                        else:
                            assert (found_light_rook != 2)
                            cur_square.put_piece_here(game.get_light_player().get_piece_set().get_all_pieces()[2+found_light_rook])
                            found_light_rook += 1
                    elif chr(board_data[board_data_index]).lower() == "s":
                        if is_dark:
                            assert (found_dark_rook != 2)
                            cur_square.put_piece_here(game.get_dark_player().get_piece_set().get_all_pieces()[2+found_dark_rook])
                            found_dark_rook += 1
                        else:
                            assert (found_light_rook != 2)
                            cur_square.put_piece_here(game.get_light_player().get_piece_set().get_all_pieces()[2+found_light_rook])
                            found_light_rook += 1
                        cur_square.get_occupying_piece().move()
                    elif chr(board_data[board_data_index]).lower() == "p":
                        # The pawn is an unmoved pawn
                        if is_dark:
                            assert (found_dark_pawn != 8)
                            cur_square.put_piece_here(game.get_dark_player().get_piece_set().get_all_pieces()[8+found_dark_pawn])
                            found_dark_pawn += 1
                        else:
                            assert (found_light_pawn != 8)
                            cur_square.put_piece_here(game.get_light_player().get_piece_set().get_all_pieces()[8+found_light_pawn])
                            found_light_pawn += 1
                    elif chr(board_data[board_data_index]).lower() == "m":
                        # The pawn is an moved pawn
                        if is_dark:
                            assert (found_dark_pawn != 8)
                            cur_square.put_piece_here(game.get_dark_player().get_piece_set().get_all_pieces()[8+found_dark_pawn])
                            found_dark_pawn += 1
                        else:
                            assert (found_light_pawn != 8)
                            cur_square.put_piece_here(game.get_light_player().get_piece_set().get_all_pieces()[8+found_light_pawn])
                            found_light_pawn += 1
                        cur_square.get_occupying_piece().move()
                    else:
                        # unidentified piece, shouldn't be possible
                        print(chr(board_data[board_data_index]))
                        assert 0

                elif game.get_game_type() == GameType.CHECKERS:
                    if is_dark:
                        cur_square.put_piece_here(
                            game.get_dark_player().get_piece_set().get_all_pieces()[
                                found_dark_checkers_pieces]
                        )
                        found_dark_checkers_pieces += 1
                    else:
                        cur_square.put_piece_here(
                            game.get_light_player().get_piece_set().get_all_pieces()[
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
        if game.get_game_type() == GameType.CHECKERS:
            # Start at the back of the list of live pieces not placed on the board and capture them
            i = 0
            while i != (12-found_dark_checkers_pieces):
                game.get_dark_player().get_piece_set().capture_piece(
                    game.get_dark_player().get_piece_set().get_live_pieces()[
                        11-i]
                )
                i += 1
            i = 0
            while i != (12-found_light_checkers_pieces):
                game.get_light_player().get_piece_set().capture_piece(
                    game.get_light_player().get_piece_set().get_live_pieces()[
                        11-i]
                )
                i += 1
        elif game.get_game_type() == GameType.CHESS:
            # king
            if not found_dark_king:
                game.get_dark_player().get_piece_set().capture_piece(
                    game.get_dark_player().get_piece_set().get_all_pieces()[0])
            if not found_light_king:
                game.get_light_player().get_piece_set().capture_piece(
                    game.get_light_player().get_piece_set().get_all_pieces()[0])
            # queen
            if not found_dark_queen:
                game.get_dark_player().get_piece_set().capture_piece(
                    game.get_dark_player().get_piece_set().get_all_pieces()[1])
            if not found_light_queen:
                game.get_light_player().get_piece_set().capture_piece(
                    game.get_light_player().get_piece_set().get_all_pieces()[1])
            # rook
            while found_dark_rook != 2:
                game.get_dark_player().get_piece_set().capture_piece(
                    game.get_dark_player().get_piece_set().get_all_pieces()[1+found_dark_rook])
                found_dark_rook += 1
            while found_light_rook != 2:
                game.get_light_player().get_piece_set().capture_piece(
                    game.get_light_player().get_piece_set().get_all_pieces()[1+found_light_rook])
                found_light_rook += 1
            # bishop
            while found_dark_bishop != 2:
                game.get_dark_player().get_piece_set().capture_piece(
                    game.get_dark_player().get_piece_set().get_all_pieces()[3+found_dark_bishop])
                found_dark_bishop += 1
            while found_light_bishop != 2:
                game.get_light_player().get_piece_set().capture_piece(
                    game.get_light_player().get_piece_set().get_all_pieces()[3+found_light_bishop])
                found_light_bishop += 1
            # knight
            while found_dark_knight != 2:
                game.get_dark_player().get_piece_set().capture_piece(
                    game.get_dark_player().get_piece_set().get_all_pieces()[5+found_dark_knight])
                found_dark_knight += 1
            while found_light_knight != 2:
                game.get_light_player().get_piece_set().capture_piece(
                    game.get_light_player().get_piece_set().get_all_pieces()[5+found_light_knight])
                found_light_knight += 1
            # pawn
            while found_dark_pawn != 8:
                game.get_dark_player().get_piece_set().capture_piece(
                    game.get_dark_player().get_piece_set().get_all_pieces()[7+found_dark_pawn])
                found_dark_pawn += 1
            while found_light_pawn != 8:
                game.get_light_player().get_piece_set().capture_piece(
                    game.get_light_player().get_piece_set().get_all_pieces()[7+found_light_pawn])
                found_light_pawn += 1
        # delete the file after loading
        os.remove(path+"/save-game.cmpt370" + GAME_TYPE_STRING_LOOK_UP_TABLE[game.get_game_type()])
        return

    else:
        fp.close()
        # ui.showError("File version " + str(file_version) + " unsupported in this version, update the game")
        raise Exception("ChessFileErrorOrSomethingFigureOutHowPeopleWantThisTOWOrk")
