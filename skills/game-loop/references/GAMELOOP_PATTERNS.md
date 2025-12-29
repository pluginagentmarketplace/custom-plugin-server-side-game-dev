# Game Loop Architecture Patterns

## Fixed Timestep Loop (Recommended for Multiplayer)

```python
accumulator = 0
dt = 1/60  # Fixed 60 FPS timestep

while running:
    elapsed = time.since_last_frame()

    # Cap elapsed time (prevent spiral of death)
    if elapsed > 0.25:
        elapsed = 0.25

    accumulator += elapsed

    # Fixed timestep update
    while accumulator >= dt:
        update(dt)
        accumulator -= dt

    # Interpolate between frames
    alpha = accumulator / dt
    render(alpha)
```

**Advantages:**
- ✅ Deterministic physics
- ✅ Network synchronization consistency
- ✅ Replay-able gameplay
- ✅ Independent of frame rate

**Disadvantages:**
- ⚠️ May need multiple updates per frame
- ⚠️ Potential caught-up state (lag)

## Variable Timestep Loop (Simple, Not Recommended for Online)

```python
while running:
    dt = time.since_last_frame()
    update(dt)
    render()
```

**Disadvantages for Multiplayer:**
- ❌ Non-deterministic due to varying dt
- ❌ Network desyncs likely
- ❌ Players see different results

## Triple-Buffer Rendering

```
Frame N:       Calculate         Calculate         Calculate
               Physics           Input             Output
               ↓                 ↓                 ↓
Frame Buffers: Back              Middle            Front
               ↓                 ↓                 ↓
               Update            Render            Display
```

## Update-Render Separation

### Update Frequency vs Render Frequency
```
Game State:    Update at 60 Hz (dt = 16.67ms)
Rendering:     Render at 144 Hz (or more)
Result:        Smooth visuals + deterministic state
```

### Implementation
```cpp
// Game thread (fixed 60 Hz)
while(game_running) {
    for(auto& object : objects) {
        object.update(DT);
    }
    render_queue.push(snapshot);
}

// Render thread (variable frame rate)
while(render_running) {
    snapshot = render_queue.pop();
    display.render(snapshot);
}
```

## Lag Compensation

### Server-Authoritative State
```
Client sends: Input command + timestamp
Server:       Apply, calculate new state
Network:      Send state + server time
Client:       Interpolate to server time + lag
```

### Extrapolation vs Interpolation
```
Interpolation:  Use past positions (safe, smooth)
              pos = lerp(old_pos, current_pos, alpha)

Extrapolation:  Predict future (low latency, risky)
              pos = current_pos + velocity * predicted_dt
```

## Physics Integration Methods

### Explicit Euler (Simplest)
```
v += a * dt
x += v * dt
```
- Fast
- Less stable
- Good for games

### Semi-Implicit Euler (Better)
```
v += a * dt
x += v * dt  // Uses updated velocity
```
- Still fast
- More stable
- Better energy conservation

### RK4 (Most Accurate)
```
k1 = f(t, x)
k2 = f(t + dt/2, x + dt*k1/2)
k3 = f(t + dt/2, x + dt*k2/2)
k4 = f(t + dt, x + dt*k3)

x = x + (k1 + 2*k2 + 2*k3 + k4) * dt/6
```
- Most accurate
- More expensive
- For critical simulations

## Determinism Challenges

### Non-Deterministic Sources
❌ Floating point precision differences
❌ Threading/random order execution
❌ External timing sources
❌ Uninitialized memory

### Ensuring Determinism
✅ Fixed timestep
✅ Deterministic physics (no random drift)
✅ Consistent seeding for RNG
✅ Single-threaded update (or careful sync)

### Replication Test
```python
def test_determinism():
    # Run A
    game_a = GameState()
    for input in input_sequence:
        game_a.update(input, DT)

    # Run B (same input)
    game_b = GameState()
    for input in input_sequence:
        game_b.update(input, DT)

    # Should match exactly
    assert game_a.state == game_b.state
```

## Frame Rate Decoupling

### Problem
```
60 Hz Game Loop + 144 Hz Render
= Stuttering on frame syncs
```

### Solution
```
Game State:       Update 60 Hz (tick-based)
Render Thread:    Read last snapshot
Interpolation:    Smooth between snapshots

Result: 144+ FPS rendering without state desync
```

### Implementation Pattern
```cpp
struct GameSnapshot {
    timestamp_t server_time;
    position_t objects[MAX_OBJECTS];
    rotation_t rotations[MAX_OBJECTS];
};

// Game thread
while(running) {
    update_game_logic();
    snapshots[next_index] = capture_snapshot();
    next_index = (next_index + 1) % 3;
}

// Render thread
while(rendering) {
    snapshot1 = snapshots[index-1];
    snapshot2 = snapshots[index];
    alpha = (current_time - snapshot1.time) / DT;

    for(object : objects) {
        interpolated = lerp(snapshot1[obj], snapshot2[obj], alpha);
        render(interpolated);
    }
}
```

## Maximum Delta Time

```
Problem: Frame stutter → huge dt → physics breaks

Solution: Cap dt!
    dt_actual = min(dt_measured, dt_max)

Common values:
    dt_max = 0.25s  (assume 4 FPS minimum)
    dt_max = 0.1s   (more aggressive)
```

## Anti-patterns

❌ **Unlimited Delta Time**: Causes huge jumps
❌ **Single-threaded with blocking I/O**: Stalls updates
❌ **Floating-point arithmetic for comparisons**: Desyncs
❌ **Update after render**: One frame input lag
❌ **No network lag compensation**: Rubber-banding
