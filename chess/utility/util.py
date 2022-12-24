import itertools as itr
import numpy as np
import json


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return itr.zip_longest(*args, fillvalue=fillvalue)


def xyiter(x1, y1, x2, y2, incl_start=False, incl_end=False):
    sx = int(np.sign(x2 - x1))
    sy = int(np.sign(y2 - y1))

    if incl_start:
        yield x1, y1

    x1 += sx
    y1 += sy

    while not (sx != 0 and x1 == x2) and not (sy != 0 and y1 == y2):
        yield x1, y1

        x1 += sx
        y1 += sy

    if incl_end:
        yield x2, y2


def unpack2ddr(args):
        x1, y1 = args[0]
        x2, y2 = args[1]

        dx, dy = x2 - x1, y2 - y1

        return dx, dy

def read_file(fn):
    with open(fn, mode="r", encoding="utf-8") as f:
        return f.read()
        
def write_file(fn, text):
    with open(fn, mode="w", encoding="utf-8") as f:
        f.write(text)

def jload(fn):
    return json.loads(read_file(fn))

def jdump(fn, x):
    return write_file(fn, json.dumps(x, indent=4))


__all__ = ["grouper", "xyiter", "unpack2ddr", "jload", "jdump"]
