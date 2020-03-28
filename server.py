import socket
import time
import threading

HOST = '127.0.0.1'
PORT = 5005
BUFFER_SIZE = 20

class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((HOST, PORT))
        self.sock.listen(5)

        while True:
            conn, addr = self.sock.accept()
            print("Connnection from: " + str(addr))

            self.run(conn)

    def run(self, conn) -> None:
        while True:
            data = conn.recv(BUFFER_SIZE)
            # ConnectionResetError - client is closing connection but server didn't send the response
            if not data:
                break
            print("Received data: " + str(data))
            conn.send(data)

        conn.close()

t = ServerThread()

