import anthropic
import json
from typing import List
from app.agent.prompts import build_analysis_prompt
from app.agent.tools import DB_QUERY_TOOL, FETCH_LOG_TOOL
from app.config import settings


def parse_agent_response(content: list) -> dict:
    for block in content:
        if hasattr(block, "text"):
            text = block.text.strip()
            try:
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0].strip()
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0].strip()
                return json.loads(text)
            except json.JSONDecodeError:
                pass
    return {
        "is_flaky": False,
        "confidence": 0.0,
        "root_cause": "unknown",
        "reasoning": "Could not parse agent response",
        "suggested_fix": "Manual investigation required"
    }


async def analyze_test_with_llm(
    test_name: str,
    history: List[dict]
) -> dict:
    if not settings.anthropic_api_key:
        return {
            "is_flaky": False,
            "confidence": 0.0,
            "root_cause": "unknown",
            "reasoning": "No Anthropic API key configured",
            "suggested_fix": "Add ANTHROPIC_API_KEY to .env file"
        }

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    prompt = build_analysis_prompt(test_name, history)
    messages = [{"role": "user", "content": prompt}]

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            tools=[DB_QUERY_TOOL, FETCH_LOG_TOOL],
            messages=messages,
        )

        while response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    if block.name == "query_test_history":
                        result = f"History already provided: {len(history)} runs"
                    else:
                        result = "Log not available in local environment"

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            messages += [
                {"role": "assistant", "content": response.content},
                {"role": "user", "content": tool_results}
            ]

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                tools=[DB_QUERY_TOOL, FETCH_LOG_TOOL],
                messages=messages,
            )

        return parse_agent_response(response.content)

    except Exception as e:
        return {
            "is_flaky": False,
            "confidence": 0.0,
            "root_cause": "unknown",
            "reasoning": f"Agent error: {str(e)}",
            "suggested_fix": "Check API key and network connection"
        }