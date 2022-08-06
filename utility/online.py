import socket
import threading
import time
import traceback



def make_socket(remote_address, remote_port, local_port=None, active=True):
    if not local_port:
        local_port = remote_port

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("", local_port))

    def listen(s, ret):
        print("listening")
        s.listen(0)
        s, a = s.accept()
        print("accepted", a)

        ret.append((s, a))

    if active:
        print("trying to connect", (remote_address, remote_port))

        while True:
            try:
                s.connect((remote_address, remote_port))
                break
            except:
                traceback.print_exc()
                print("retrying")
                time.sleep(10)
    else:
        ret = []

        t = threading.Thread(target=lambda: listen(s, ret))
        t.start()

        try:
            while t.is_alive():
                t.join(1)
            s, a = ret[0]
        except:
            s.close()
            t.join()
            print("stopping listening")
            return

    print("connected")

    return s


__all__ = ["OnlineDialog", "make_socket"]