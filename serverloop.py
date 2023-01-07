"""Run the server from the configuration"""

import json

from chess.server.gameserver import thread_loop

import os
import sys
os.chdir(sys.path[0])

with open("server_config.json", encoding="utf-8") as f:
    config = json.load(f)

port = config["port"]

if __name__ == "__main__":
    print(os.getpid())
    thread_loop(port)
    print("exited gracefully")
