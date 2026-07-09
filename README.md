# Standup Coach Agent

Standup Coach Agent is a lightweight Python workflow assistant for student project teams. It simulates a daily standup process, collects team updates from sample JSON files, identifies blockers, generates action items, suggests GitHub task board updates, and creates a formatted Word document summary.

This project does not require real Slack or GitHub API access. It uses local sample data so the workflow is easy to understand, run, and extend.

## Why This Is Useful

Student AI project teams often need a simple way to stay organized during fast-moving sprints. Standup Coach Agent helps teams:

- Review what each member completed yesterday.
- Track what each member plans to work on today.
- Surface blockers before they slow down the project.
- Turn blockers into action items.
- Suggest task board updates for GitHub Projects or GitHub Issues.
- Create a shareable `.docx` summary for instructors, teammates, or project documentation.

## Tools Used

- Python
- JSON sample data
- `python-docx` for Word document generation

## Project Structure

```text
standup-coach-agent/
├── data/
│   ├── sample_team.json
│   └── sample_standup_responses.json
├── output/
├── standup_agent.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Install Dependencies

From inside the project folder, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required package:

```bash
pip install -r requirements.txt
```

## How To Run

Run the script from the project folder:

```bash
python standup_agent.py
```

After the script runs, a Word document will be created in the `output/` folder. The filename will include the current date.

## How It Works

The script follows a simple workflow:

1. Load team data from `data/sample_team.json`.
2. Load standup responses from `data/sample_standup_responses.json`.
3. Identify team members who reported blockers.
4. Generate action items from those blockers.
5. Suggest GitHub task board updates.
6. Create a formatted Word document summary in `output/`.

## Future Enhancements

- Slack integration for collecting real standup responses.
- GitHub Issues or GitHub Projects integration.
- Automated standup reminders.
- LLM-generated summaries and next-step recommendations.
- A simple web dashboard for viewing team progress.
