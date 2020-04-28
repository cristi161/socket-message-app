import socket
import threading

HOST = '127.0.0.1'
PORT = 5005
BUFFER_SIZE = 1024

connected_clients_ports   = {}
connected_clients_sockets = {}

##akshbdashbd


class ConnectionThread(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.client_sock = conn
        self.addr = addr
        self.name = "client_port:" + str(addr[1])

    def run(self) -> None:
        message = ""
        while True:
            data = self.client_sock.recv(BUFFER_SIZE)
            if not data:
                break
            message = message.join(str(data))

            dest, msg = process_message(data.decode("utf-8"))
            get_sock(dest).sendall(bytes(msg, "utf8"))
            #self.client_sock.send(b"Message received")
            print(str(self.addr) + " said: " + str(data) + "(" + str(self.name) + ")")
        connected_clients_ports[addr[1]] = False
        print(str(self.addr) + " has been disconnected")

    def bind(self, conn, addr):
        self.client_sock = conn
        self.addr = addr

def get_sock(port) -> socket:
    return connected_clients_sockets[port]

def process_message(msg = ""):
    message = msg.split("::")

    return int(message[0]), message[1]


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))

    print("Server started")
    print("Waiting for connection...")

    #tp = create_thread_pool(20)
    #tp_size = 0

    while True:
        clients = ''
        sock.listen(1)
        conn, addr = sock.accept()

        if not connected_clients_ports.get(addr[1]):
            connected_clients_ports[addr[1]] = True
            connected_clients_ports[str(addr[1])+"_ws"] = conn
        for key, value in connected_clients_ports.items():
            if value is True:
                if addr[1] == key:
                    clients = clients + str(key) + "(you):"
                else:
                    clients = clients + str(key) + ":"
        conn.sendall(bytes(clients, "utf8"))

        connected_clients_sockets[int(addr[1])] = conn

        newthread = ConnectionThread(conn, addr)
        newthread.start()

        print(str(addr) + " is connected")
        #newthread.join()
        #conn.close()