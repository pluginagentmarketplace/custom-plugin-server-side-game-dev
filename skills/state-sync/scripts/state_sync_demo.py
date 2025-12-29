#!/usr/bin/env python3
"""
State Synchronization Demo
Demonstrates client-side prediction, server reconciliation, and lag compensation
"""

import time
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class PlayerState:
    """Player game state"""
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    timestamp: float
    is_local: bool

class StateSync:
    """Handle state synchronization between client and server"""

    def __init__(self, network_latency_ms: float = 50):
        self.network_latency = network_latency_ms / 1000  # Convert to seconds
        self.client_state: PlayerState = None
        self.server_state: PlayerState = None
        self.last_acked_state: PlayerState = None

    def client_update(self, input_velocity: Tuple[float, float], dt: float):
        """Update client state with local input (client-side prediction)"""
        x, y = self.client_state.position
        vx, vy = input_velocity

        # Client applies input immediately (optimistic)
        new_x = x + vx * dt
        new_y = y + vy * dt

        self.client_state = PlayerState(
            position=(new_x, new_y),
            velocity=input_velocity,
            timestamp=time.time(),
            is_local=True
        )

    def send_to_server(self, input_velocity: Tuple[float, float]) -> PlayerState:
        """Send input to server (with latency)"""
        # Simulate network latency
        time.sleep(self.network_latency)

        # Server receives and applies
        server_state = PlayerState(
            position=self.client_state.position,
            velocity=input_velocity,
            timestamp=time.time(),
            is_local=False
        )

        return server_state

    def server_reconcile(self, server_state: PlayerState):
        """Server sends authoritative state back to client"""
        # Simulate round-trip latency
        time.sleep(self.network_latency * 2)

        # Check if client prediction matches server
        error = self.calculate_error(self.client_state, server_state)
        return server_state, error

    def calculate_error(self, predicted: PlayerState, actual: PlayerState) -> float:
        """Calculate prediction error"""
        px, py = predicted.position
        ax, ay = actual.position

        distance = ((px - ax) ** 2 + (py - ay) ** 2) ** 0.5
        return distance

class LagCompensation:
    """Compensate for network lag"""

    def __init__(self, latency_ms: float = 100):
        self.latency = latency_ms / 1000
        self.state_buffer: List[Tuple[float, PlayerState]] = []

    def record_state(self, timestamp: float, state: PlayerState):
        """Record historical state"""
        self.state_buffer.append((timestamp, state))

        # Keep only last 1 second of states
        cutoff = timestamp - 1.0
        self.state_buffer = [(t, s) for t, s in self.state_buffer if t > cutoff]

    def get_lag_compensated_state(self, current_time: float) -> PlayerState:
        """Get state from N milliseconds ago (where opponent was)"""
        target_time = current_time - self.latency

        # Find closest state
        best_state = None
        best_distance = float('inf')

        for timestamp, state in self.state_buffer:
            distance = abs(timestamp - target_time)
            if distance < best_distance:
                best_distance = distance
                best_state = state

        return best_state if best_state else self.state_buffer[-1][1]

class InterpolationDemo:
    """Demonstrate interpolation between frames"""

    @staticmethod
    def linear_interpolation(state1: PlayerState, state2: PlayerState, alpha: float):
        """Interpolate between two states"""
        x1, y1 = state1.position
        x2, y2 = state2.position

        # Alpha: 0 = state1, 1 = state2
        x = x1 + (x2 - x1) * alpha
        y = y1 + (y2 - y1) * alpha

        return (x, y)

    @staticmethod
    def extrapolate(state: PlayerState, dt: float):
        """Predict next position based on velocity"""
        x, y = state.position
        vx, vy = state.velocity

        new_x = x + vx * dt
        new_y = y + vy * dt

        return (new_x, new_y)

def simulate_multiplayer_sync():
    """Simulate client-server state synchronization"""

    print("=" * 70)
    print("STATE SYNCHRONIZATION DEMONSTRATION")
    print("=" * 70)
    print()

    # Setup
    latency_ms = 50
    sync = StateSync(network_latency_ms=latency_ms)

    # Initial state
    sync.client_state = PlayerState(
        position=(0, 0),
        velocity=(10, 0),
        timestamp=time.time(),
        is_local=True
    )

    print(f"Network Latency: {latency_ms}ms (one-way)")
    print()

    # Simulate 3 frames
    print("FRAME-BY-FRAME SIMULATION")
    print("-" * 70)

    for frame in range(1, 4):
        print(f"\nFrame {frame}:")
        print(f"  Client (predicted): {sync.client_state.position}")

        # Client sends input
        print(f"  → Sending to server...")
        server_response = sync.send_to_server((10, 0))

        # Server processes and responds
        server_state, error = sync.server_reconcile(server_response)
        print(f"  ← Server response: {server_state.position}")
        print(f"  Prediction error: {error:.4f} units")

        # Small delay for next frame
        time.sleep(0.05)

    print()
    print("=" * 70)
    print("LAG COMPENSATION DEMONSTRATION")
    print("=" * 70)
    print()

    # Record several states
    lag_comp = LagCompensation(latency_ms=50)

    print("Recording player positions over time...")
    current_time = time.time()

    # Simulate recording states
    for i in range(10):
        state = PlayerState(
            position=(i * 10, 0),
            velocity=(10, 0),
            timestamp=current_time + (i * 0.016),  # 60 Hz
            is_local=False
        )
        lag_comp.record_state(state.timestamp, state)

    print(f"Recorded {len(lag_comp.state_buffer)} states")
    print()

    # Get lag-compensated state
    lag_comp_state = lag_comp.get_lag_compensated_state(current_time + 0.15)
    latest_state = lag_comp.state_buffer[-1][1]

    print(f"Latest opponent position:        {latest_state.position}")
    print(f"Lag-compensated position (50ms): {lag_comp_state.position}")
    print()

    print("=" * 70)
    print("INTERPOLATION DEMONSTRATION")
    print("=" * 70)
    print()

    state1 = PlayerState(position=(0, 0), velocity=(10, 0), timestamp=0, is_local=True)
    state2 = PlayerState(position=(10, 0), velocity=(10, 0), timestamp=0.016, is_local=True)

    print("Rendering between two server updates:")
    print(f"State 1: {state1.position}")
    print(f"State 2: {state2.position}")
    print()

    for frame in range(0, 17):
        alpha = frame / 16  # 0.0 to 1.0
        interpolated_pos = InterpolationDemo.linear_interpolation(state1, state2, alpha)
        print(f"Frame {frame:2d} (α={alpha:.2f}): Render at {interpolated_pos}")

    print()
    print("✅ Summary:")
    print("  ✓ Client-side prediction: Feel responsive")
    print("  ✓ Server reconciliation: Maintain accuracy")
    print("  ✓ Lag compensation: Fair hitboxes")
    print("  ✓ Interpolation: Smooth visuals")

if __name__ == "__main__":
    simulate_multiplayer_sync()
