"""
Optional LLM summary generation for Standup Coach Agent.

This module keeps LLM support separate from the main workflow. If no API key is
configured, the project still returns a useful non-LLM summary.
"""

import json
import urllib.error
import urllib.request


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def create_rule_based_summary(responses, blockers, action_items):
    """Create a simple summary without calling an LLM."""
    total_updates = len(responses)
    blocker_count = len(blockers)

    summary_lines = [
        f"The team shared {total_updates} standup updates today.",
        f"{blocker_count} blocker(s) need attention.",
        "Top action items:",
    ]

    for item in action_items:
        summary_lines.append(f"- {item}")

    return "\n".join(summary_lines)


def build_llm_prompt(team, responses, blockers, action_items):
    """Build a clear prompt from the standup data."""
    standup_details = []

    for response in responses:
        member = next(
            person for person in team if person["id"] == response["member_id"]
        )
        standup_details.append(
            {
                "name": member["name"],
                "role": member["role"],
                "yesterday": response["yesterday"],
                "today": response["today"],
                "blockers": response["blockers"],
            }
        )

    return (
        "You are a helpful standup coach for a student AI project team. "
        "Write a concise daily standup summary with project health, blockers, "
        "and next steps. Keep it practical and easy for students to understand.\n\n"
        f"Standup details:\n{json.dumps(standup_details, indent=2)}\n\n"
        f"Blockers:\n{json.dumps(blockers, indent=2)}\n\n"
        f"Action items:\n{json.dumps(action_items, indent=2)}"
    )


def call_openai_responses_api(prompt, llm_config):
    """Call the OpenAI Responses API using only the Python standard library."""
    request_body = {
        "model": llm_config["model"],
        "input": prompt,
    }
    request_data = json.dumps(request_body).encode("utf-8")

    request = urllib.request.Request(
        OPENAI_RESPONSES_URL,
        data=request_data,
        headers={
            "Authorization": f"Bearer {llm_config['api_key']}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        response_data = json.loads(response.read().decode("utf-8"))

    if response_data.get("output_text"):
        return response_data["output_text"]

    # Some API responses return text inside a nested output list.
    for item in response_data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in ["output_text", "text"]:
                return content.get("text", "")

    return ""


def generate_standup_summary(team, responses, blockers, action_items, llm_config):
    """Generate an LLM summary when possible, otherwise use a local fallback."""
    fallback_summary = create_rule_based_summary(responses, blockers, action_items)

    if not llm_config["api_key"]:
        return {
            "summary": fallback_summary,
            "used_llm": False,
            "note": "No API key found. Used rule-based summary.",
        }

    prompt = build_llm_prompt(team, responses, blockers, action_items)

    try:
        llm_summary = call_openai_responses_api(prompt, llm_config)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        return {
            "summary": fallback_summary,
            "used_llm": False,
            "note": f"LLM request failed. Used rule-based summary. Error: {error}",
        }

    if not llm_summary:
        return {
            "summary": fallback_summary,
            "used_llm": False,
            "note": "LLM returned an empty summary. Used rule-based summary.",
        }

    return {
        "summary": llm_summary,
        "used_llm": True,
        "note": "Generated with optional LLM support.",
    }
