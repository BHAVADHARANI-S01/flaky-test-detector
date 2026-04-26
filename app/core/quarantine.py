from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import FlakyTestRecord


async def quarantine_test(
    db: AsyncSession,
    test_name: str,
    repo: str
) -> bool:
    result = await db.execute(
        select(FlakyTestRecord)
        .where(FlakyTestRecord.test_name == test_name)
        .where(FlakyTestRecord.repo == repo)
    )
    record = result.scalar_one_or_none()

    if record:
        record.is_quarantined = True
        await db.commit()
        print(f"Quarantined test: {test_name}")
        return True
    return False


async def unquarantine_test(
    db: AsyncSession,
    test_name: str,
    repo: str
) -> bool:
    result = await db.execute(
        select(FlakyTestRecord)
        .where(FlakyTestRecord.test_name == test_name)
        .where(FlakyTestRecord.repo == repo)
    )
    record = result.scalar_one_or_none()

    if record:
        record.is_quarantined = False
        await db.commit()
        print(f"Unquarantined test: {test_name}")
        return True
    return False