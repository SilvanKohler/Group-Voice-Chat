import socket, threading, sys
clients = []
CHUNK = 4096
count = 0
users = 0
class forwarding(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        global count
        threading.Thread.__init__(self)
        self.num = count
        count += 1
        clients.append(clientsocket)
        self.csocket = clientsocket
        self.addr = clientAddress
        print('Client at ' + str(clientAddress) + ' queued...')
    def run(self):
        global count
        global users
        print('Client at ' + str(clientAddress) + ' connected to voice-chat.')
        users += 1
        print('{} users'.format(users))
        while True:
            try:
                data = self.csocket.recv(CHUNK)
            except:
                print('Client at ' + str(clientAddress) + ' disconnected...')
                clients.remove(clients[self.num])
                count -= 1
                users -= 1
                print('{} users'.format(users))
                break
            finally:
                for i in range(len(clients)):
                    if not i == self.num:
                        try:
                            clients[i].send(data)
                        except:
                            pass
if len(sys.argv) > 1:
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
else:
    IP = '0.0.0.0'
    PORT = 65535
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((IP, PORT))
print('Server started on ' + str(IP) + ':' + str(PORT))
print('Waiting for client request..')
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = forwarding(clientAddress, clientsock)
    newthread.start()
