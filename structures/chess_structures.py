import socket
import threading

import numpy as np
import itertools as itr

from typing import Optional, Callable

from structures.structures import *
from utility.util import *
from structures.colours import *


class Piece:
    def __init__(self, shape="A", col="w"):
        self.shape = shape
        self.col = col
        self.double = False

    def get_colour(self):
        return self.col


class NormalTile(Tile):
    def __init__(self):
        self.piece = None

    def get_piece(self):
        return self.piece

    def set_piece(self, piece: Piece):
        ret, self.piece = self.piece, piece
        return ret


class MovedPiece(Piece):
    def __init__(self, shape="A", col="w"):
        Piece.__init__(self, shape=shape, col=col)

        self.moved = 0


class Pawn(MovedPiece):
    def __init__(self, shape=None, col="w"):
        MovedPiece.__init__(self, shape="p", col=col)

        self.double = False


def parse_boardstr(boardstr: str):
    players = boardstr.split(";")

    pieces = []

    for player in players:
        col = player[0]
        shapes = player[1:]

        for x, y, shape in grouper(shapes, 3):
            i = ord(x) - ord("a")
            j = int(y) - 1
            pos = (i, j)

            pieces += [(pos, col, shape)]

    return pieces


class Chess(Game):
    def __init__(self):
        Game.__init__(self)

        self.board: Optional[Board] = None
        #self.counter: Optional[PieceCounter] = None
        #self.tkchess: Optional[TkChess] = None

        self.socket: Optional[socket.socket] = None
        self.socket_thread: Optional[threading.Thread] = None

        self.object_map = {0: None}
        self.obj_count = 1

        self.turn = "w"
        self.player = "bw"
        self.turn_num = 1

        self.receiving = True

    def set_ruleset(self, ruleset: Ruleset):
        self.ruleset = ruleset

    def set_board(self, board: "Board"):
        self.board = board

    def get_board(self):
        return self.board

    def set_socket(self, socket: "socket.socket"):
        self.socket = socket

    def get_id(self, item):
        return next(k for k, v in self.object_map.items() if v == item)

    def get_by_id(self, item_id: int):
        return self.object_map[item_id]

    def add_object(self, item):
        tag = self.obj_count
        self.object_map[tag] = item
        self.obj_count += 1
        return tag

    def process(self, effect: str, args):
        if self.ruleset:
            self.ruleset.process(effect, args)

    def get_turn(self):
        return self.turn

    def get_turn_num(self):
        return self.turn_num

    def get_player(self):
        return self.player

    def load_board_str(self, board_str: str):
        for pos, col, shape in parse_boardstr(board_str):
            self.ruleset.process("create_piece", (pos, col, shape))



class Board:
    def __init__(self, game: Chess, nx=8, ny=8):
        self.game = game
        #self.tkboard: Optional[TkBoard] = None

        self.nx, self.ny = nx, ny

        self.tiles = np.empty((self.nx, self.ny), dtype=object)

        self.views = {}

    def make_tiles(self, tile_constr: Callable[[], Tile]):
        for ix, v in np.ndenumerate(self.tiles):
            self.tiles[ix] = tile_constr()

    def click(self, tile_i):
        self.game.process("touch", (tuple(tile_i), self.game.get_player()))

    def shape(self):
        return self.nx, self.ny

    def tile_ids(self):
        nx, ny = self.shape()
        for i, j in itr.product(range(nx), range(ny)):
            yield i, j

    def get_game(self):
        return self.game

    def get_views(self):
        return self.views

    def get_piece(self, tile_i):
        return self.get_tile(tile_i).get_piece()

    def get_tile(self, tile_i):
        try:
            return self.tiles[tuple(tile_i)]
        except IndexError:
            return None



def search_valid(self, game: Chess, around):  # around must be tile_id
    self.success_indicator.unset()
    for tile_id in game.board.tile_ids():
        self.subruleset.process(self.move0, (around, tile_id))

        if self.success_indicator.is_set():
            yield tile_id

        self.success_indicator.unset()


__all__ = ["PieceCounter", "NormalTile", "Piece", "MovedPiece", "Pawn", "Chess", "Board", "search_valid"]