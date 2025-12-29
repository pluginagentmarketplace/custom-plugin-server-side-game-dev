#!/usr/bin/env python3
"""Async programming benchmark for game servers."""
import asyncio
import time

async def handle_player(player_id: int):
    """Simulate player connection handling."""
    await asyncio.sleep(0.01)  # Simulate network latency
    return f"Player {player_id} processed"

async def benchmark(num_players: int = 1000):
    """Benchmark async player handling."""
    start = time.time()
    tasks = [handle_player(i) for i in range(num_players)]
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start
    print(f"Processed {num_players} players in {elapsed:.3f}s")
    print(f"Throughput: {num_players/elapsed:.0f} players/sec")
    return results

if __name__ == "__main__":
    asyncio.run(benchmark())
