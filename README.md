# Standup Coach Agent

Standup Coach Agent is a lightweight Python application I built to show
one practical way AI can support one of the most common engineering
workflows: the daily standup.

The goal isn't to replace team conversations. It's to reduce the
follow-up work that usually comes afterward by capturing updates,
surfacing blockers, identifying action items, and producing a clear
daily summary. The project uses local sample data, so it's easy to run
without setting up Slack, GitHub, or an LLM provider first. Optional AI
summaries and GitHub Issues support can be enabled as you expand the
project.

The project also includes an AI Standup Coach feature. Instead of
summarizing the standup, it reviews the quality of each person's update
and gives short feedback on how to make the next update more useful.

------------------------------------------------------------------------

## Who This Project Is For

This project was designed with student software engineering teams in
mind, but the workflow can easily be adapted for professional
development teams.

Whether you're working through a class project, a hackathon, or a small
engineering sprint, the goal is the same: spend less time organizing
standup notes and more time building software.

------------------------------------------------------------------------

## Why I Built This

One thing I've noticed is that daily standups don't usually create the
work. The follow-up afterward does.

Someone has to document updates, track blockers, assign action items,
and keep project documentation current. Those are all good uses of AI
because they reduce repetitive work without replacing the conversations
that help teams stay aligned.

This project keeps that workflow simple and visible by:

-   Capturing what each team member completed.
-   Recording current work in progress.
-   Bringing blockers and requests for help to the forefront.
-   Suggesting follow-up action items.
-   Generating GitHub task and issue recommendations.
-   Producing a Word summary that can be shared with teammates,
    instructors, or stakeholders.

------------------------------------------------------------------------

## Technologies

-   Python
-   JSON
-   `python-docx`
-   Optional OpenAI-compatible LLM integration
-   Optional GitHub Issues integration
-   Slack-style workflow simulation using local JSON data
-   Rule-based fallback logic for coaching when no API key is available

------------------------------------------------------------------------

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
├── standup_coach.py
└── standup_agent.py
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
| `slack_parser.py` | Converts Slack-style standup messages into the application's standard response format. |
| `standup_coach.py` | Reviews standup quality and returns coaching feedback for each team member. |
| `standup_agent.py` | Main application entry point that coordinates the complete standup workflow. |
| `requirements.txt` | Lists the Python package dependencies required to run the project. |
| `README.md` | Project overview, setup instructions, and usage documentation. |
```

------------------------------------------------------------------------

## Getting Started

From the project folder:

``` bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the application:

``` bash
python standup_agent.py
```

After the script completes, a formatted Word document is generated in
the `output/` folder.

------------------------------------------------------------------------

## Slack-Style Workflow Demo

Many teams collect standup updates in Slack before anyone turns them
into meeting notes or project tasks.

This project doesn't require a real Slack workspace. Instead, it uses
local sample messages that mirror the format of a typical standup
conversation. That keeps the project easy to run while leaving room for
a real Slack integration later.

To run the Slack-style workflow for a single session:

``` bash
STANDUP_INPUT_MODE=slack python standup_agent.py
```

To make Slack mode the default, copy `.env.example` to `.env` and set:

``` text
STANDUP_INPUT_MODE=slack
```

To switch back to the structured sample data:

``` text
STANDUP_INPUT_MODE=structured
```

Both modes produce the same downstream outputs, including blockers,
action items, GitHub issue recommendations, and the Word summary.

------------------------------------------------------------------------

## AI Standup Coach

Summaries are useful after a standup, but they do not help the team get
better at writing standups. The coaching feature focuses on that
problem.

For each team member, the app reviews the update and looks for common
issues:

- Missing completed work
- Vague descriptions like "worked on stuff"
- Missing or unclear next steps
- Missing blocker status
- Updates that are too short to be useful
- Extra detail that makes the update harder to scan

The feedback is short on purpose. It is meant to be something a teammate
could read quickly and apply the next day.

Example feedback:

```text
Marcus Johnson
Good Clear update on completed work.
Warning Today's goal could be more specific.
Warning Missing blocker status. Say whether you are blocked or not.
```

When `OPENAI_API_KEY` is configured, the app can use the LLM to generate
coaching. Without an API key, it falls back to rule-based coaching so the
feature still works locally.

The coaching appears in its own section of the Word report, separate
from blockers, action items, and GitHub recommendations.


### Adapting This for Real Slack Conversations

The current demo uses structured Slack-style messages so the workflow is easy to understand and test.

In a real Slack channel, a standup may include several messages, follow-up questions, clarifications, and side conversations. An AI layer could review the full thread and extract:

- completed work
- current priorities
- blockers
- requests for help
- task ownership
- follow-up actions

Before updating GitHub or generating the Word report, the agent could post a draft summary back into Slack and ask the team to confirm that the updates were captured correctly.

Once approved, the structured summary could move through the existing workflow for GitHub issue creation, project documentation, and report generation.

------------------------------------------------------------------------

## Optional AI Summary

If an API key is available, the application can generate an AI summary
in addition to the standard report.

Copy the example environment file:

``` bash
cp .env.example .env
```

Update the values:

``` text
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

If no API key is provided, the application automatically falls back to
its built-in summary generation.

------------------------------------------------------------------------

## Optional GitHub Issues Integration

The application can translate reported blockers into suggested GitHub
Issues.

Configure the following values in `.env`:

``` text
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO_OWNER=your_github_username_or_org
GITHUB_REPO_NAME=your_repository_name
GITHUB_CREATE_ISSUES=false
```

By default, the project runs in **dry-run mode**, allowing you to review
the issues that would be created before making any changes.

Setting:

``` text
GITHUB_CREATE_ISSUES=true
```

enables real GitHub Issue creation.

------------------------------------------------------------------------

## Workflow

The current workflow is intentionally straightforward:

1.  Load the project team.
2.  Read structured standup responses or Slack-style messages.
3.  Convert the input into one shared response format.
4.  Identify blockers and requests for assistance.
5.  Generate action items.
6.  Review standup quality and generate coaching feedback.
7.  Recommend GitHub task board updates.
8.  Generate GitHub Issue payloads.
9.  Produce a formatted Word summary.

Keeping the parsing logic separate from the reporting workflow makes it
easy to swap in a real Slack bot later without changing the rest of the
application.

------------------------------------------------------------------------

## Roadmap

Ideas I'm interested in exploring next include:

- Real Slack bot integration for interactive standups
- AI-assisted conversation summarization that can review a full Slack standup thread, identify each team member's completed work, current priorities, blockers, and requests for help, and convert the conversation into the application's standard response format
- Team confirmation step in Slack so the generated summary can be reviewed and corrected before it is sent to GitHub or included in the Word report
- GitHub Projects synchronization
- Automated standup reminders
- Richer AI-generated coaching and next-step recommendations
- Lightweight web dashboard for team visibility

------------------------------------------------------------------------

## About This Project

I built this project as part of my ongoing work exploring how AI can
improve software engineering workflows.

Rather than using AI simply because it's available, I'm interested in
finding practical ways it can reduce repetitive work, improve
collaboration, and help teams stay focused on building software.
