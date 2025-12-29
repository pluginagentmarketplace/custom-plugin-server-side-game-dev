#!/usr/bin/env python3
"""
Database Performance Benchmark for Game Servers
Compares Redis, PostgreSQL, and Cassandra write/read performance
"""

import time
import random
import json
from typing import Dict, List, Tuple

class GameDataBenchmark:
    """Benchmark game server database operations"""

    def __init__(self):
        self.player_data = {
            'player_id': random.randint(1, 1000000),
            'position': {'x': random.random() * 100, 'y': random.random() * 100},
            'health': random.randint(1, 100),
            'inventory': [{'item_id': i, 'quantity': random.randint(1, 10)} for i in range(5)],
            'timestamp': time.time()
        }

    def simulate_redis_write(self) -> float:
        """Simulate Redis SET operation (in-memory, fastest)"""
        start = time.time()
        # Simulate: redis.set(f"player:{id}", json.dumps(data), ex=3600)
        json.dumps(self.player_data)  # Serialization cost
        time.sleep(0.0001)  # Network latency simulation
        return (time.time() - start) * 1000

    def simulate_postgres_write(self) -> float:
        """Simulate PostgreSQL UPDATE operation"""
        start = time.time()
        # Simulate: INSERT INTO player_state (id, data) VALUES (...) ON CONFLICT UPDATE
        json.dumps(self.player_data)
        time.sleep(0.005)  # Network + disk sync latency
        return (time.time() - start) * 1000

    def simulate_cassandra_write(self) -> float:
        """Simulate Cassandra WRITE_ONE consistency operation"""
        start = time.time()
        # Simulate: INSERT INTO player_state (id, position, health) VALUES (...)
        json.dumps(self.player_data)
        time.sleep(0.003)  # Distributed write latency
        return (time.time() - start) * 1000

    def run_benchmark(self, iterations: int = 1000) -> Dict:
        """Run comprehensive benchmark"""
        results = {
            'redis': [],
            'postgresql': [],
            'cassandra': []
        }

        print(f"Running {iterations} iterations per database...")

        # Redis benchmark
        for _ in range(iterations):
            results['redis'].append(self.simulate_redis_write())

        # PostgreSQL benchmark
        for _ in range(iterations):
            results['postgresql'].append(self.simulate_postgres_write())

        # Cassandra benchmark
        for _ in range(iterations):
            results['cassandra'].append(self.simulate_cassandra_write())

        return results

    def calculate_stats(self, times: List[float]) -> Dict:
        """Calculate statistics from latency measurements"""
        times_sorted = sorted(times)
        return {
            'min': min(times),
            'max': max(times),
            'avg': sum(times) / len(times),
            'p95': times_sorted[int(len(times) * 0.95)],
            'p99': times_sorted[int(len(times) * 0.99)]
        }

    def print_results(self, results: Dict):
        """Print benchmark results"""
        print("\n" + "=" * 70)
        print("GAME SERVER DATABASE BENCHMARK RESULTS")
        print("=" * 70)

        for db_name, latencies in results.items():
            stats = self.calculate_stats(latencies)
            print(f"\n{db_name.upper():15} | Latency Percentiles (ms)")
            print("-" * 70)
            print(f"{'Min':15} | {stats['min']:8.3f} ms")
            print(f"{'Average':15} | {stats['avg']:8.3f} ms")
            print(f"{'P95':15} | {stats['p95']:8.3f} ms")
            print(f"{'P99':15} | {stats['p99']:8.3f} ms")
            print(f"{'Max':15} | {stats['max']:8.3f} ms")

        print("\n" + "=" * 70)
        print("RECOMMENDATION")
        print("=" * 70)
        avg_redis = self.calculate_stats(results['redis'])['avg']
        avg_postgres = self.calculate_stats(results['postgresql'])['avg']
        avg_cassandra = self.calculate_stats(results['cassandra'])['avg']

        print(f"\n✅ Redis (in-memory):     {avg_redis:.3f}ms - Best for real-time state")
        print(f"✅ PostgreSQL (relational): {avg_postgres:.3f}ms - Best for persistent data")
        print(f"✅ Cassandra (distributed): {avg_cassandra:.3f}ms - Best for geo-distributed")
        print()

if __name__ == "__main__":
    benchmark = GameDataBenchmark()
    results = benchmark.run_benchmark(1000)
    benchmark.print_results(results)
