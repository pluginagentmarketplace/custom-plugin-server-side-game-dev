# State Synchronization Patterns for Multiplayer Games

## The Synchronization Triangle

```
        Client
         /  \
        /    \
  Prediction  Reconciliation
      /        \
     /          \
    Server ← Authority
```

## Client-Side Prediction (Optimistic Updates)

### How It Works
```
1. Local Input → Apply immediately
2. Send to server (with latency)
3. Server validates
4. Server responds
5. Reconcile if error

Result: Instant feedback, then correctness
```

### Implementation
```cpp
// Client
local_position += input_velocity * dt;  // Instant
render(local_position);

// Send to server
server.SendInput(input, current_time);

// Server validates
validated_position = ApplyInput(input);

// Server responds
client.ReceiveState(validated_position);

// Reconcile
if (distance(local_position, validated_position) > threshold) {
    local_position = validated_position;  // Snap or lerp
}
```

### Advantages
✅ Feels responsive (0ms apparent latency)
✅ Better player experience
✅ Smooth movement

### Disadvantages
⚠️ Potential desync if prediction wrong
⚠️ Network bandwidth for validation
⚠️ Complexity in implementation

## Server Reconciliation

### Re-simulation Approach
```
Server keeps input history:
  [Input 1] → [Input 2] → [Input 3] → [Input 4]
   (t=0)      (t=16ms)    (t=32ms)    (t=48ms)

When correction needed:
  1. Start from last known good state
  2. Replay all inputs from then
  3. Compare client prediction with result
  4. Send correction if different
```

### Timeline Correction
```
Client thinks:     0ms
Server says:      -20ms (was 20ms ago)
Client corrects:   Teleport back 20ms worth

Better: Smoothly lerp back to correct position
```

## Lag Compensation

### Problem
```
A shoots at B
B was here on A's screen
But B moved during network latency
Server-side hitbox at B's NEW position
→ A's shot misses unfairly!
```

### Solution: Rewind State
```
1. Record all player positions over time
2. When A shoots, look back N milliseconds
3. Where was B at that time?
4. Use THAT position for hitbox

Result: Fair aiming despite lag
```

### Implementation
```python
class PlayerStateBuffer:
    def __init__(self, buffer_time=500):  # 500ms history
        self.states = []  # (timestamp, position, rotation)

    def record(self, timestamp, position, rotation):
        self.states.append((timestamp, position, rotation))
        self.cleanup()

    def cleanup(self):
        # Remove states older than buffer_time
        cutoff = time.now() - self.buffer_time
        self.states = [s for s in self.states if s[0] > cutoff]

    def get_at_time(self, timestamp):
        # Find closest state to requested time
        # Could interpolate between states
        best = min(self.states, key=lambda s: abs(s[0] - timestamp))
        return best[1]  # position
```

### Benefits
✅ Fair for all players (same lag = same fairness)
✅ Eliminates "I shot them!"
✅ Skill-based (not luck-based)

## Interpolation vs Extrapolation

### Interpolation (Safe)
```
Use: Last two server updates
Time: Current - Network latency
Benefit: Accurate, smooth

visual_pos = lerp(old_pos, new_pos, alpha)

Where alpha goes 0→1 during time between updates
```

### Extrapolation (Fast but Risky)
```
Use: Velocity from last update
Time: Predict where player is going
Benefit: Lower apparent latency

predicted_pos = last_pos + velocity * predicted_time
```

### Comparison
```
Latency: 50ms
Update frequency: 60 Hz (16ms per frame)

Interpolation:
  ✅ Position accurate
  ✅ Smooth motion
  ❌ 50ms behind reality

Extrapolation:
  ✅ Feels more responsive
  ⚠️ Can predict wrong
  ❌ Rubber-banding if wrong
```

## Delta Compression

### Problem
```
Send full state each frame:
  Position (12 bytes)
  Rotation (8 bytes)
  Health (2 bytes)
  Velocity (12 bytes)
  = 34 bytes per player × 100 players = 3.4 KB/frame
  = 204 KB/sec at 60 Hz
  = Too much bandwidth!
```

### Solution: Send Only Changes
```
Full state every 100 frames (1.6 seconds)
Delta updates every other frame:
  Changed fields only
  1-2 bytes per field per update

Result: 10-20 bytes per player per frame
       = 1-2 KB per frame with 100 players
       = 60-120 KB/sec (10x reduction!)
```

### Implementation
```cpp
struct PlayerDelta {
    uint16_t changed_flags;  // Bit flags: pos=1, rot=2, health=4
    // Only include fields indicated by flags
    if (changed_flags & POS_CHANGED) {
        position = read_vec3();
    }
    if (changed_flags & ROT_CHANGED) {
        rotation = read_quat();
    }
}
```

## Entity Interpolation

### Smooth Movement Despite Updates
```
Server Update Rate:  20 Hz (50ms)
Render Rate:         60 Hz (16ms)

Frame 0:    Receive pos1 at t=0ms      → Render pos1
Frame 1:    Render pos1 + interp       → Render ~20% pos2
Frame 2:    Render pos1 + interp       → Render ~40% pos2
Frame 3:    Receive pos2 at t=50ms     → Render ~60% pos2
Frame 4:    Render pos2 + interp       → Render ~80% pos2

Result: Smooth motion even with low update rate
```

## Dead Reckoning (Extrapolation Enhancement)

### Include Velocity in Updates
```
Server sends:
  Position
  Velocity
  Acceleration (optional)

Client extrapolates:
  next_pos = current_pos + velocity * dt
  next_vel = current_vel + accel * dt
```

### Benefits
```
✅ Can render at any frame rate
✅ Smooth motion between updates
⚠️ Can diverge if physics changes unpredictably
```

## Network Protocol Design for Sync

### Packet Types
```
1. INITIAL_STATE: Full snapshot (0.5 KB)
2. DELTA_UPDATE: Only changed fields (20-50 bytes)
3. CORRECTION: "You're wrong, here's the truth" (100+ bytes)
4. ACK: "Got your update" (4 bytes)
```

### Update Frequency Guidelines
```
Real-time (shooting):     60 Hz (16ms)
  ↓ Network constraint
Practical (UDP):          30-60 Hz
Practical (Throttled):    20-30 Hz
Turn-based:              As needed (1-5 Hz)
```

## Handling Disconnects & Rejoin

### State on Disconnect
```
Option 1: Freeze
  ✅ Simple
  ❌ Unfair (can't fight back)

Option 2: Predict
  ⚠️ Better but inaccurate
  ❌ Can rubber-band badly

Option 3: Remove
  ✅ Fair
  ⚠️ Harsh (lose progress)
```

### Rejoin Protocol
```
Client disconnects (N ms)
  ↓
Request full state snapshot
  ↓
Server sends complete state
  ↓
Client fast-forwards to current time
  ↓
Resume normal sync

Avoid: Sending all missed deltas (too many!)
```

## Anti-patterns

❌ **No prediction**: Feels laggy
✅ **Do**: Client-side prediction

❌ **Trusting client completely**: Cheating
✅ **Do**: Server validates all critical state

❌ **Sending full state every frame**: Bandwidth waste
✅ **Do**: Delta compression

❌ **Same update rate as render**: Causes stuttering
✅ **Do**: Decouple update/render rates

❌ **No lag compensation**: Unfair gameplay
✅ **Do**: Rewind for hitbox calculations

❌ **Extrapolation for position**: Rubber-banding
✅ **Do**: Use interpolation for smooth visuals
