#!/usr/bin/env python3
"""UDP game server for low-latency player updates."""
import socket
import struct
import time

# Packet format: player_id (4), x (4), y (4), timestamp (8)
PACKET_FORMAT = "!IffQ"
PACKET_SIZE = struct.calcsize(PACKET_FORMAT)

def run_udp_server(host='0.0.0.0', port=9999):
    """Run UDP game server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    sock.setblocking(False)

    players = {}
    print(f"UDP Server running on {host}:{port}")

    try:
        while True:
            try:
                data, addr = sock.recvfrom(PACKET_SIZE)
                if len(data) == PACKET_SIZE:
                    player_id, x, y, timestamp = struct.unpack(PACKET_FORMAT, data)
                    players[player_id] = {
                        'x': x, 'y': y,
                        'addr': addr,
                        'last_update': time.time()
                    }
                    # Broadcast to other players
                    for pid, pdata in players.items():
                        if pid != player_id:
                            sock.sendto(data, pdata['addr'])
            except BlockingIOError:
                # No data available, continue
                pass
            except Exception as e:
                print(f"Error: {e}")

            # Cleanup inactive players
            current = time.time()
            players = {k: v for k, v in players.items()
                      if current - v['last_update'] < 30}

            time.sleep(0.001)  # 1ms tick
    except KeyboardInterrupt:
        print("Server shutdown")
    finally:
        sock.close()

if __name__ == "__main__":
    run_udp_server()
