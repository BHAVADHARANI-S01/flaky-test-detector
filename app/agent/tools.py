DB_QUERY_TOOL = {
    "name": "query_test_history",
    "description": "Query the database for historical test run data for a specific test",
    "input_schema": {
        "type": "object",
        "properties": {
            "test_name": {
                "type": "string",
                "description": "The full name of the test to query"
            },
            "limit": {
                "type": "integer",
                "description": "Number of recent runs to fetch",
                "default": 25
            }
        },
        "required": ["test_name"]
    }
}

FETCH_LOG_TOOL = {
    "name": "fetch_stack_trace",
    "description": "Fetch the full stack trace for a failed test run",
    "input_schema": {
        "type": "object",
        "properties": {
            "run_id": {
                "type": "string",
                "description": "The run ID to fetch logs for"
            }
        },
        "required": ["run_id"]
    }
}