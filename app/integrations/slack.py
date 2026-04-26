import httpx
from app.config import settings

async def send_slack_alert(
    test_name: str,
    repo: str,
    flakiness_score: float,
    root_cause: str,
    reasoning: str,
    suggested_fix: str
):
    if not settings.slack_webhook_url:
        print("No Slack webhook configured, skipping alert")
        return

    score_percent = round(flakiness_score * 100)

    message = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 Flaky Test Detected"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Test:*\n`{test_name}`"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Repo:*\n{repo}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Flakiness Score:*\n{score_percent}%"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Root Cause:*\n{root_cause}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Analysis:*\n{reasoning}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Suggested Fix:*\n{suggested_fix}"
                }
            },
            {
                "type": "divider"
            }
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.slack_webhook_url,
                json=message,
                timeout=10.0
            )
            response.raise_for_status()
            print(f"Slack alert sent for {test_name}")
    except Exception as e:
        print(f"Failed to send Slack alert: {e}")