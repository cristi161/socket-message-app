import socket

HOST = "127.0.0.1"
PORT = 5005
BUFFER = 1024

def create_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    return sock

def send_message(sock, message):
    sock.send(message)
    return sock.recv(BUFFER)
