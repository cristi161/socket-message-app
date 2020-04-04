import socket
import threading

HOST = "127.0.0.1"
PORT = 5005
BUFFER = 1024


def create_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    return sock


def send_message(sock, message):
    sock.sendall(message)
    return sock.recv(BUFFER)


class InputThread(threading.Thread):
    def __init__(self, sock, _dest):
        threading.Thread.__init__(self)
        self.sock = sock
        self.dest = _dest

    def run(self) -> None:
        while True:
            print(self.dest + "::", end='')
            message = input()
            if message == "q":
                self.sock.close()  # a break for while is necessary
                break
            send_message(self.sock, bytes(self.dest + "::" + message, "utf8"))


class RecvThread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self) -> None:
        try:
            while True:
                recv_msg = s.recv(BUFFER).decode("utf-8")
                print("Received message: " + str(recv_msg))
        except Exception:
            pass


if __name__ == '__main__':
    s = create_sock()

    clients = s.recv(BUFFER).decode("utf-8")
    clients_lst = clients.split(":")
    clients_nr = len(clients_lst) - 1

    if clients_nr == 1:
        print("Connected users: " + clients_lst[0] + "(you)")
    else:
        print("Connected users: " + ', '.join(clients_lst[:-1]))

    print("Choose a client from connected users")
    dest = input()  # port of the recipient of the message

    input_t = InputThread(s, dest)
    recv_t = RecvThread(s)
    input_t.start()
    recv_t.start()

    #input_t.join()

    #s.close()
