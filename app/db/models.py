from sqlalchemy import Column, String, Float, Boolean, DateTime, Integer, JSON
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import uuid

class Base(DeclarativeBase):
    pass

class TestRun(Base):
    __tablename__ = "test_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    test_name = Column(String, index=True)
    repo = Column(String)
    commit_sha = Column(String)
    run_id = Column(String)
    passed = Column(Boolean)
    duration_ms = Column(Float)
    error_message = Column(String, nullable=True)
    stack_trace = Column(String, nullable=True)
    retry_count = Column(Integer, default=0)
    runner_os = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    meta = Column(JSON, default={})

class FlakyTestRecord(Base):
    __tablename__ = "flaky_tests"

    test_name = Column(String, primary_key=True)
    repo = Column(String, primary_key=True)
    flakiness_score = Column(Float, default=0.0)
    root_cause = Column(String, nullable=True)
    confidence = Column(Float, default=0.0)
    is_quarantined = Column(Boolean, default=False)
    llm_reasoning = Column(String, nullable=True)
    suggested_fix = Column(String, nullable=True)
    last_analyzed = Column(DateTime, nullable=True)
    total_runs = Column(Integer, default=0)
    fail_count = Column(Integer, default=0)