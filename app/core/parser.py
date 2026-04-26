import xml.etree.ElementTree as ET
from typing import List
import uuid

def parse_junit_xml(xml_content: str, repo: str, run_id: str, commit_sha: str) -> List[dict]:
    runs = []
    
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError:
        return runs

    testsuites = root.findall(".//testcase")

    for testcase in testsuites:
        test_name = testcase.get("name", "unknown")
        classname = testcase.get("classname", "")
        duration_ms = float(testcase.get("time", 0)) * 1000

        failure = testcase.find("failure")
        error = testcase.find("error")

        passed = failure is None and error is None
        error_message = None
        stack_trace = None

        if failure is not None:
            error_message = failure.get("message", "")
            stack_trace = failure.text or ""
        elif error is not None:
            error_message = error.get("message", "")
            stack_trace = error.text or ""

        runs.append({
            "id": str(uuid.uuid4()),
            "test_name": f"{classname}.{test_name}" if classname else test_name,
            "repo": repo,
            "run_id": run_id,
            "commit_sha": commit_sha,
            "passed": passed,
            "duration_ms": duration_ms,
            "error_message": error_message,
            "stack_trace": stack_trace,
            "retry_count": 0,
        })

    return runs