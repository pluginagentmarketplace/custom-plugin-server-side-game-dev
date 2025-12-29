# Game Server Deployment Guide

## Deployment Pipeline Stages

```
DEVELOPMENT → STAGING → CANARY → PRODUCTION
    ↓           ↓          ↓         ↓
  Local      Docker    1% Traffic  100% Traffic
  Tests      Tests     Monitor      Monitor
```

## Docker Deployment

### Build Multi-stage Image
```dockerfile
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o gameserver .

FROM alpine:latest
RUN apk add --no-cache ca-certificates
COPY --from=builder /app/gameserver /usr/local/bin/
HEALTHCHECK --interval=10s CMD gameserver-health
ENTRYPOINT ["gameserver"]
```

### Image Size Optimization
| Stage | Size | Technique |
|-------|------|-----------|
| **Initial** | 1.2GB | Full Go SDK |
| **Multi-stage** | 250MB | Builder pattern |
| **Alpine** | 50MB | Minimal base |
| **Distroless** | 25MB | No shell/package mgr |

## Kubernetes Deployment

### StatefulSet for Game Servers
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: game-server
spec:
  serviceName: game-server
  replicas: 10
  selector:
    matchLabels:
      app: game-server
  template:
    metadata:
      labels:
        app: game-server
    spec:
      containers:
      - name: game-server
        image: game-server:3.0.0
        ports:
        - containerPort: 8080
          protocol: TCP
        - containerPort: 5000
          protocol: UDP
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
```

## Rolling Deployment

### Zero-Downtime Update Strategy
```
Phase 1: Create new pods (replicas++)
Phase 2: Wait for health checks (ready)
Phase 3: Route traffic to new pods (0% old)
Phase 4: Remove old pods (replicas--)
```

### Health Check Integration
```
/health                 → Liveness probe
/ready                  → Readiness probe
/startup                → Startup probe
Match state validation  → Custom check
```

## Monitoring & Alerting

### Key Metrics
```
CPU Usage:        < 80% (trigger scaling)
Memory:           < 90% (trigger scaling)
GC Pause:         < 100ms (Java/Go)
Player Latency:   < 200ms (p99)
Server Load:      < 95% (player capacity)
Match Duration:   Target-specific
```

### Alerting Rules
```yaml
alert: HighCPU
  expr: cpu_usage > 0.8 for 5m
  action: Scale +25% replicas

alert: HighLatency
  expr: p99_latency > 200ms for 2m
  action: Page on-call

alert: FailedHealthCheck
  expr: health_check_failures > 3
  action: Trigger rollback
```

## Rollback Procedures

### Automatic Rollback
```
Trigger Condition:
  - Health check failures > 10%
  - Error rate spike > 50%
  - Player disconnect spike

Automatic Action:
  1. Revert to last known good image
  2. Preserve player state (Redis)
  3. Log incident
  4. Alert on-call team
```

### Manual Rollback
```bash
# Immediate rollback
kubectl set image statefulset/game-server \
  game-server=game-server:2.9.0

# Verify rollback
kubectl rollout status statefulset/game-server

# Check player impact
kubectl logs -f deployment/monitoring | grep disconnect
```

## Infrastructure as Code

### Terraform Pattern
```hcl
resource "aws_ecs_service" "game_server" {
  name            = "game-server"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.game_server.arn
  desired_count   = 50

  deployment_configuration {
    maximum_percent         = 150  # Allow 150% replicas
    minimum_healthy_percent = 100  # Keep 100% healthy
  }

  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.game_server.id]
  }
}
```

## CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy Game Server

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: go test ./...
      - run: docker build -t gameserver:${{ github.sha }} .

  deploy:
    needs: test
    steps:
      - run: kubectl set image deployment/game-server \
              gameserver=gameserver:${{ github.sha }}
      - run: kubectl rollout status deployment/game-server
      - run: ./health-check.sh  # Verify deployment
```

## Multi-Region Deployment

### Geographic Distribution
```
North America       Europe           Asia
├─ 50 servers       ├─ 50 servers    ├─ 50 servers
├─ 5ms latency      ├─ 5ms latency   ├─ 5ms latency
└─ Failover         └─ Failover      └─ Failover
   ↓                   ↓                ↓
Global Matchmaking (Redis cluster)
```

### DNS Geo-routing
```
Route 53 (AWS)          →  Nearest region
CloudFlare Geo-IP       →  Optimized path
GeoFence validation     →  Regulatory compliance
```

## Cost Optimization

### Scaling by Game Type
```
Casual Games:     10-50 servers
Competitive:      50-200 servers
Battle Royale:    200+ servers (dynamic)

Idle Time Scaling:
  Off-peak hours: Scale down 50%
  Peak hours:     Scale up 200%
  Event times:    Scale up 300%
```

### Resource Allocation
```
CPU:    2 cores per 500 players
Memory: 1GB per 200 concurrent players
Network: 1Mbps per 100 concurrent players
Storage: SSD for server state persistence
```

## Security in Deployment

### Network Security
```
Traffic:          TLS 1.3 encrypted
Port Security:    UFW/Security Groups
DDoS Protection:  Rate limiting
Player Isolation: VPC per tenant
```

### Secrets Management
```
API Keys:         AWS Secrets Manager
DB Credentials:   Kubernetes Secrets
Certificates:     Let's Encrypt auto-renewal
Player Data:      Encrypted at rest
```

## Troubleshooting Deployment

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Memory leak | OOM kills | Restart pods, check leaks |
| High latency | Slow responses | Check GC, increase resources |
| Network issues | Packet loss | Check bandwidth, scale horizontally |
| Health check failure | Pod restart loop | Fix health endpoint, increase timeout |
