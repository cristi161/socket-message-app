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
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self) -> None:
        message = input()
        if message == "q":
            self.sock.close() #a break for while is necessary
            return None
        send_message(self.sock, bytes(message, "utf8"))

class RecvThread(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
    def run(self) -> None:
        recv_msg = s.recv(BUFFER).decode("utf-8")
        print("Received message: " + str(recv_msg))

if __name__ == '__main__':
    s = create_sock()

    clients = s.recv(BUFFER).decode("utf-8")
    clients_nr = len(clients.split(":")) - 1

    if clients_nr == 1:
        print("No connected users")
    else:
        print("Connected users: " + clients)

    while True:
        input_t = InputThread(s)
        recv_t = RecvThread(s)
        input_t.start()
        recv_t.start()

        input_t.join()

        if input_t == None:
            break

    s.close()
