from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.crud import get_all_flaky_tests

router = APIRouter()

@router.get("/api/flaky")
async def get_flaky_tests(
    repo: str = Query(None, description="Filter by repo"),
    db: AsyncSession = Depends(get_db)
):
    records = await get_all_flaky_tests(db, repo=repo)
    return {
        "total": len(records),
        "flaky_tests": [
            {
                "test_name": r.test_name,
                "repo": r.repo,
                "flakiness_score": r.flakiness_score,
                "root_cause": r.root_cause,
                "is_quarantined": r.is_quarantined,
                "total_runs": r.total_runs,
                "fail_count": r.fail_count,
                "last_analyzed": str(r.last_analyzed),
            }
            for r in records
        ]
    }