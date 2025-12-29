#!/usr/bin/env python3
"""Thread pool implementation for game server tasks."""
import threading
import queue
import time

class GameThreadPool:
    """Thread pool for CPU-bound game operations."""

    def __init__(self, num_workers: int = 4):
        self.tasks = queue.Queue()
        self.workers = []
        self.results = {}
        self._lock = threading.Lock()

        for i in range(num_workers):
            worker = threading.Thread(target=self._worker, daemon=True)
            worker.start()
            self.workers.append(worker)

    def _worker(self):
        """Worker thread that processes tasks."""
        while True:
            task_id, func, args = self.tasks.get()
            try:
                result = func(*args)
                with self._lock:
                    self.results[task_id] = result
            except Exception as e:
                with self._lock:
                    self.results[task_id] = f"Error: {e}"
            finally:
                self.tasks.task_done()

    def submit(self, task_id: str, func, *args):
        """Submit a task to the pool."""
        self.tasks.put((task_id, func, args))

    def wait_all(self):
        """Wait for all tasks to complete."""
        self.tasks.join()

def physics_calc(player_id: int) -> dict:
    """Simulate physics calculation."""
    time.sleep(0.01)  # Simulate work
    return {"player": player_id, "collision": False}

if __name__ == "__main__":
    pool = GameThreadPool(num_workers=8)
    start = time.time()

    for i in range(100):
        pool.submit(f"physics_{i}", physics_calc, i)

    pool.wait_all()
    print(f"Processed 100 physics tasks in {time.time()-start:.3f}s")
