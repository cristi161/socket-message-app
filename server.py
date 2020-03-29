import socket
import threading

HOST = '127.0.0.1'
PORT = 5005
BUFFER_SIZE = 1024

def close_connection(sock, addr):
    sock.close()
    print(str(addr) + " has been disconnected")

class ConnectionThread(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.client_sock = conn
        self.addr = addr

    def run(self) -> None:
        message = ""
        while True:
            data = self.client_sock.recv(BUFFER_SIZE)
            if not data:
                break
            message = message.join(str(data))
            self.client_sock.send(b"Message received")
            print(str(self.addr) + " said: " + str(data) + "(" + str(self.name) + ")")
        print(str(self.addr) + " has been disconnected")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

print("Server started")
print("Waiting for connection...")

thread_pool = []
thread_pool_size = 0

while True:
    sock.listen(1)
    conn, addr = sock.accept()
    newthread = ConnectionThread(conn, addr)
    newthread.start()
    print(str(addr) + " is connected")
    #newthread.join()
    #conn.close()
