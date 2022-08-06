import json
import sys

from server.gameserver import thread_loop

PORT = 8080
if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
    
if __name__ == "__main__":
    thread_loop(PORT)
