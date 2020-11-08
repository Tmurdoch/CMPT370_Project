# Board Game Simulator
# CMPT 370 Group 4
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import Pieces


class PieceSet:
    """

    """
    def __init__(self, piece_set_type, colour):
        self.castled = False
        self.pieceSetType = piece_set_type  # Has no setter method
        self.capturedPieces = []
        if piece_set_type == "Checkers" or piece_set_type == "checkers":
            self.livePieces = [Pieces.CheckersCoin(colour) for i in range(12)]
        elif piece_set_type == "Chess" or piece_set_type == "chess":
            self.livePieces = [Pieces.King(colour),
                               Pieces.Queen(colour),
                               Pieces.Rook(colour), Pieces.Rook(colour),
                               Pieces.Bishop(colour), Pieces.Bishop(colour),
                               Pieces.Knight(colour), Pieces.Knight(colour),
                               Pieces.Pawn(colour), Pieces.Pawn(colour), Pieces.Pawn(colour), Pieces.Pawn(colour),
                               Pieces.Pawn(colour), Pieces.Pawn(colour), Pieces.Pawn(colour), Pieces.Pawn(colour)]
        else:
            raise Exception("piece_set_type can only be Chess or Checkers")

    def castle(self):
        self.castled = True

    def get_castled(self):
        return self.castled

    def capture_piece(self, captured_piece):
        if captured_piece in self.livePieces:
            self.livePieces.remove(captured_piece)
            self.capturedPieces.append(captured_piece)
            return True
        else:
            return False

    def get_captured_pieces(self):
        return self.capturedPieces

    def get_piece_set_type(self):
        return self.pieceSetType

    def get_live_pieces(self):
        return self.livePieces
