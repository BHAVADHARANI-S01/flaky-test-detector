from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import ingest, reports, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Try to create tables but don't crash if DB fails
    try:
        from app.db.session import create_tables
        await create_tables()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Database setup warning: {e}")
    yield


app = FastAPI(
    title="Flaky Test Detector",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(ingest.router)
app.include_router(reports.router)
app.include_router(health.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "flaky-test-detector"}