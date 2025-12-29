#!/usr/bin/env python3
"""Compare programming languages for game server development."""

LANGUAGES = {
    "go": {
        "strengths": ["Concurrency", "Simplicity", "Fast compile"],
        "weaknesses": ["Generics (limited)", "Error handling"],
        "best_for": ["Microservices", "API servers", "Matchmaking"],
        "performance": 8,
        "developer_experience": 9,
    },
    "rust": {
        "strengths": ["Memory safety", "Performance", "Zero-cost abstractions"],
        "weaknesses": ["Learning curve", "Compile time"],
        "best_for": ["Game engines", "High-performance servers"],
        "performance": 10,
        "developer_experience": 6,
    },
    "cpp": {
        "strengths": ["Raw performance", "Control", "Ecosystem"],
        "weaknesses": ["Complexity", "Memory bugs"],
        "best_for": ["AAA game servers", "Physics engines"],
        "performance": 10,
        "developer_experience": 5,
    },
    "nodejs": {
        "strengths": ["Fast development", "Ecosystem", "Full-stack"],
        "weaknesses": ["Single-threaded", "Callback hell"],
        "best_for": ["Prototypes", "Social games", "Web games"],
        "performance": 6,
        "developer_experience": 9,
    },
}

def recommend_language(requirements: dict) -> str:
    """Recommend best language based on requirements."""
    scores = {}
    for lang, props in LANGUAGES.items():
        score = props["performance"] * requirements.get("performance_weight", 0.5)
        score += props["developer_experience"] * requirements.get("dx_weight", 0.5)
        scores[lang] = score
    return max(scores, key=scores.get)

if __name__ == "__main__":
    print("=== Language Comparison ===")
    for lang, props in LANGUAGES.items():
        print(f"\n{lang.upper()}")
        print(f"  Performance: {props['performance']}/10")
        print(f"  Dev Experience: {props['developer_experience']}/10")
