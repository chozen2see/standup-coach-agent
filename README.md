# Standup Coach Agent

Standup Coach Agent is a lightweight Python application that explores how AI can support one of the most common engineering workflows: the daily standup.

The goal is not to replace team conversations. It is to reduce the follow-up work around them: capturing updates, surfacing blockers, identifying action items, and producing a clear daily summary. The project uses local sample data, so it is easy to run without setting up Slack, GitHub, or an LLM provider first. Optional AI summaries and GitHub Issues support can be enabled later.

---

## Why I Built This

Daily standups are useful, but they often create a small pile of follow-up work: documenting updates, tracking blockers, assigning action items, and keeping project notes current.

This project keeps that workflow simple and visible by:

- Capturing what each team member completed.
- Recording current work in progress.
- Bringing blockers and requests for help to the forefront.
- Suggesting follow-up action items.
- Generating GitHub task and issue recommendations.
- Producing a Word summary that can be shared with teammates, instructors, or stakeholders.

---

## Technologies

- Python
- JSON
- python-docx
- Optional OpenAI-compatible LLM integration
- Optional GitHub Issues integration
- Slack-style workflow simulation using local JSON data

---

## Project Structure

```text
standup-coach-agent/
├── data/
│   ├── sample_team.json
│   ├── sample_standup_responses.json
│   └── sample_slack_messages.json
├── output/
├── standup_agent.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Getting Started

From the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the application:

```bash
python standup_agent.py
```

After the script completes, a formatted Word document is generated in the `output/` folder.

---

## Slack-Style Workflow Demo

Many teams collect standup updates in Slack before anyone turns them into notes or tickets. This project simulates that flow with `data/sample_slack_messages.json`.

The Slack-style demo does not require Slack credentials. It reads local messages that look like channel posts, parses the `Yesterday`, `Today`, and `Blockers` sections, and converts them into the same response format used by the rest of the app.

To run the Slack-style workflow for one command:

```bash
STANDUP_INPUT_MODE=slack python standup_agent.py
```

To use it regularly, copy `.env.example` to `.env` and set:

```text
STANDUP_INPUT_MODE=slack
```

Use the default structured JSON workflow with:

```text
STANDUP_INPUT_MODE=structured
```

Both modes produce the same downstream outputs: blockers, action items, GitHub issue dry-run output, and the Word summary.

---

## Optional AI Summary

If an API key is available, the application can generate an AI summary in addition to the standard report.

Copy the example environment file:

```bash
cp .env.example .env
```

Update the values:

```text
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

If no API key is provided, the application automatically falls back to its built-in summary generation.

---

## Optional GitHub Issues Integration

The application can also translate reported blockers into suggested GitHub Issues.

Configure the following values in `.env`:

```text
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO_OWNER=your_github_username_or_org
GITHUB_REPO_NAME=your_repository_name
GITHUB_CREATE_ISSUES=false
```

By default, the project runs in **dry-run mode**, allowing you to review the issues that would be created before making any changes.

Setting:

```text
GITHUB_CREATE_ISSUES=true
```

enables real GitHub Issue creation.

---

## Workflow

The current workflow is intentionally simple:

1. Load the project team.
2. Read structured standup responses or Slack-style messages.
3. Convert the input into one shared response format.
4. Identify blockers and requests for assistance.
5. Generate action items.
6. Recommend GitHub task board updates.
7. Generate GitHub Issue payloads.
8. Produce a formatted Word summary.

The app keeps parsing separate from the reporting workflow, which makes a real Slack bot a natural next step.

---

## Roadmap

Planned enhancements include:

- Real Slack bot integration for interactive standups
- GitHub Projects synchronization
- Automated standup reminders
- Richer AI-generated coaching and next-step recommendations
- Lightweight web dashboard for team visibility

---

## About This Project

This project is part of a practical exploration of AI-assisted software team workflows. The focus is not AI for its own sake. The focus is helping teams reduce administrative work and keep project information easier to act on.
