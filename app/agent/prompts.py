from typing import List


def build_analysis_prompt(test_name: str, history: List[dict]) -> str:
    total = len(history)
    failures = sum(1 for r in history if not r["passed"])
    passes = total - failures

    error_messages = list(set([
        r.get("error_message", "")
        for r in history
        if not r["passed"] and r.get("error_message")
    ]))

    durations = [r["duration_ms"] for r in history if r["duration_ms"] > 0]
    avg_duration = round(sum(durations) / len(durations), 2) if durations else 0

    pass_fail_sequence = " ".join([
        "PASS" if r["passed"] else "FAIL"
        for r in history
    ])

    prompt = f"""
You are a senior test reliability engineer. Analyze this test run history and determine if it is flaky.

Test name: {test_name}
Total runs: {total}
Passes: {passes}
Failures: {failures}
Average duration: {avg_duration}ms

Pass/Fail sequence (most recent first):
{pass_fail_sequence}

Error messages seen on failures:
{chr(10).join(f"- {e}" for e in error_messages[:5]) if error_messages else "- No error messages recorded"}

Your job:
1. Determine if this test is flaky (non-deterministic)
2. Classify the root cause
3. Suggest a fix

Root cause categories:
- timing: timeouts, race conditions, async issues
- network: connection errors, HTTP failures
- resource_contention: port conflicts, file locks, memory
- test_ordering: depends on other tests running first
- environment: env variables, OS differences, config
- unknown: cannot determine

Respond ONLY with a valid JSON object like this:
{{
  "is_flaky": true,
  "confidence": 0.85,
  "root_cause": "timing",
  "reasoning": "The test fails intermittently with timeout errors suggesting a race condition",
  "suggested_fix": "Add explicit wait conditions or increase the timeout threshold"
}}
"""
    return prompt.strip()