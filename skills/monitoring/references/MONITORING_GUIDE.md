# Game Server Monitoring & Observability Guide

## Four Golden Signals

Metrics to monitor for any backend system:

### 1. Latency
```
Definition:  How long requests take
Target:      P99 < 200ms for game updates
Alert:       P99 > 200ms for 2 consecutive minutes
Example:     Player input → Server → Response

Why it matters:
  - Directly impacts player experience
  - Network + processing + serialization time
  - Most critical metric for games
```

### 2. Traffic
```
Definition:  Requests per second (RPS)
Target:      Depends on game architecture
Alert:       Unusual spike (2x baseline)
Example:     100 players × 20 updates/sec = 2000 RPS

Normal patterns:
  - Daily: peaks during evening hours
  - Weekly: weekends > weekdays
  - Seasonal: holidays > normal days
```

### 3. Errors
```
Definition:  Request failure rate
Target:      < 0.1% (99.9% success)
Alert:       > 1% error rate
Example:     500 errors, timeouts, client errors

Classification:
  4xx errors: Client fault (invalid request)
  5xx errors: Server fault (should be rare)
  Network:    Connection failures
```

### 4. Saturation
```
Definition:  How full the system is
Target:      Stay < 80% capacity
Alert:       > 85% for scaling decision
Example:     CPU: 75%, Memory: 60%, Disk: 40%

Signs of saturation:
  - Increased latency under load
  - Rising error rates
  - GC pause times increasing
  - Queue depths growing
```

## Game-Specific Metrics

### Player Experience Metrics
```
Active Players:       Current concurrent players
Queue Wait Time:      Time to find match (target: 30s)
Latency Percentiles:  P50, P95, P99 (ms)
Disconnect Rate:      Players leaving per hour
Frame Stutter:        Frame time variance
```

### Server Health Metrics
```
TPS (Ticks/Second):   Update frequency (target: 60)
Match Count:          Concurrent matches running
State Sync Time:      Time to sync player state (target: <50ms)
CPU per Player:       Total CPU / player count
Memory per Player:    Total memory / player count
```

### Business Metrics
```
Daily Active Users:   DAU
Session Length:       Average game session duration
Churn Rate:          % players leaving per day
Revenue per User:    ARPU (if applicable)
```

## Monitoring Architecture

### Three Tiers of Monitoring

```
TIER 1: Application Metrics
  └─ Where: In game code
     What: Business logic, player actions
     Tools: StatsD, Micrometer, Prometheus client

TIER 2: System Metrics
  └─ Where: OS level
     What: CPU, memory, disk, network
     Tools: Prometheus Node Exporter, collectd

TIER 3: Infrastructure Metrics
  └─ Where: Cloud provider
     What: Container CPU/memory, network I/O
     Tools: CloudWatch, Datadog, New Relic
```

## Alerting Rules

### SLO (Service Level Objective) Targets
```
Availability:   99.9% (9 hours/month downtime allowed)
Latency P99:    < 200ms
Error Rate:     < 0.5%
Throughput:     >= 1000 RPS
```

### Alert Thresholds
```yaml
alerts:
  - name: HighLatency
    condition: p99_latency > 200ms for 2 minutes
    action: Page on-call

  - name: HighErrorRate
    condition: error_rate > 1% for 5 minutes
    action: Page on-call

  - name: HighCPU
    condition: cpu_usage > 85% for 5 minutes
    action: Trigger auto-scaling

  - name: LowDiskSpace
    condition: disk_free < 10%
    action: Alert ops team

  - name: ServiceDown
    condition: health_check fails for 30 seconds
    action: Page on-call immediately
```

## Logging Strategy

### Log Levels
```
ERROR:    System failures, exceptions (keep logs small)
WARNING:  Unusual conditions, degradation (brief context)
INFO:    Business events, deployments (structured)
DEBUG:   Detailed execution trace (development only)
TRACE:   Line-by-line execution (rare debugging)
```

### Structured Logging Format
```json
{
  "timestamp": "2025-12-28T10:30:45.123Z",
  "level": "INFO",
  "service": "game-server",
  "instance": "gs-prod-01",
  "player_id": "p123456",
  "match_id": "m789012",
  "event": "player_spawned",
  "latency_ms": 45,
  "trace_id": "abc123xyz"
}
```

### Log Aggregation
```
Collect:     Fluentd, Logstash
Store:       Elasticsearch, S3, BigQuery
Query:       Kibana, Splunk, DataDog
Alert:       Alert on error patterns
```

## Tracing & Distributed Tracing

### Request Lifecycle Tracing
```
Player Input
  ├─ Network transmission (5ms)
  ├─ Server receive (1ms)
  ├─ Authentication (3ms)
  ├─ Game logic (15ms)
  │  ├─ Physics update (8ms)
  │  ├─ State update (4ms)
  │  └─ Other (3ms)
  ├─ Serialization (2ms)
  └─ Network send (5ms)
  = Total: 31ms
```

### Trace Instrumentation
```
Tools: Jaeger, DataDog APM, AWS X-Ray

Benefits:
  - Identify slow operations
  - See dependencies between services
  - Correlate with errors
  - Find optimization opportunities
```

## Dashboard Design

### Real-time Operations Dashboard
```
Layout:
  ┌─────────────────────────────────────┐
  │ Status: 🟢 HEALTHY                  │
  ├─────────────────────────────────────┤
  │ Active Players: 487 | Matches: 12   │
  │ CPU: 65% | Memory: 72% | Disk: 45% │
  ├─────────────────────────────────────┤
  │ Latency P99: 85ms | Errors: 0.02%  │
  │ TPS: 59.8 | Queue Wait: 8s          │
  ├─────────────────────────────────────┤
  │ [Metrics Graph]  [Error Timeline]   │
  └─────────────────────────────────────┘
```

### Historical Analysis Dashboard
```
Show:
  - 24 hour trends
  - Peak/off-peak patterns
  - Week-over-week comparison
  - Anomaly detection
  - Correlation between metrics
```

## Performance Baseline

### Establish Baselines
```
Method 1: Synthetic Load Testing
  └─ Run controlled load, measure metrics

Method 2: Profiling Production
  └─ Sample 1% of traffic, analyze patterns

Method 3: Historical Analysis
  └─ Analyze last 30 days of metrics
```

### Example Baselines
```
Metric              | Baseline | Alert    | Critical
─────────────────────────────────────────────────────
CPU per 100 players | 40%      | 70%      | 85%
Memory per 100 pl   | 1.2GB    | 1.8GB    | 2.0GB
P99 Latency         | 50ms     | 150ms    | 250ms
Error Rate          | 0.01%    | 0.5%     | 1.0%
TPS Variance        | ±2 ticks | ±5 ticks | ±10 ticks
```

## Observability Maturity

### Level 1: Blind
```
❌ No monitoring
❌ Issues discovered by players
❌ Mean time to recovery: 4+ hours
```

### Level 2: Metrics
```
✅ Basic CPU/memory graphs
✅ Know when something is wrong
❌ Don't know why
❌ MTTR: 2 hours
```

### Level 3: Logs + Metrics
```
✅ Can correlate metrics with logs
✅ Can root cause issues
⚠️ Manual investigation needed
✅ MTTR: 20 minutes
```

### Level 4: Distributed Tracing
```
✅ See request flow end-to-end
✅ Instant root cause identification
✅ Automatic anomaly detection
✅ MTTR: 2 minutes
```

## Cost Optimization

### Sampling Strategy
```
Development:    100% sample (all events)
Staging:        50% sample (balance cost/visibility)
Production:     5% sample (normal traffic)
                100% sample (errors only)
```

### Retention Policy
```
Real-time dashboards:   5 minutes (high granularity)
Recent metrics:         7 days (granular)
Historical:            90 days (hourly aggregation)
Archive:               1 year (daily aggregation)
```

## Anti-patterns

❌ **Monitoring every variable**: Creates noise
✅ **Do**: Monitor golden signals + game-specific metrics

❌ **Alerting on every metric**: Alert fatigue
✅ **Do**: Alert only on actionable issues

❌ **Logs without context**: Hard to debug
✅ **Do**: Structured logs with trace IDs

❌ **No SLOs defined**: Unclear what's healthy
✅ **Do**: Define SLOs, monitor against them

❌ **Storing all logs forever**: Expensive
✅ **Do**: Implement retention policy
