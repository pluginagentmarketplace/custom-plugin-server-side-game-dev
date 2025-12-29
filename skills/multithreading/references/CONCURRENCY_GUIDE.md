# Multithreading Guide for Game Servers

## Thread Models

### 1. Main Thread + Worker Pool
```
Main Thread (Game Loop)
    ├── Network I/O
    ├── State Updates
    └── Worker Pool
        ├── Physics Worker
        ├── AI Worker
        └── Persistence Worker
```

### 2. Actor Model
- Each player/entity is an actor
- Message passing between actors
- No shared state (lock-free)

## Thread Safety Patterns

### Lock-Free Data Structures
```cpp
std::atomic<int> player_count{0};
player_count.fetch_add(1, std::memory_order_relaxed);
```

### Read-Write Locks
```python
import threading
rwlock = threading.RLock()
with rwlock:
    # Critical section
    pass
```

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| Deadlock | Lock ordering |
| Race condition | Atomic operations |
| Priority inversion | Priority inheritance |
| False sharing | Cache-line padding |

## Best Practices

1. **Minimize critical sections**
2. **Use lock-free queues** for message passing
3. **Separate read/write paths**
4. **Profile before optimizing**
