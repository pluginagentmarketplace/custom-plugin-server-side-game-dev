# Game Server Databases Guide

## Database Selection Matrix

| Feature | Redis | PostgreSQL | Cassandra | MongoDB |
|---------|-------|-----------|-----------|---------|
| **Speed** | ⚡⚡⚡ | ⚡⚡ | ⚡⚡ | ⚡⚡ |
| **Persistence** | ❌ | ✅ | ✅ | ✅ |
| **Horizontal Scale** | ❌ | ⚠️ | ✅ | ✅ |
| **Real-time Data** | ✅ | ❌ | ⚠️ | ❌ |
| **Transactions** | ❌ | ✅ | ❌ | ✅ |
| **Player State** | 🏆 | ❌ | ⚠️ | ❌ |
| **Persistent Data** | ❌ | 🏆 | ⚠️ | 🏆 |
| **Geo-distributed** | ❌ | ❌ | 🏆 | ✅ |

## Use Cases

### Redis (In-Memory)
```
Best For: Real-time player state, leaderboards, sessions
Typical Use:
  - Current player position updates
  - Active player sessions
  - Match state during gameplay
  - Leaderboard rankings
  - Game cache layer

Latency: <5ms average
Throughput: 100k+ ops/sec
```

### PostgreSQL (Relational)
```
Best For: Persistent player data, accounts, transactions
Typical Use:
  - Player account data
  - Game progress/achievements
  - Inventory (with proper serialization)
  - Match history
  - Game economy (credits, items)

Latency: 5-20ms average
Throughput: 10k-50k ops/sec
```

### Cassandra (Distributed)
```
Best For: Large-scale distributed systems, time-series data
Typical Use:
  - Player analytics
  - Match telemetry
  - Global leaderboards
  - User behavior tracking
  - Geo-distributed player data

Latency: 10-50ms average
Throughput: 100k+ ops/sec
```

## Architecture Pattern: Lambda

```
┌─────────────────┐
│   GAME CLIENT   │
└────────┬────────┘
         │
    ┌────▼──────────────┐
    │  GAME SERVER      │
    │  (Authoritative)  │
    └────┬──────────────┘
         │
    ┌────▼─────────────────────────┐
    │    DATA LAYER ROUTING        │
    ├──────────────────────────────┤
    │ Real-time? → Redis           │
    │ Persistent? → PostgreSQL      │
    │ Analytics? → Cassandra        │
    └──────────────────────────────┘
```

## Connection Pooling

### Redis Pool
```python
# Recommended: 10-20 connections per server
pool_size = 20
max_overflow = 10
```

### PostgreSQL Pool
```python
# Recommended: 5-10 connections
pool_size = 10
max_overflow = 5
```

### Cassandra Cluster
```python
# Recommended: 100-200 connections
contact_points = ['node1', 'node2', 'node3']
num_connections = 150
```

## Data Consistency Considerations

### Eventual Consistency (Redis)
- ✅ High performance
- ✅ Low latency
- ❌ Possible data loss on crash
- Solution: Backup to PostgreSQL periodically

### Strong Consistency (PostgreSQL)
- ✅ Data guarantee
- ✅ ACID transactions
- ❌ Higher latency
- Solution: Use for critical data only

### Tunable Consistency (Cassandra)
- ✅ Trade-off control
- ✅ Distributed
- ❌ Operational complexity
- Solution: Use QUORUM for critical, ONE for real-time

## Backup & Recovery Strategy

```
CRITICAL DATA (PostgreSQL)
  ├─ Backups: Daily snapshots
  ├─ Retention: 30 days
  └─ Recovery: Point-in-time possible

OPERATIONAL DATA (Redis)
  ├─ Persistence: RDB snapshots
  ├─ Replication: Active/passive
  └─ Recovery: Can recreate from PostgreSQL

ANALYTICS (Cassandra)
  ├─ Backups: Incremental snapshots
  ├─ Retention: 90 days
  └─ Recovery: Repair via nodetool
```

## Scaling Patterns

### Horizontal Scaling
```
Redis Cluster:     Sharding across nodes
PostgreSQL:        Read replicas + sharding
Cassandra:         Add nodes automatically
```

### Vertical Scaling
```
Redis:    Increase memory
PostgreSQL: Better hardware
Cassandra: More nodes for distribution
```

## Performance Tuning

### Query Optimization
- Index frequently accessed fields
- Denormalize for read-heavy workloads
- Use connection pools efficiently
- Batch operations when possible

### Caching Strategy
```
Cache Layers:
  L1: Application memory (fastest)
  L2: Redis (fast, shared)
  L3: PostgreSQL (persistent)
  L4: Cassandra (distributed)
```

## Game-Specific Patterns

### Player Position Updates
- Store in Redis with 10-second expiry
- Broadcast to nearby players only
- No persistence needed
- Eventual consistency acceptable

### Player Inventory
- Cache in Redis
- Persist in PostgreSQL
- Dual-write pattern during transaction
- Strong consistency required

### Match Statistics
- Write-through to Cassandra
- Aggregate in Redis
- Query from PostgreSQL
- Analytics after match ends

## Anti-patterns to Avoid

❌ **Don't**: Store large objects directly in Redis
✅ **Do**: Serialize to JSON, use compression

❌ **Don't**: Use PostgreSQL for real-time updates
✅ **Do**: Use Redis with PostgreSQL fallback

❌ **Don't**: Ignore connection pool limits
✅ **Do**: Monitor pool utilization, adjust proactively

❌ **Don't**: Store game state only in memory
✅ **Do**: Implement Redis -> PostgreSQL backup cycle
