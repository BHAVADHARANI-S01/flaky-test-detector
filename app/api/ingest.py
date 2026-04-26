from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.crud import save_test_run, get_test_history, save_flaky_record
from app.core.parser import parse_junit_xml
from app.core.heuristics import compute_flakiness_score
from app.agent.classifier import classify_test
from pydantic import BaseModel

router = APIRouter()


class IngestPayload(BaseModel):
    run_id: str
    commit_sha: str
    repo: str
    runner_os: str = "unknown"
    xml_content: str


@router.post("/api/ingest")
async def ingest_results(
    payload: IngestPayload,
    db: AsyncSession = Depends(get_db)
):
    runs = parse_junit_xml(
        payload.xml_content,
        repo=payload.repo,
        run_id=payload.run_id,
        commit_sha=payload.commit_sha
    )

    if not runs:
        raise HTTPException(status_code=400, detail="No test cases found in XML")

    results = []

    for run_data in runs:
        run_data["runner_os"] = payload.runner_os
        await save_test_run(db, run_data)

        history = await get_test_history(db, run_data["test_name"], payload.repo)
        score = compute_flakiness_score(history)

        if score > 0.1 and len(history) >= 3:
            result = await classify_test(
                run_data["test_name"],
                history,
                repo=payload.repo
            )

            if result["is_flaky"]:
                await save_flaky_record(db, {
                    "test_name": run_data["test_name"],
                    "repo": payload.repo,
                    "flakiness_score": result["flakiness_score"],
                    "root_cause": result["root_cause"],
                    "confidence": result["confidence"],
                    "llm_reasoning": result["reasoning"],
                    "suggested_fix": result["suggested_fix"],
                    "total_runs": len(history),
                    "fail_count": sum(1 for h in history if not h["passed"]),
                })

        results.append({
            "test_name": run_data["test_name"],
            "passed": run_data["passed"],
            "flakiness_score": score,
        })

    return {
        "status": "accepted",
        "runs": len(runs),
        "results": results
    }