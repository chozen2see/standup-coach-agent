"""
Standup Coach Agent

This beginner-friendly script simulates an AI workflow assistant for student
project teams. It reads sample team data and standup responses, identifies
blockers, creates action items, suggests GitHub task board updates, and writes
a formatted Word document summary.
"""

import json
from datetime import date
from pathlib import Path

from docx import Document

from config import get_llm_config, load_environment
from llm_summary import generate_standup_summary


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"


def load_json_file(file_path):
    """Load and return JSON data from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def find_team_member(team, member_id):
    """Find a team member by their ID."""
    for member in team:
        if member["id"] == member_id:
            return member

    return None


def response_has_blocker(response):
    """Return True when a standup response includes a real blocker."""
    blocker_text = response["blockers"].strip().lower()
    no_blocker_answers = ["none", "no", "no blockers", "n/a", "na"]

    return blocker_text not in no_blocker_answers


def identify_blockers(team, responses):
    """Create a list of blockers with the team member attached."""
    blockers = []

    for response in responses:
        if response_has_blocker(response):
            member = find_team_member(team, response["member_id"])
            blockers.append(
                {
                    "name": member["name"],
                    "role": member["role"],
                    "blocker": response["blockers"],
                }
            )

    return blockers


def generate_action_items(blockers):
    """Turn blockers into clear action items for the project team."""
    action_items = []

    for blocker in blockers:
        action_items.append(
            f"Follow up with {blocker['name']} about blocker: {blocker['blocker']}"
        )

    if not action_items:
        action_items.append("No blockers reported today. Keep the current sprint moving.")

    return action_items


def suggest_github_updates(team, responses, blockers):
    """Suggest task board updates without using the real GitHub API."""
    updates = []
    blocked_names = {blocker["name"] for blocker in blockers}

    for response in responses:
        member = find_team_member(team, response["member_id"])

        if member["name"] in blocked_names:
            updates.append(
                {
                    "task_owner": member["github_username"],
                    "suggested_column": "Blocked",
                    "note": f"Review blocker: {response['blockers']}",
                }
            )
        else:
            updates.append(
                {
                    "task_owner": member["github_username"],
                    "suggested_column": "In Progress",
                    "note": f"Continue work: {response['today']}",
                }
            )

    return updates


def create_docx_summary(
    team, responses, blockers, action_items, github_updates, standup_summary
):
    """Create a formatted Word document summary in the output folder."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    today = date.today().isoformat()
    output_path = OUTPUT_DIR / f"standup_summary_{today}.docx"

    document = Document()
    document.add_heading("Daily Standup Summary", level=1)
    document.add_paragraph(f"Date: {today}")

    document.add_heading("AI-Generated Summary", level=2)
    document.add_paragraph(standup_summary["summary"])
    document.add_paragraph(f"Source: {standup_summary['note']}")

    document.add_heading("Team Updates", level=2)
    for response in responses:
        member = find_team_member(team, response["member_id"])

        document.add_heading(f"{member['name']} - {member['role']}", level=3)
        document.add_paragraph(f"Yesterday: {response['yesterday']}")
        document.add_paragraph(f"Today: {response['today']}")
        document.add_paragraph(f"Blockers: {response['blockers']}")

    document.add_heading("Blockers", level=2)
    if blockers:
        for blocker in blockers:
            document.add_paragraph(
                f"{blocker['name']} ({blocker['role']}): {blocker['blocker']}",
                style="List Bullet",
            )
    else:
        document.add_paragraph("No blockers reported today.")

    document.add_heading("Action Items", level=2)
    for item in action_items:
        document.add_paragraph(item, style="List Number")

    document.add_heading("Suggested GitHub Task Board Updates", level=2)
    for update in github_updates:
        document.add_paragraph(
            f"@{update['task_owner']} -> {update['suggested_column']}: {update['note']}",
            style="List Bullet",
        )

    document.save(output_path)
    return output_path


def main():
    """Run the standup workflow from sample JSON files."""
    load_environment()

    team = load_json_file(DATA_DIR / "sample_team.json")
    responses = load_json_file(DATA_DIR / "sample_standup_responses.json")

    blockers = identify_blockers(team, responses)
    action_items = generate_action_items(blockers)
    github_updates = suggest_github_updates(team, responses, blockers)
    standup_summary = generate_standup_summary(
        team, responses, blockers, action_items, get_llm_config()
    )
    output_path = create_docx_summary(
        team, responses, blockers, action_items, github_updates, standup_summary
    )

    print("Standup Coach Agent finished successfully.")
    print(f"Blockers found: {len(blockers)}")
    print(f"LLM summary used: {standup_summary['used_llm']}")
    print(f"Summary saved to: {output_path}")


if __name__ == "__main__":
    main()
