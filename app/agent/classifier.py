from app.core.heuristics import compute_flakiness_score, classify_root_cause_heuristic


async def classify_test(
    test_name: str,
    history: list,
    repo: str = None
) -> dict:
    score = compute_flakiness_score(history)

    if score < 0.1:
        return {
            "is_flaky": False,
            "flakiness_score": score,
            "root_cause": None,
            "confidence": 1.0,
            "reasoning": "Test passes consistently",
            "suggested_fix": None
        }

    root_cause = classify_root_cause_heuristic(history)

    return {
        "is_flaky": True,
        "flakiness_score": score,
        "root_cause": root_cause,
        "confidence": round(score, 2),
        "reasoning": f"Test shows non-deterministic behavior with flakiness score of {score}. Pattern suggests {root_cause} issue.",
        "suggested_fix": get_fix_suggestion(root_cause)
    }


def get_fix_suggestion(root_cause: str) -> str:
    fixes = {
        "timing": "Add explicit wait conditions, increase timeout thresholds, or fix race conditions in async code.",
        "network": "Mock external HTTP calls in tests or add retry logic with exponential backoff.",
        "resource_contention": "Use unique ports/files per test, add proper setup/teardown, or run tests sequentially.",
        "test_ordering": "Make tests independent by adding proper setup/teardown fixtures.",
        "environment": "Use consistent environment variables across all CI runners.",
        "unknown": "Add logging to capture more details on failure. Run test in isolation to identify the root cause."
    }
    return fixes.get(root_cause, fixes["unknown"])