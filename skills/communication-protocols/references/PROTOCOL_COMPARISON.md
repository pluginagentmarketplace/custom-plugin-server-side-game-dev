# Communication Protocol Comparison for Games

## Protocol Selection Guide

| Protocol | Latency | Reliability | Use Case |
|----------|---------|-------------|----------|
| UDP | ~1ms | None | Player positions, shots |
| WebSocket | ~5ms | Full | Chat, inventory, lobby |
| gRPC | ~10ms | Full | Matchmaking, auth |
| HTTP/2 | ~20ms | Full | Leaderboards, shop |

## When to Use What

### UDP (User Datagram Protocol)
- Real-time position updates
- Bullet trajectories
- Voice chat (raw)
- Client prediction data

### WebSocket
- Game state synchronization
- Chat systems
- Lobby management
- Turn-based games

### gRPC
- Server-to-server communication
- Matchmaking services
- Authentication flows
- Microservice calls
