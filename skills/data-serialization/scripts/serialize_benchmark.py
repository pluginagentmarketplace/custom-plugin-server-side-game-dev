#!/usr/bin/env python3
"""Benchmark different serialization formats for game data."""
import json
import time

# Sample game state
GAME_STATE = {
    "players": [
        {"id": i, "x": 100.5 + i, "y": 200.3 + i, "health": 100}
        for i in range(100)
    ],
    "tick": 12345,
    "timestamp": 1703779200.123
}

def benchmark_json(iterations: int = 10000):
    """Benchmark JSON serialization."""
    start = time.time()
    for _ in range(iterations):
        data = json.dumps(GAME_STATE)
        json.loads(data)
    elapsed = time.time() - start
    size = len(json.dumps(GAME_STATE))
    print(f"JSON: {elapsed:.3f}s, Size: {size} bytes")

def benchmark_msgpack(iterations: int = 10000):
    """Benchmark MessagePack serialization."""
    try:
        import msgpack
        start = time.time()
        for _ in range(iterations):
            data = msgpack.packb(GAME_STATE)
            msgpack.unpackb(data)
        elapsed = time.time() - start
        size = len(msgpack.packb(GAME_STATE))
        print(f"MsgPack: {elapsed:.3f}s, Size: {size} bytes")
    except ImportError:
        print("MsgPack: Not installed (pip install msgpack)")

if __name__ == "__main__":
    print("=== Serialization Benchmark ===")
    benchmark_json()
    benchmark_msgpack()
