# python-ai

I am Muhammad Abdullah Akbar. This repo is my work for the Python for AI course (Module 1: Python Basics for GenAI and Agentic AI).

**My AI goal:** become an AI Agent Developer.

## How to run

```bash
uv run main.py
```

Every lesson script lives in `code/`. Run any of them from the repo root:

```bash
uv run code/lesson_01_intro.py
```

## Module 1 Project: AI Prompt Kit

A Python tool that turns a local business's details into 4 ready-to-use AI prompts.

**Run:** `uv run code/project_m1_prompt_kit.py`

![Prompt Kit running](docs/project-m1-run.png)

**Who would pay for this:** small business owners in Pakistan, like tuition academies and shops, who want AI help but don't know what to type.

## Module 1 Final Project: AI Front Desk

A front desk assistant for a local bakery (example business). It answers common questions with free rules, gives exact price quotes with `/quote` (bulk discount and delivery fee), turns every question it cannot answer into a clean AI prompt routed to a local or cloud-style model with a cost estimate, and ends with a session report for the owner.

**Run:** `uv run code/project_m1_front_desk.py`

![AI Front Desk running](docs/project-m1-part2-run.png)

**Who would pay for this:** a bakery owner whose staff answer the same questions and work out price quotes by hand all day. The desk answers the easy questions instantly, quotes prices the same way every time, and the session report shows which questions it could not answer. I have not measured how much time this saves.

Design, rule tests and AI tests: `docs/project-m1-part2-design.md` and `docs/project-m1-part2-results.md`. The business name, prices, hours and phone number are examples for practice.

## Task 1.8: KIPS Business Helper Bot (design)

A rule-based chatbot for KIPS tuition academy, Lahore. Run: `uv run code/lesson_08_mini_chatbot.py`

The fees, timings and reply texts are example details for practice, not KIPS's real ones. Rules are checked top to bottom and the first match wins.

| # | Intent (what the user wants) | Keywords to look for | Reply |
|---|---|---|---|
| 1 | Exit | bye, exit | Goodbye and chat summary |
| 2 | Human handover | human, agent | "Connecting you to a human..." and the chat ends |
| 3 | Complaint | refund, complaint, unhappy, delay, late | Manager will call today |
| 4 | Fees | fee, price, cost, how much | Matric and Intermediate monthly fees |
| 5 | Admission | admission, admit, enrol, register, join | Send name, class and phone number |
| 6 | Timings | timing, time, hour, open, schedule | Class timings |
| 7 | Location | where, location, address, branch | Lahore, ask the front desk |
| 8 | Subjects | subject, course, matric, intermediate, class | Matric and Intermediate classes |
| 9 | Greeting | hi, hello, salam, assalam | Friendly hello |
| 10 | Anything else | (no match) | Fallback: count it and print the AI prompt for Module 2 |

## Lessons done so far

| Task | What I built | Files |
|---|---|---|
| 1.1 Your AI Career Intro | Prints my name, dream role, a business problem and why | `code/lesson_01_intro.py` |
| 1.2 Toolkit Proof | Proof that my AI dev tools work, plus my first Ollama chat | `code/lesson_02_toolkit.py`, `docs/setup-check.png`, `docs/ollama-first-chat.md` |
| 1.3 Client-Ready Repo | This uv project with `code/`, `docs/`, `notebooks/` and a README | `main.py`, `pyproject.toml`, `uv.lock`, `.gitignore` |
| 1.4 Business Prompt Builder | Asks for business details and builds an AI prompt | `code/lesson_04_print_input.py`, `docs/prompt-test.md` |
| 1.5 AI Model Profile Card | Model profile with `str`, `int`, `float` and `bool`, and a cost estimate | `code/lesson_05_variables.py` |
| 1.6 Prompt Cleaner | Cleans a messy name and question, estimates tokens, builds a prompt | `code/lesson_06_strings_prompts.py` |
| 1.7 Smart Model Router | Picks a model for code, private or chat tasks and estimates the cost | `code/lesson_07_conditions.py` |
| 1.8 Business Helper Bot | Rule-based chatbot for KIPS (design table above) | `code/lesson_08_mini_chatbot.py` |

Also done:

- Module 1 Checkpoint 1 quick checks: `docs/my-answers-module-1.md`
- Module 1 Checkpoint 1 project (AI Prompt Kit): `code/project_m1_prompt_kit.py` and `docs/project-m1-results.md`
- Module 1 Checkpoint 2 quick checks: `docs/my-answers-module-1.md`
- Module 1 Checkpoint 2 project (AI Front Desk): `code/project_m1_front_desk.py`, `docs/project-m1-part2-design.md` and `docs/project-m1-part2-results.md`
