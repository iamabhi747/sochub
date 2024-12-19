import socket
import os
import select
import threading

def close_socket(socket: socket.socket):
    try: socket.close()
    except: pass

class SocHub:
    def __init__(self, host, port):
        self.socket = None
        self.sockets = []
        self.networks = dict()
        self.soc_map = dict()
        self.setup_server(host, port)
        self.STOP = False

        conn_thr = threading.Thread(target=self.connection_loop)
        conn_thr.start()

        self.sync_loop()
        self.STOP = True
        conn_thr.join()

    def setup_server(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(5)
        self.socket.settimeout(5)

    def close(self):
        for socket in self.sockets:
            close_socket(socket)
        close_socket(self.socket)

    def connection_loop(self):
        while not self.STOP:
            self.accept_connection()

    def sync_loop(self):
        while not self.STOP:
            readables, _, _ = select.select(self.sockets, [], [], 1)
            print('Syncing...', len(readables), 'active')
            for readable in readables:
                try:
                    data = readable.recv(1024)
                    if not data:
                        self.sockets.remove(readable)
                        self.networks[self.soc_map[readable]].remove(readable)
                        self.soc_map.pop(readable, None)
                        close_socket(readable)
                        continue
                    for network in self.networks[self.soc_map[readable]]:
                        if network != readable:
                            network.sendall(data)
                except:
                    self.sockets.remove(readable)
                    self.networks[self.soc_map[readable]].remove(readable)
                    self.soc_map.pop(readable, None)
                    close_socket(readable)
                    continue

    def accept_connection(self):
        try:
            conn, addr = self.socket.accept()
            conn.settimeout(1)
            connection_type = conn.recv(1)

            if connection_type == b'C':
                network_auth = conn.recv(64).decode()
                if network_auth not in self.networks:
                    close_socket(conn)
                    return
                conn.sendall(b'ACK')
                conn.settimeout(None)
                self.sockets.append(conn)
                self.networks[network_auth].append(conn)
                self.soc_map[conn] = network_auth

            elif connection_type == b'N':
                network_auth = os.urandom(32).hex()
                conn.sendall(network_auth.encode())
                ack = conn.recv(3)
                if ack != b'ACK':
                    close_socket(conn)
                    return
                conn.settimeout(None)
                self.networks[network_auth] = [conn]
                self.sockets.append(conn)
                self.soc_map[conn] = network_auth
            
            else:
                close_socket(conn)
                return
            
            print('Connected:', addr, "Network:", network_auth)
                
        except:
            return