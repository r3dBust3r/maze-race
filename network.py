import socket
import pickle
import struct

def send_msg(sock, data):
    msg = pickle.dumps(data)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    return pickle.loads(recvall(sock, msglen))

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

class Network:
    def __init__(self, server_ip="localhost"):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server_ip
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p_id = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return recv_msg(self.client)
        except Exception as e:
            print(f"Connection failed: {e}")
            pass

    def send(self, data):
        try:
            send_msg(self.client, data)
            return recv_msg(self.client)
        except socket.error as e:
            print(e)
