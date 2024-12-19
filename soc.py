import socket

def close_socket(socket: socket.socket):
    try: socket.close()
    except: pass

def connect(soc: socket.socket, host: str, port: int, network: str = None):
    soc.connect((host, port))
    if network:
        assert len(network) == 64, 'Invalid network'
        soc.sendall(b'C')
        soc.sendall(network.encode())
        if soc.recv(3) != b'ACK':
            close_socket(soc)
            return False
        return True
    else:
        soc.sendall(b'N')
        network = soc.recv(64).decode()
        soc.sendall(b'ACK')
        return network
