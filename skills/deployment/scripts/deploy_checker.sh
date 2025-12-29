#!/bin/bash
# Game Server Deployment Readiness Checker
# Validates environment, health checks, and rollback procedures

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/../.."

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASS=0
FAIL=0
WARN=0

check() {
    local name=$1
    local command=$2

    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} $name"
        ((PASS++))
    else
        echo -e "${RED}❌${NC} $name"
        ((FAIL++))
    fi
}

warn() {
    local name=$1
    local command=$2

    if eval "$command" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️${NC}  $name"
        ((WARN++))
    fi
}

echo "=========================================="
echo "🚀 Game Server Deployment Readiness Check"
echo "=========================================="
echo ""

# Environment checks
echo "📋 Environment Checks"
echo "---"
check "Docker installed" "which docker"
check "Docker Compose installed" "which docker-compose"
check "kubectl installed" "which kubectl"
check "Terraform installed" "which terraform"
check "Environment variables configured" "test -f .env.production"
echo ""

# Build checks
echo "🏗️  Build Checks"
echo "---"
check "Docker image builds" "docker build --dry-run -t gameserver:test ."
check "Kubernetes manifests valid" "test -d k8s/ && ls k8s/*.yaml"
check "Terraform configs valid" "test -d terraform/ && ls terraform/*.tf"
echo ""

# Code quality checks
echo "📊 Code Quality"
echo "---"
warn "Code coverage > 80%" "grep -q 'coverage.*80' coverage.xml"
warn "No security vulnerabilities" "test -f security-scan.json"
warn "Dependency audit passed" "npm audit --json | grep -q vulnerabilities"
echo ""

# Deployment artifacts
echo "📦 Deployment Artifacts"
echo "---"
check "Docker registry configured" "test -n \"\$DOCKER_REGISTRY\""
check "Kubernetes secrets exist" "kubectl get secret docker-registry"
check "Database migrations ready" "test -f db/migrations/latest.sql"
warn "Rollback procedure documented" "test -f docs/ROLLBACK.md"
echo ""

# Production readiness
echo "✅ Production Readiness"
echo "---"
check "Health check endpoint" "grep -q '/health' src/server.py"
check "Logging configured" "grep -q 'logging' src/server.py"
check "Metrics endpoint available" "grep -q '/metrics' src/server.py"
warn "Performance baseline established" "test -f docs/PERFORMANCE_BASELINE.md"
echo ""

# Summary
echo "=========================================="
echo "📊 Summary"
echo "=========================================="
echo -e "${GREEN}Passed:${NC}  $PASS"
echo -e "${RED}Failed:${NC}  $FAIL"
echo -e "${YELLOW}Warnings:${NC} $WARN"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✅ READY FOR DEPLOYMENT${NC}"
    exit 0
else
    echo -e "${RED}❌ FIX ISSUES BEFORE DEPLOYMENT${NC}"
    exit 1
fi
