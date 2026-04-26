from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.db.models import TestRun, FlakyTestRecord
from datetime import datetime

async def save_test_run(db: AsyncSession, run_data: dict) -> TestRun:
    run = TestRun(**run_data)
    db.add(run)
    await db.commit()
    await db.refresh(run)
    return run

async def get_test_history(
    db: AsyncSession,
    test_name: str,
    repo: str,
    limit: int = 25
) -> list:
    result = await db.execute(
        select(TestRun)
        .where(TestRun.test_name == test_name)
        .where(TestRun.repo == repo)
        .order_by(desc(TestRun.created_at))
        .limit(limit)
    )
    rows = result.scalars().all()
    return [
        {
            "id": r.id,
            "test_name": r.test_name,
            "passed": r.passed,
            "duration_ms": r.duration_ms,
            "error_message": r.error_message,
            "retry_count": r.retry_count,
        }
        for r in rows
    ]

async def save_flaky_record(db: AsyncSession, data: dict) -> FlakyTestRecord:
    result = await db.execute(
        select(FlakyTestRecord)
        .where(FlakyTestRecord.test_name == data["test_name"])
        .where(FlakyTestRecord.repo == data["repo"])
    )
    existing = result.scalar_one_or_none()

    if existing:
        for key, value in data.items():
            setattr(existing, key, value)
        existing.last_analyzed = datetime.utcnow()
    else:
        existing = FlakyTestRecord(**data, last_analyzed=datetime.utcnow())
        db.add(existing)

    await db.commit()
    return existing

async def get_all_flaky_tests(db: AsyncSession, repo: str = None) -> list:
    query = select(FlakyTestRecord)
    if repo:
        query = query.where(FlakyTestRecord.repo == repo)
    result = await db.execute(query)
    return result.scalars().all()