async def upload_test_run(run_id: str, data: dict) -> str:
    print(f"Blob storage not configured, skipping upload for {run_id}")
    return ""