"""
Standup coaching helpers.

The coaching feature reviews the quality of each person's update. It is not a
standup summary. The goal is to help teammates write clearer engineering
standups over time.
"""


NO_BLOCKER_VALUES = {"none", "no", "no blockers", "n/a", "na"}
VAGUE_WORDS = {"stuff", "things", "worked on", "handled", "helped", "updated"}
MEASURABLE_WORDS = {
    "built",
    "created",
    "fixed",
    "tested",
    "designed",
    "reviewed",
    "implemented",
    "added",
    "completed",
    "wrote",
}
NEXT_STEP_WORDS = {
    "add",
    "build",
    "check",
    "connect",
    "create",
    "finish",
    "review",
    "test",
    "write",
}


def is_empty(value):
    """Return True when a standup field is missing useful content."""
    return not value or not value.strip()


def has_no_blocker(blocker_text):
    """Return True when the blocker field explicitly says there is no blocker."""
    return blocker_text.strip().lower() in NO_BLOCKER_VALUES


def is_unusually_short(response):
    """Return True when the update is too short to be useful."""
    combined_update = " ".join(
        [response.get("yesterday", ""), response.get("today", ""), response.get("blockers", "")]
    )
    return len(combined_update.split()) < 12


def contains_vague_work(text):
    """Return True when a work description is probably too vague."""
    normalized_text = text.strip().lower()

    if len(normalized_text.split()) < 4:
        return True

    for vague_word in VAGUE_WORDS:
        if vague_word in normalized_text:
            return True

    return False


def has_measurable_progress(text):
    """Return True when completed work sounds concrete enough to review."""
    normalized_text = text.strip().lower()

    for word in MEASURABLE_WORDS:
        if word in normalized_text:
            return True

    return False


def has_next_step(text):
    """Return True when today's plan includes a clear next action."""
    normalized_text = text.strip().lower()

    for word in NEXT_STEP_WORDS:
        if normalized_text.startswith(word) or f" {word} " in normalized_text:
            return True

    return False


def has_unnecessary_information(response):
    """Return True when an update is long enough to need trimming."""
    combined_update = " ".join(
        [response.get("yesterday", ""), response.get("today", ""), response.get("blockers", "")]
    )
    return len(combined_update.split()) > 90


def coach_standup_response(member, response):
    """Create coaching feedback for one team member."""
    feedback = []
    yesterday = response.get("yesterday", "")
    today = response.get("today", "")
    blockers = response.get("blockers", "")

    if is_empty(yesterday):
        feedback.append("Warning Missing completed work. Add what changed since the last standup.")
    elif contains_vague_work(yesterday):
        feedback.append("Warning Completed work could be more specific.")
    elif has_measurable_progress(yesterday):
        feedback.append("Good Clear update on completed work.")
    else:
        feedback.append("Warning Completed work is understandable, but add a concrete result.")

    if is_empty(today):
        feedback.append("Warning Missing next steps. Add what you plan to do next.")
    elif has_next_step(today):
        feedback.append("Good Clear next step for today.")
    else:
        feedback.append("Warning Today's goal could be more specific.")

    if is_empty(blockers):
        feedback.append("Warning Missing blocker status. Say whether you are blocked or not.")
    elif has_no_blocker(blockers):
        feedback.append(
            "Warning No blocker reported. Confirm whether you are unblocked or need help."
        )
    else:
        feedback.append("Good Blocker is clear and can be followed up on.")

    if is_unusually_short(response):
        feedback.append("Warning Standup is unusually short. Add enough detail for the team to act.")

    if has_unnecessary_information(response):
        feedback.append("Warning Standup may include extra detail. Keep it focused on project work.")

    return {
        "name": member["name"],
        "role": member["role"],
        "feedback": feedback,
    }


def generate_rule_based_coaching(team, responses):
    """Generate coaching feedback for every standup response."""
    coaching = []

    for response in responses:
        member = next(person for person in team if person["id"] == response["member_id"])
        coaching.append(coach_standup_response(member, response))

    return {
        "items": coaching,
        "used_llm": False,
        "note": "Generated with rule-based coaching.",
    }
