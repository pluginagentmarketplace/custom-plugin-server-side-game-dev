#!/usr/bin/env python3
"""
Game Server Metrics Collection & Monitoring
Demonstrates key metrics for production game servers
"""

import time
import random
from typing import Dict, List
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class ServerMetrics:
    """Game server metrics snapshot"""
    timestamp: str
    cpu_usage: float        # 0-100 %
    memory_usage: float     # 0-100 %
    active_players: int
    tps: float              # Ticks per second
    avg_latency: float      # ms
    p99_latency: float      # ms
    error_rate: float       # % of requests
    match_count: int
    avg_players_per_match: float
    gc_pause_time: float    # ms

class GameServerMonitor:
    """Collect and analyze game server metrics"""

    def __init__(self):
        self.metrics_history: List[ServerMetrics] = []

    def collect_metrics(self) -> ServerMetrics:
        """Collect current metrics from game server"""
        # In production, these would come from actual instrumentation
        metrics = ServerMetrics(
            timestamp=datetime.now().isoformat(),
            cpu_usage=random.uniform(20, 80),
            memory_usage=random.uniform(30, 85),
            active_players=random.randint(100, 500),
            tps=random.uniform(58, 62),  # Should be 60 for 60 Hz tick
            avg_latency=random.uniform(10, 50),
            p99_latency=random.uniform(50, 200),
            error_rate=random.uniform(0.001, 0.05),
            match_count=random.randint(5, 20),
            avg_players_per_match=8.5,
            gc_pause_time=random.uniform(5, 30)
        )
        self.metrics_history.append(metrics)
        return metrics

    def check_health(self, metrics: ServerMetrics) -> Dict[str, str]:
        """Perform health checks against SLOs"""
        alerts = {}

        # CPU alert
        if metrics.cpu_usage > 80:
            alerts['cpu'] = f"HIGH: {metrics.cpu_usage:.1f}%"
        elif metrics.cpu_usage > 90:
            alerts['cpu'] = f"CRITICAL: {metrics.cpu_usage:.1f}%"

        # Memory alert
        if metrics.memory_usage > 85:
            alerts['memory'] = f"HIGH: {metrics.memory_usage:.1f}%"
        elif metrics.memory_usage > 95:
            alerts['memory'] = f"CRITICAL: {metrics.memory_usage:.1f}%"

        # Latency alert
        if metrics.p99_latency > 200:
            alerts['latency'] = f"HIGH P99: {metrics.p99_latency:.0f}ms"
        elif metrics.p99_latency > 500:
            alerts['latency'] = f"CRITICAL P99: {metrics.p99_latency:.0f}ms"

        # TPS alert
        if abs(metrics.tps - 60) > 2:
            alerts['tps'] = f"LOW: {metrics.tps:.1f} (target: 60)"

        # Error rate alert
        if metrics.error_rate > 0.01:
            alerts['errors'] = f"HIGH: {metrics.error_rate:.3%}"
        elif metrics.error_rate > 0.05:
            alerts['errors'] = f"CRITICAL: {metrics.error_rate:.3%}"

        # GC pause alert
        if metrics.gc_pause_time > 100:
            alerts['gc'] = f"HIGH PAUSE: {metrics.gc_pause_time:.0f}ms"

        return alerts

    def analyze_trends(self) -> Dict[str, float]:
        """Analyze metrics trends"""
        if len(self.metrics_history) < 2:
            return {}

        recent = self.metrics_history[-10:]  # Last 10 samples

        trends = {
            'cpu_avg': sum(m.cpu_usage for m in recent) / len(recent),
            'memory_avg': sum(m.memory_usage for m in recent) / len(recent),
            'latency_avg': sum(m.avg_latency for m in recent) / len(recent),
            'error_rate_avg': sum(m.error_rate for m in recent) / len(recent),
        }

        # Calculate slopes (trend direction)
        if len(recent) >= 2:
            cpu_first = recent[0].cpu_usage
            cpu_last = recent[-1].cpu_usage
            trends['cpu_trend'] = cpu_last - cpu_first

            mem_first = recent[0].memory_usage
            mem_last = recent[-1].memory_usage
            trends['memory_trend'] = mem_last - mem_first

        return trends

    def print_metrics(self, metrics: ServerMetrics):
        """Print metrics in human-readable format"""
        print("\n" + "=" * 70)
        print(f"Game Server Metrics - {metrics.timestamp}")
        print("=" * 70)

        print("\n🖥️  SYSTEM RESOURCES")
        print("-" * 70)
        print(f"  CPU Usage:         {metrics.cpu_usage:6.1f}%")
        print(f"  Memory Usage:      {metrics.memory_usage:6.1f}%")
        print(f"  GC Pause Time:     {metrics.gc_pause_time:6.1f} ms")

        print("\n👥 PLAYER & GAME METRICS")
        print("-" * 70)
        print(f"  Active Players:    {metrics.active_players:6} players")
        print(f"  Match Count:       {metrics.match_count:6} matches")
        print(f"  Avg Players/Match: {metrics.avg_players_per_match:6.1f} players")

        print("\n⏱️  PERFORMANCE METRICS")
        print("-" * 70)
        print(f"  Server TPS:        {metrics.tps:6.1f} ticks/sec (target: 60)")
        print(f"  Avg Latency:       {metrics.avg_latency:6.1f} ms")
        print(f"  P99 Latency:       {metrics.p99_latency:6.1f} ms")
        print(f"  Error Rate:        {metrics.error_rate:6.3%}")

    def print_health_status(self, alerts: Dict[str, str]):
        """Print health check results"""
        print("\n🏥 HEALTH CHECK")
        print("-" * 70)

        if not alerts:
            print("  ✅ All systems healthy!")
        else:
            for system, message in alerts.items():
                print(f"  ⚠️  {system.upper()}: {message}")

    def print_summary(self):
        """Print collection summary"""
        if not self.metrics_history:
            return

        print("\n📊 COLLECTION SUMMARY")
        print("-" * 70)
        print(f"  Samples collected: {len(self.metrics_history)}")
        print(f"  Time span: {self.metrics_history[0].timestamp} to {self.metrics_history[-1].timestamp}")

        # Calculate statistics
        players = [m.active_players for m in self.metrics_history]
        latencies = [m.avg_latency for m in self.metrics_history]

        print(f"  Player range: {min(players)} - {max(players)}")
        print(f"  Latency range: {min(latencies):.1f}ms - {max(latencies):.1f}ms")

class AlertSystem:
    """Alert severity and routing"""

    SEVERITY = {
        'INFO': 0,
        'WARNING': 1,
        'CRITICAL': 2,
    }

    @staticmethod
    def determine_severity(alerts: Dict[str, str]) -> str:
        """Determine alert severity"""
        if not alerts:
            return 'INFO'

        has_critical = any('CRITICAL' in v for v in alerts.values())
        if has_critical:
            return 'CRITICAL'

        return 'WARNING'

    @staticmethod
    def route_alert(severity: str, alerts: Dict[str, str]):
        """Route alert to appropriate channel"""
        print(f"\n🚨 ALERT [{severity}]")
        if severity == 'CRITICAL':
            print("   → Paging on-call engineer")
            print("   → Posting to #incidents Slack channel")
        elif severity == 'WARNING':
            print("   → Logging to monitoring dashboard")
            print("   → Email to team")

if __name__ == "__main__":
    # Create monitor
    monitor = GameServerMonitor()

    print("Game Server Monitoring System")
    print("=" * 70)

    # Collect metrics over time
    print("\nCollecting metrics for 5 samples...")
    for i in range(5):
        metrics = monitor.collect_metrics()
        monitor.print_metrics(metrics)

        # Check health
        alerts = monitor.check_health(metrics)
        monitor.print_health_status(alerts)

        # Route alerts
        severity = AlertSystem.determine_severity(alerts)
        if alerts:
            AlertSystem.route_alert(severity, alerts)

        time.sleep(0.5)

    # Print trends
    trends = monitor.analyze_trends()
    print("\n📈 TREND ANALYSIS")
    print("-" * 70)
    for metric, value in trends.items():
        print(f"  {metric:20} {value:8.2f}")

    monitor.print_summary()
