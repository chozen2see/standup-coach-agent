# Standup Coach Agent

Standup Coach Agent is a lightweight Python application I built to show one practical way AI can support one of the most common engineering workflows: the daily standup.

The goal isn't to replace team conversations. It's to reduce the follow-up work that usually comes afterward by capturing updates, surfacing blockers, identifying action items, and producing a clear daily summary. The project uses local sample data, so it's easy to run without setting up Slack, GitHub, or an LLM provider first. Optional AI summaries and GitHub Issues support can be enabled as you expand the project.

The project also includes an AI Standup Coach feature. Rather than simply summarizing a standup, it reviews the quality of each person's update and provides practical feedback to help improve future standups.

---

## Who This Project Is For

This project was designed with student software engineering teams in mind, but the workflow can easily be adapted for professional development teams.

Whether you're working through a class project, a hackathon, or a small engineering sprint, the goal is the same: spend less time organizing standup notes and more time building software.

---

## Why I Built This

One thing I've noticed is that daily standups don't usually create the work. The follow-up afterward does.

Someone has to document updates, track blockers, assign action items, and keep project documentation current. Those are all good uses of AI because they reduce repetitive work without replacing the conversations that help teams stay aligned.

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
- `python-docx`
- Optional OpenAI-compatible LLM integration
- Optional GitHub Issues integration
- Slack-style workflow simulation using local JSON data
- Rule-based coaching when no API key is available

---

## Project Structure

```text
standup-coach-agent/
├── data/
│   ├── sample_slack_messages.json
│   ├── sample_standup_responses.json
│   └── sample_team.json
├── output/
├── .env.example
├── .gitignore
├── config.py
├── github_issues.py
├── llm_summary.py
├── README.md
├── requirements.txt
├── slack_parser.py
├── standup_agent.py
└── standup_coach.py
```

### File Overview

| File / Folder | Purpose |
|----------------|---------|
| `data/` | Sample data used to demonstrate both the structured and Slack-style standup workflows. |
| `sample_team.json` | Defines the sample project team and team members. |
| `sample_standup_responses.json` | Structured standup responses used by the original workflow. |
| `sample_slack_messages.json` | Sample Slack-style messages that simulate a daily standup conversation. |
| `output/` | Destination for generated Word reports. |
| `.env.example` | Example environment variables for configuring optional AI and GitHub features. |
| `.gitignore` | Specifies files and folders that should not be committed to the repository. |
| `config.py` | Loads and manages application configuration and environment variables. |
| `github_issues.py` | Generates GitHub Issue recommendations and supports optional GitHub Issues integration. |
| `llm_summary.py` | Generates an optional AI-powered executive summary when an API key is available. |
| `README.md` | Project overview, setup instructions, and usage documentation. |
| `requirements.txt` | Lists the Python package dependencies required to run the project. |
| `slack_parser.py` | Converts Slack-style standup messages into the application's standard response format. |
| `standup_agent.py` | Main application entry point that coordinates the complete standup workflow. |
| `standup_coach.py` | Reviews each team member's standup update and generates coaching feedback to help improve the quality of future standups. |

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

## AI Standup Coach

Generating a summary is useful after a standup, but it doesn't help the team improve the quality of future standups. That's the purpose of the AI Standup Coach.

The application reviews each team member's update for:

- Missing completed work
- Vague descriptions of progress
- Missing or unclear next steps
- Missing blocker status
- Updates that are too brief
- Unnecessary detail that makes updates harder to scan

Example:

```text
Marcus Johnson

✓ Clear update on completed work.
⚠ Today's goal could be more specific.
⚠ No blocker status provided. Consider indicating whether you're blocked or able to continue independently.
```

The coaching appears in its own section of the generated Word report.

### Adapting This for Real Slack Conversations

The current demo intentionally uses structured Slack-style messages so the workflow is easy to understand and test.

In a production implementation, an AI conversation understanding layer could review an entire Slack thread, identify meaningful updates for each participant, and convert the conversation into the structured format used by the application.

Before updating GitHub or generating the Word report, the agent could post a draft summary back into Slack so the team can confirm that the updates were captured correctly.

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
4. Review standup quality and generate coaching feedback.
5. Identify blockers and requests for assistance.
6. Generate action items.
7. Generate an AI summary (optional).
8. Generate GitHub recommendations.
9. Produce a formatted Word report.

Keeping the parsing logic separate from the reporting workflow makes it easy to introduce a real Slack bot later without changing the rest of the application.

---

## Roadmap

Ideas I'm interested in exploring next include:

- Real Slack bot integration for interactive standups
- AI-assisted conversation understanding that can review an entire Slack standup thread, identify meaningful updates for each participant, and convert the conversation into the structured format used by the application
- Team confirmation step in Slack before updates are sent to GitHub or included in the Word report
- GitHub Projects synchronization
- Automated standup reminders
- Richer AI-generated coaching and next-step recommendations
- Lightweight web dashboard for team visibility

---

## Production Deployment Concept

The current project runs locally using sample data, but the same workflow could be deployed as a hosted Slack application.

A production version would use a Python API to receive Slack events, store team updates in a database, use an LLM to structure and review the conversation, request team confirmation, update GitHub, and generate a downloadable Word report.

The current modules are intentionally separated so the local JSON inputs can later be replaced with Slack events and database records without rewriting the reporting workflow.

---

## Development Approach

This project was built using an AI-assisted development workflow.

I used modern AI development tools to help accelerate implementation, iterate on ideas, review code, and refine documentation. I remained responsible for the overall architecture, feature design, testing, and final technical decisions.

One of the goals of this project was not only to build a working application, but also to explore how AI can become a practical engineering partner throughout the software development lifecycle.

---

## About This Project

I built this project as part of my ongoing work in AI-assisted software engineering.

Rather than using AI simply because it's available, I'm interested in finding practical ways it can reduce repetitive work, improve collaboration, and help teams stay focused on building software.