"""
Helpers for turning Slack-style standup messages into standup responses.

The project uses local JSON fixtures for now. A real Slack app could provide
messages in a similar shape later.
"""


def find_member_by_name(team, name):
    """Find a team member by display name."""
    for member in team:
        if member["name"].lower() == name.lower():
            return member

    return None


def parse_standup_text(text):
    """Parse Yesterday, Today, and Blockers lines from one message."""
    parsed = {
        "yesterday": "",
        "today": "",
        "blockers": "None",
    }

    field_names = {
        "yesterday": "yesterday",
        "today": "today",
        "blockers": "blockers",
        "blocker": "blockers",
    }

    for line in text.splitlines():
        if ":" not in line:
            continue

        raw_label, value = line.split(":", 1)
        label = raw_label.strip().lower()
        field_name = field_names.get(label)

        if field_name:
            parsed[field_name] = value.strip()

    return parsed


def slack_messages_to_standup_responses(team, slack_messages):
    """Convert Slack-style messages into the app's standup response format."""
    responses = []

    for message in slack_messages:
        member = find_member_by_name(team, message["user_name"])

        if not member:
            continue

        parsed_text = parse_standup_text(message["text"])
        responses.append(
            {
                "member_id": member["id"],
                "yesterday": parsed_text["yesterday"],
                "today": parsed_text["today"],
                "blockers": parsed_text["blockers"],
            }
        )

    return responses
