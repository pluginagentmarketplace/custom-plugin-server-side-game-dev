# Design Patterns for Game Servers

## Essential Patterns

### 1. Observer Pattern (Event System)
```python
class EventManager:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event: str, callback):
        self._listeners.setdefault(event, []).append(callback)

    def emit(self, event: str, data):
        for callback in self._listeners.get(event, []):
            callback(data)
```

### 2. Command Pattern (Input Handling)
- Encapsulate player actions as objects
- Enable undo/redo for turn-based games
- Queue commands for server validation

### 3. State Pattern (Game States)
- Lobby → Loading → Playing → Paused → GameOver
- Clean state transitions
- State-specific behavior

### 4. Object Pool Pattern
- Reuse bullet/particle objects
- Reduce GC pressure
- Pre-allocate common entities

## When to Use

| Pattern | Use Case |
|---------|----------|
| Observer | Events, achievements |
| Command | Player inputs |
| State | Game flow |
| Pool | Projectiles |
