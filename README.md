# python-ai

I am Muhammad Abdullah Akbar. This repo is my work for the Python for AI course (Module 1: Python Basics for GenAI and Agentic AI).

**My AI goal:** become an AI Agent Developer.

## How to run

```bash
uv run main.py
```

Lesson scripts live in `code/`:

```bash
cd code
uv run lesson_01_intro.py
```

## Module 1 Project: AI Prompt Kit

A Python tool that turns a local business's details into 4 ready-to-use AI prompts.

**Run:** `uv run code/project_m1_prompt_kit.py`

![Prompt Kit running](docs/project-m1-run.png)

**Who would pay for this:** small business owners in Pakistan, like tuition academies and shops, who want AI help but don't know what to type.

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

- Task 1.1: Your AI Career Intro
- Task 1.2: Toolkit Proof
- Task 1.3: Client-Ready Repo
- Task 1.4: Business Prompt Builder
