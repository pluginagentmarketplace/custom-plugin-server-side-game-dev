#!/usr/bin/env python3
"""Design pattern validator for game server code."""

PATTERNS = {
    "observer": ["subscribe", "notify", "observer"],
    "command": ["execute", "undo", "command"],
    "state": ["state", "transition", "context"],
    "factory": ["create", "factory", "builder"],
    "singleton": ["instance", "singleton", "_instance"],
}

def check_pattern(code: str, pattern_name: str) -> bool:
    """Check if code follows a specific pattern."""
    keywords = PATTERNS.get(pattern_name, [])
    code_lower = code.lower()
    found = sum(1 for kw in keywords if kw in code_lower)
    return found >= len(keywords) // 2

def analyze_file(filepath: str) -> dict:
    """Analyze a file for design patterns."""
    try:
        with open(filepath, 'r') as f:
            code = f.read()
        return {
            pattern: check_pattern(code, pattern)
            for pattern in PATTERNS
        }
    except FileNotFoundError:
        return {"error": "File not found"}

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        results = analyze_file(sys.argv[1])
        print(f"Patterns found: {[k for k, v in results.items() if v]}")
