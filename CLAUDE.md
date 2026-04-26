# CLAUDE.md — Project Context

This file is always loaded. It contains only global project context.
Agent-specific instructions are in `.claude/agents/`. Reusable procedures are in `.claude/skills/`.

---

## What This Project Is

A small web dashboard that aggregates data from external APIs and displays it in a clean UI.
Maintained by two human reviewers. Code is written by AI agents.

**Your role as an agent:** Implement features, fix bugs, open Pull Requests.
- Do NOT merge PRs — humans do that.
- Do NOT make architectural decisions unless an issue explicitly asks for it.
- When an issue is ambiguous, comment your assumptions on the issue, then proceed.

---

## Repository Structure

```
/
├── CLAUDE.md
├── STACK.md               ← created by the agent on first init, documents chosen framework
├── .claude/
│   ├── agents/            ← subagent definitions
│   └── skills/            ← reusable skills
├── frontend/              ← UI
│   └── src/
│       ├── components/    ← one file per widget
│       └── services/      ← API wrappers (calls backend only, never external APIs)
└── backend/               ← FastAPI (Python 3.11+)
    ├── app/
    │   ├── main.py
    │   ├── routers/       ← one router file per API domain
    │   └── schemas/       ← Pydantic models
    ├── requirements.txt
    └── .env.example
```

---

## Available External APIs

### Open-Meteo (Weather)
- Base URL: `https://api.open-meteo.com/v1/`
- No API key required.
- Docs: https://open-meteo.com/en/docs
- Example — current weather in Montreal:
  ```
  GET https://api.open-meteo.com/v1/forecast
    ?latitude=45.5017&longitude=-73.5673
    &current=temperature_2m,weathercode,windspeed_10m
    &timezone=America/Toronto
  ```
- Backend router: `backend/app/routers/weather.py`

> New APIs will be added here as the project grows.
> Do not call any API not listed in this section.

---

## Non-Negotiable Rules

1. **Never commit `.env`** — only `.env.example` with placeholder values.
2. **Frontend calls backend only** — no direct external API calls from the browser.
3. **One issue = one PR** — never bundle unrelated changes.
4. **Keep files small** — split if a file exceeds ~150 lines.

---

## Git Conventions

```bash
# Branch naming
git checkout -b feat/issue-{number}-{short-description}

# Commit style (conventional commits)
git commit -m "feat: add current weather widget (#12)"
git commit -m "fix: handle missing windspeed field (#14)"
```

Prefixes: `feat:` `fix:` `refactor:` `test:` `docs:`
Never push directly to `main`.

---

## How to Run

```bash
# Backend
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend && npm install && npm run dev
```

---

## Out of Scope

- Any service running on the host machine
- Production deployment
- Any file outside `/frontend`, `/backend`, and `.claude/`
