#!/usr/bin/env python3
"""
Fixed Timestep Game Loop Simulator
Demonstrates deterministic game loop with fixed delta time
"""

import time
import math
from typing import List, Tuple

class GameObject:
    """Simple game object with physics"""
    def __init__(self, x: float, y: float, vx: float = 0, vy: float = 0):
        self.x = x
        self.y = y
        self.vx = vx  # velocity x
        self.vy = vy  # velocity y
        self.ax = 0   # acceleration x
        self.ay = -9.8  # gravity

    def update(self, dt: float):
        """Update position using velocity (explicit Euler)"""
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def position(self) -> Tuple[float, float]:
        return (self.x, self.y)

class GameLoop:
    """Fixed timestep game loop"""

    def __init__(self, target_fps: int = 60):
        self.target_fps = target_fps
        self.dt = 1.0 / target_fps  # Fixed delta time
        self.accumulator = 0.0
        self.frame_count = 0
        self.total_time = 0.0

        # Game objects
        self.objects: List[GameObject] = []

    def add_object(self, obj: GameObject):
        """Add object to game world"""
        self.objects.append(obj)

    def update(self, dt: float):
        """Single physics update step"""
        for obj in self.objects:
            obj.update(self.dt)

    def render(self):
        """Simulate rendering (would draw to screen)"""
        pass  # In real game, draw frame

    def run(self, duration: float = 1.0):
        """Run game loop for specified duration"""
        start_time = time.time()
        frame_times = []

        while self.total_time < duration:
            frame_start = time.time()

            # Get elapsed time since last frame
            current_time = time.time()
            elapsed = current_time - start_time - self.total_time

            # Cap elapsed time (prevent spiral of death)
            if elapsed > 0.25:  # Max 250ms (prevent lag spikes)
                elapsed = 0.25

            self.accumulator += elapsed
            self.total_time += elapsed

            # Fixed timestep update loop
            while self.accumulator >= self.dt:
                self.update(self.dt)
                self.accumulator -= self.dt

            # Interpolation factor (0.0 to 1.0)
            alpha = self.accumulator / self.dt

            # Render (would use alpha for interpolation)
            self.render()

            self.frame_count += 1

            # Frame time measurement
            frame_end = time.time()
            frame_time = (frame_end - frame_start) * 1000  # Convert to ms
            frame_times.append(frame_time)

            # Sync to target FPS (if we're running too fast)
            sleep_time = self.dt - (frame_end - frame_start)
            if sleep_time > 0:
                time.sleep(sleep_time)

        return frame_times

    def print_stats(self, frame_times: List[float]):
        """Print performance statistics"""
        if not frame_times:
            return

        avg_frame_time = sum(frame_times) / len(frame_times)
        actual_fps = 1000.0 / avg_frame_time if avg_frame_time > 0 else 0

        sorted_times = sorted(frame_times)
        p95_time = sorted_times[int(len(sorted_times) * 0.95)]
        p99_time = sorted_times[int(len(sorted_times) * 0.99)]
        max_time = max(frame_times)

        print("\n" + "=" * 60)
        print("GAME LOOP PERFORMANCE METRICS")
        print("=" * 60)
        print(f"Target FPS:          {self.target_fps}")
        print(f"Actual FPS:          {actual_fps:.1f}")
        print(f"Total Frames:        {self.frame_count}")
        print()
        print(f"Avg Frame Time:      {avg_frame_time:.3f} ms")
        print(f"P95 Frame Time:      {p95_time:.3f} ms")
        print(f"P99 Frame Time:      {p99_time:.3f} ms")
        print(f"Max Frame Time:      {max_time:.3f} ms")
        print()

        # Dropped frames calculation
        dropped = sum(1 for t in frame_times if t > self.dt * 1000)
        drop_rate = (dropped / len(frame_times)) * 100 if frame_times else 0
        print(f"Dropped Frames:      {dropped} ({drop_rate:.1f}%)")
        print("=" * 60)

class DeterminismTest:
    """Test deterministic game loop"""

    def test_same_state(self):
        """Verify same input produces same output"""
        # Run 1
        loop1 = GameLoop(target_fps=60)
        loop1.add_object(GameObject(0, 100, 10, 0))
        times1 = loop1.run(0.5)

        # Run 2 (identical setup)
        loop2 = GameLoop(target_fps=60)
        loop2.add_object(GameObject(0, 100, 10, 0))
        times2 = loop2.run(0.5)

        # Both should reach same final position (deterministic)
        final1 = loop1.objects[0].position()
        final2 = loop2.objects[0].position()

        print(f"\nDeterminism Test:")
        print(f"  Final position 1: {final1}")
        print(f"  Final position 2: {final2}")
        print(f"  Match: {abs(final1[0] - final2[0]) < 0.001}")

if __name__ == "__main__":
    # Create game loop
    loop = GameLoop(target_fps=60)

    # Add some game objects
    loop.add_object(GameObject(0, 100, 5, 0))      # Object moving right
    loop.add_object(GameObject(50, 50, -5, 0))     # Object moving left
    loop.add_object(GameObject(25, 200, 0, 0))     # Object falling

    print("Running game loop for 1 second...")
    frame_times = loop.run(duration=1.0)

    loop.print_stats(frame_times)

    # Test determinism
    test = DeterminismTest()
    test.test_same_state()
