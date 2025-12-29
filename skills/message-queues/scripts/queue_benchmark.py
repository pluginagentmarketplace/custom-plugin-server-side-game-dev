#!/usr/bin/env python3
"""Message queue benchmark for game server events."""
import asyncio
import time
from collections import deque

class GameEventQueue:
    """Simple in-memory event queue for benchmarking."""

    def __init__(self):
        self.queue = deque(maxlen=100000)
        self.processed = 0

    def publish(self, event: dict):
        """Publish event to queue."""
        self.queue.append(event)

    def consume(self) -> dict:
        """Consume event from queue."""
        if self.queue:
            self.processed += 1
            return self.queue.popleft()
        return None

async def benchmark(events: int = 100000):
    """Benchmark queue throughput."""
    queue = GameEventQueue()

    # Publish events
    start = time.time()
    for i in range(events):
        queue.publish({
            "type": "player_move",
            "player_id": i % 100,
            "x": i * 0.1,
            "y": i * 0.2
        })
    publish_time = time.time() - start

    # Consume events
    start = time.time()
    while queue.consume():
        pass
    consume_time = time.time() - start

    print(f"Published {events} events in {publish_time:.3f}s")
    print(f"Consumed {queue.processed} events in {consume_time:.3f}s")
    print(f"Throughput: {events/(publish_time+consume_time):.0f} events/sec")

if __name__ == "__main__":
    asyncio.run(benchmark())
