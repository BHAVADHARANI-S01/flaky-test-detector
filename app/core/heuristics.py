from typing import List

def compute_flakiness_score(history: List[dict]) -> float:
    if len(history) < 3:
        return 0.0

    total = len(history)
    failures = sum(1 for r in history if not r["passed"])
    pass_rate = failures / total

    if pass_rate == 0.0 or pass_rate == 1.0:
        return 0.0

    retry_passes = sum(
        1 for r in history
        if r["passed"] and r.get("retry_count", 0) > 0
    )
    retry_signal = min(retry_passes / total, 0.4)

    durations = [r["duration_ms"] for r in history if r["duration_ms"] > 0]
    duration_signal = 0.0
    if len(durations) > 1:
        avg = sum(durations) / len(durations)
        variance = sum((d - avg) ** 2 for d in durations) / len(durations)
        std_dev = variance ** 0.5
        if avg > 0:
            cv = std_dev / avg
            duration_signal = min(cv * 0.2, 0.2)

    base_score = 1.0 - abs(pass_rate - 0.5) * 2
    total_score = min(base_score + retry_signal + duration_signal, 1.0)
    return round(total_score, 3)


def classify_root_cause_heuristic(history: List[dict]) -> str:
    error_messages = [
        r.get("error_message", "") or ""
        for r in history if not r["passed"]
    ]

    combined = " ".join(error_messages).lower()

    if any(word in combined for word in ["timeout", "timed out", "deadline"]):
        return "timing"
    elif any(word in combined for word in ["connection", "network", "socket", "http"]):
        return "network"
    elif any(word in combined for word in ["port", "address", "already in use"]):
        return "resource_contention"
    elif any(word in combined for word in ["order", "depends", "setup", "teardown"]):
        return "test_ordering"
    elif any(word in combined for word in ["environment", "env", "variable", "config"]):
        return "environment"
    else:
        return "unknown"