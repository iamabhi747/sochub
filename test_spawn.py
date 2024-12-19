from soc import connect, close_socket
import socket
import sys
import select

def interactive(soc):
    while True:
        readable, _, _ = select.select([soc, sys.stdin], [], [])
        for r in readable:
            if r == sys.stdin:
                data = sys.stdin.readline()
                soc.sendall(data.encode())
            else:
                data = soc.recv(1024)
                if not data:
                    close_socket(soc)
                    return
                sys.stdout.write(data.decode())

def test_spawn(host, port, network):
    if network:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        assert connect(soc, host, port, network)
    else:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        network = connect(soc, host, port)
        if not network: return
    print('Connected to network:', network)
    interactive(soc)

if __name__ == '__main__':
    network = None
    if len(sys.argv) == 2:
        network = sys.argv[1]
    test_spawn('localhost', 12345, network)

