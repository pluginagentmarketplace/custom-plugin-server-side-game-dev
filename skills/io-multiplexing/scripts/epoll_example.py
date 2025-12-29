#!/usr/bin/env python3
"""I/O multiplexing example using select (cross-platform epoll alternative)."""
import socket
import select

def run_multiplexed_server(host='0.0.0.0', port=9999):
    """Run a multiplexed game server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(100)
    server.setblocking(False)

    sockets = [server]
    print(f"Multiplexed server running on {host}:{port}")

    try:
        while True:
            readable, _, _ = select.select(sockets, [], [], 0.1)
            for sock in readable:
                if sock is server:
                    conn, addr = server.accept()
                    conn.setblocking(False)
                    sockets.append(conn)
                    print(f"Player connected: {addr}")
                else:
                    try:
                        data = sock.recv(1024)
                        if data:
                            # Process game message
                            sock.send(b"ACK")
                        else:
                            sockets.remove(sock)
                            sock.close()
                    except:
                        sockets.remove(sock)
                        sock.close()
    except KeyboardInterrupt:
        print("Server shutdown")
    finally:
        server.close()

if __name__ == "__main__":
    run_multiplexed_server()
