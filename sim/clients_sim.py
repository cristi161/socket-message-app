import threading
import client

class SimClientThread(threading.Thread):
    def __init__(self, message=False):
        threading.Thread.__init__(self)
        self.message = message
    def run(self) -> None:
        sock = client.create_sock()
        if self.message != False:
            print(client.send_message(sock, message=self.message))
        else:
            print(client.send_message(sock, message=bytes(self.name, 'utf8')))
        sock.close()

def create_clients(number, start = False):
    threads = []
    for i in range(number):
        threads.append(SimClientThread())

    if start==False:
        return threads
    elif start==True:
        for simClientThread in threads:
            simClientThread.start()
    else:
        return False

create_clients(12, start=True)
