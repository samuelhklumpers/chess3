import bisect
import threading
import time
import traceback

import tkinter as tk

from chess.structures.ruleset import Ruleset


class Game:
    def __init__(self):
        self.ruleset = Ruleset(self)


class TkGame(tk.Tk):
    def __init__(self, game: Game):
        tk.Tk.__init__(self, "game")

        self.game = game


class Tile:
    ...

