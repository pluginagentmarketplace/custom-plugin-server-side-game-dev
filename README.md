<div align="center">

# Server-Side Game Development Plugin

### Complete Multiplayer Game Server Mastery for Claude Code

**Build scalable multiplayer game servers with 7 specialized agents covering networking, matchmaking, state synchronization, and cloud deployment**

[![Verified](https://img.shields.io/badge/Verified-Working-success?style=flat-square&logo=checkmarx)](https://github.com/pluginagentmarketplace/custom-plugin-server-side-game-dev)
[![License](https://img.shields.io/badge/License-Custom-yellow?style=flat-square)](LICENSE)
[![Version](https://img.shields.io/badge/Version-3.1.0-blue?style=flat-square)](https://github.com/pluginagentmarketplace/custom-plugin-server-side-game-dev)
[![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen?style=flat-square)](https://github.com/pluginagentmarketplace/custom-plugin-server-side-game-dev)
[![Agents](https://img.shields.io/badge/Agents-7-orange?style=flat-square)](#agents-overview)
[![Skills](https://img.shields.io/badge/Skills-17-purple?style=flat-square)](#skills-reference)
[![SASMP](https://img.shields.io/badge/SASMP-v1.3.0-blueviolet?style=flat-square)](#)

[![Networking](https://img.shields.io/badge/Networking-WebSocket_UDP_gRPC-2E9EF7?style=for-the-badge)](skills/networking/)
[![Real-time](https://img.shields.io/badge/Real--time-State_Sync-00C853?style=for-the-badge)](skills/state-sync/)
[![Matchmaking](https://img.shields.io/badge/Matchmaking-ELO_MMR-FF6F00?style=for-the-badge)](skills/matchmaking/)
[![Deployment](https://img.shields.io/badge/Deployment-Docker_K8s-326CE5?style=for-the-badge)](skills/deployment/)

[Quick Start](#quick-start) | [Agents](#agents-overview) | [Skills](#skills-reference) | [Commands](#commands)

</div>

---

## Verified Installation

> **This plugin has been tested and verified working on Claude Code.**
> Last verified: December 2025

---

## Quick Start

### Option 1: Install from GitHub (Recommended)

```bash
# Step 1: Add the marketplace from GitHub
/plugin add marketplace pluginagentmarketplace/custom-plugin-server-side-game-dev

# Step 2: Install the plugin
/plugin install server-side-game-dev-plugin@pluginagentmarketplace-game-server

# Step 3: Restart Claude Code to load new plugins
```

### Option 2: Clone and Load Locally

```bash
# Clone the repository
git clone https://github.com/pluginagentmarketplace/custom-plugin-server-side-game-dev.git

# Navigate to the directory in Claude Code
cd custom-plugin-server-side-game-dev

# Load the plugin
/plugin load .
```

After loading, restart Claude Code.

### Verify Installation

After restarting Claude Code, verify the plugin is loaded. You should see these agents available:

```
custom-plugin-server-side-game-dev:01-game-server-architect
custom-plugin-server-side-game-dev:02-networking-specialist
custom-plugin-server-side-game-dev:03-matchmaking-engineer
custom-plugin-server-side-game-dev:04-state-sync-expert
custom-plugin-server-side-game-dev:05-game-loop-developer
custom-plugin-server-side-game-dev:06-database-specialist
custom-plugin-server-side-game-dev:07-devops-deployment
```

---

## Available Skills

Once installed, these 17 skills become available:

| Skill | Invoke Command | Golden Format |
|-------|----------------|---------------|
| Networking | `Skill("custom-plugin-server-side-game-dev:networking")` | websocket-server.yaml |
| Matchmaking | `Skill("custom-plugin-server-side-game-dev:matchmaking")` | elo-algorithm.yaml |
| State Sync | `Skill("custom-plugin-server-side-game-dev:state-sync")` | interpolation.yaml |
| Game Loop | `Skill("custom-plugin-server-side-game-dev:game-loop")` | fixed-timestep.yaml |
| Databases | `Skill("custom-plugin-server-side-game-dev:databases")` | redis-config.yaml |
| Deployment | `Skill("custom-plugin-server-side-game-dev:deployment")` | k8s-deployment.yaml |
| Monitoring | `Skill("custom-plugin-server-side-game-dev:monitoring")` | prometheus-config.yaml |
| Socket Programming | `Skill("custom-plugin-server-side-game-dev:socket-programming")` | epoll-server.yaml |
| Data Serialization | `Skill("custom-plugin-server-side-game-dev:data-serialization")` | protobuf-schema.proto |
| Multithreading | `Skill("custom-plugin-server-side-game-dev:multithreading")` | thread-pool.yaml |
| Design Patterns | `Skill("custom-plugin-server-side-game-dev:design-patterns")` | game-patterns.yaml |
| Security/Encryption | `Skill("custom-plugin-server-side-game-dev:security-encryption")` | jwt-auth.yaml |
| Communication Protocols | `Skill("custom-plugin-server-side-game-dev:communication-protocols")` | grpc-service.proto |
| Message Queues | `Skill("custom-plugin-server-side-game-dev:message-queues")` | rabbitmq-config.yaml |
| I/O Multiplexing | `Skill("custom-plugin-server-side-game-dev:io-multiplexing")` | epoll-reactor.yaml |
| Async Programming | `Skill("custom-plugin-server-side-game-dev:async-programming")` | async-patterns.yaml |
| Programming Languages | `Skill("custom-plugin-server-side-game-dev:programming-languages")` | language-choice.yaml |

---

## What This Plugin Does

This plugin provides **7 specialized agents** and **17 production-ready skills** for multiplayer game server development:

| Agent | Purpose |
|-------|---------|
| **Game Server Architect** | Design scalable multiplayer architectures, system design |
| **Networking Specialist** | WebSocket, UDP, gRPC, protocol optimization |
| **Matchmaking Engineer** | ELO, skill-based matching, queue systems |
| **State Sync Expert** | Interpolation, prediction, lag compensation |
| **Game Loop Developer** | Fixed timestep, physics integration |
| **Database Specialist** | Redis, PostgreSQL, game data persistence |
| **DevOps Deployment** | Docker, Kubernetes, CI/CD pipelines |

---

## Agents Overview

### 7 Implementation Agents

Each agent is designed to **do the work**, not just explain:

| Agent | Capabilities | Example Prompts |
|-------|--------------|-----------------|
| **Game Server Architect** | System design, scalability, load balancing | `"Design MMO architecture"`, `"Plan 10k CCU server"` |
| **Networking Specialist** | WebSocket, UDP, latency optimization | `"Implement WebSocket server"`, `"Add UDP for game state"` |
| **Matchmaking Engineer** | ELO, MMR, queue management | `"Build matchmaking system"`, `"Implement ELO ranking"` |
| **State Sync Expert** | Interpolation, prediction, reconciliation | `"Add client-side prediction"`, `"Implement state sync"` |
| **Game Loop Developer** | Fixed timestep, physics, tick rate | `"Create 60Hz game loop"`, `"Add physics integration"` |
| **Database Specialist** | Redis caching, PostgreSQL, Cassandra | `"Set up Redis for sessions"`, `"Design player DB schema"` |
| **DevOps Deployment** | Docker, K8s, monitoring, CI/CD | `"Containerize game server"`, `"Deploy to Kubernetes"` |

---

## Commands

4 interactive commands for game server workflows:

| Command | Usage | Description |
|---------|-------|-------------|
| `/server-init` | `/server-init` | Initialize game server project structure |
| `/network-test` | `/network-test` | Test network latency and throughput |
| `/deploy` | `/deploy` | Deploy to cloud infrastructure |
| `/monitor` | `/monitor` | Monitor server health and metrics |

---

## Skills Reference

Each skill includes **Golden Format** content:
- `assets/` - YAML templates and configurations
- `scripts/` - Automation and validation scripts
- `references/` - Methodology guides and best practices

### All 17 Skills by Category

| Category | Skills |
|----------|--------|
| **Networking** | networking, socket-programming, communication-protocols, io-multiplexing |
| **Game Logic** | game-loop, state-sync, multithreading, async-programming |
| **Matchmaking** | matchmaking |
| **Data** | databases, data-serialization, message-queues |
| **Infrastructure** | deployment, monitoring |
| **Architecture** | design-patterns, programming-languages, security-encryption |

---

## Usage Examples

### Example 1: Create WebSocket Game Server

```typescript
// Before: Basic HTTP server

// After (with Networking Specialist agent):
Skill("custom-plugin-server-side-game-dev:networking")

// Generates:
// - WebSocket server with room management
// - Binary protocol for game state
// - Heartbeat and reconnection logic
// - Connection pooling
```

### Example 2: Implement Matchmaking System

```python
# Before: Random player matching

# After (with Matchmaking Engineer agent):
Skill("custom-plugin-server-side-game-dev:matchmaking")

# Provides:
# - ELO rating algorithm
# - Skill-based matching queue
# - Wait time vs match quality balance
# - Party/group support
```

### Example 3: Deploy to Kubernetes

```yaml
# Before: Manual deployment

# After (with DevOps Deployment agent):
Skill("custom-plugin-server-side-game-dev:deployment")

# Creates:
# - Kubernetes deployment manifests
# - Horizontal Pod Autoscaler
# - Service mesh configuration
# - Prometheus monitoring
```

---

## Plugin Structure

```
custom-plugin-server-side-game-dev/
├── .claude-plugin/
│   ├── plugin.json           # Plugin manifest
│   └── marketplace.json      # Marketplace config
├── agents/                   # 7 specialized agents
│   ├── 01-game-server-architect.md
│   ├── 02-networking-specialist.md
│   ├── 03-matchmaking-engineer.md
│   ├── 04-state-sync-expert.md
│   ├── 05-game-loop-developer.md
│   ├── 06-database-specialist.md
│   └── 07-devops-deployment.md
├── skills/                   # 17 skills (Golden Format)
│   ├── networking/
│   │   ├── SKILL.md
│   │   ├── assets/
│   │   ├── scripts/
│   │   └── references/
│   ├── matchmaking/
│   ├── state-sync/
│   ├── game-loop/
│   ├── databases/
│   ├── deployment/
│   ├── monitoring/
│   └── ... (10 more skills)
├── commands/                 # 4 slash commands
│   ├── server-init.md
│   ├── network-test.md
│   ├── deploy.md
│   └── monitor.md
├── hooks/hooks.json
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

---

## Technology Coverage

| Category | Technologies |
|----------|--------------|
| **Languages** | C++, Rust, Go, Node.js, Python |
| **Networking** | WebSocket, UDP, gRPC, TCP, HTTP/2 |
| **Databases** | Redis, PostgreSQL, Cassandra, MongoDB |
| **Serialization** | Protocol Buffers, FlatBuffers, MessagePack |
| **Infrastructure** | Docker, Kubernetes, AWS, GCP, Azure |
| **Monitoring** | Prometheus, Grafana, ELK Stack |

---

## Security Notice

This plugin is designed for **authorized development use only**:

**USE FOR:**
- Building multiplayer game servers
- Learning game networking
- Implementing matchmaking systems
- Cloud deployment automation

**SECURITY TOPICS:**
- JWT authentication
- TLS encryption
- DDoS protection
- Anti-cheat fundamentals

---

## Metadata

| Field | Value |
|-------|-------|
| **Last Updated** | 2025-12-28 |
| **Maintenance Status** | Active |
| **SASMP Version** | 1.3.0 |
| **Support** | [Issues](../../issues) |

---

## License

Custom License - See [LICENSE](LICENSE) for details.

Copyright (c) 2025 Dr. Umit Kacar & Muhsin Elcicek

---

## Contributing

Contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Follow the Golden Format for new skills
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## Contributors

**Authors:**
- **Dr. Umit Kacar** - Senior AI Researcher & Engineer
- **Muhsin Elcicek** - Senior Software Architect

---

<div align="center">

**Build the next generation of multiplayer games!**

[![Made for Games](https://img.shields.io/badge/Made%20for-Game%20Servers-2E9EF7?style=for-the-badge&logo=unity)](https://github.com/pluginagentmarketplace/custom-plugin-server-side-game-dev)

**Built by Dr. Umit Kacar & Muhsin Elcicek**

</div>
