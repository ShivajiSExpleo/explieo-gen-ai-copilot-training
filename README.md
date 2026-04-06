# Explieo — Gen AI & GitHub Copilot Training

A hands-on training program designed to help engineering teams work effectively with **GitHub Copilot** and **Generative AI** tools. This repository contains all course materials, lab exercises, code samples, and supporting resources used across training sessions.

---

## 📚 Course Overview

This program covers how to leverage AI-assisted development to write better code faster — with a focus on practical prompt engineering, real-world Python exercises, and responsible AI usage in enterprise settings.

| Module | Topic |
|--------|-------|
| Day 1 | Introduction to GitHub Copilot · Prompt Engineering Fundamentals |
| Day 2 | Advanced Prompting · Code Generation · Testing with AI |
| Upcoming | *(updated as sessions are added)* |

---

## 🗂️ Repository Structure

```
.
├── 6AprilOnwardsTraining/          # Class materials from Apr 6 onwards
│   ├── Day2.py                     # CSV streaming exercise (Day 2)
│   ├── lab_starter_Day1.py         # Hands-on lab starter file (Day 1)
│   ├── PythonCodes/                # Additional Python exercises & tests
│   ├── PresentationDay1.pptx       # Day 1 slide deck
│   └── copilot_instructor_guide.docx
│
├── dashboard/                      # Live training dashboard (FastAPI)
│   ├── server.py                   # Backend server
│   ├── parser.py                   # Data parser
│   ├── static/index.html           # Frontend UI
│   └── requirements.txt
│
├── Prompt_Engineering_for_Precise_Code_Generation.docx      # Day 1 guide
├── Prompt_Engineering_for_Precise_Code_Generation_Day2.docx # Day 2 guide
├── copilot_instructor_guide_Day1.docx                       # Instructor reference
├── AI_Assisted_Python_Pre_Post_Assessments.xlsx             # Pre/Post assessments
└── Stackquotient_template.xlsx                              # Template resource
```

---

## 🧪 Lab Exercises

Each lab file includes:
- **Business context** — why this function matters in a real team
- **Acceptance criteria** — what "done" looks like
- **Team standards** — type hints, docstrings, input validation, edge cases, and tests

### Day 1 Labs (`lab_starter_Day1.py`)
| # | Exercise | Concepts |
|---|----------|----------|
| 1 | `validate_customer_email` | Input normalization, domain allowlists |
| 2 | `calculate_compound_interest` | Financial calculations, input validation |
| 3 | `load_csv_records` | File I/O, error handling |
| 4 | `fetch_api_json` | HTTP requests, timeouts, safe error messages |
| 5 | `mask_pii` | Data privacy, dictionary immutability |
| 6 | Unit Tests | pytest, happy paths, edge cases |

### Day 2 Labs (`Day2.py`)
| # | Exercise | Concepts |
|---|----------|----------|
| 1 | `stream_csv_records` | Memory-efficient generators, chunked streaming |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- [GitHub Copilot](https://github.com/features/copilot) enabled in your IDE
- VS Code (recommended) with the GitHub Copilot extension

### Running the Dashboard

```bash
cd dashboard
pip install -r requirements.txt
./start.sh
```

Then open `http://localhost:8000` in your browser.

### Running Lab Tests

```bash
cd 6AprilOnwardsTraining/PythonCodes
pytest test_day2.py -v
```

---

## 📋 Team Coding Standards

All exercises follow these enterprise standards — the same ones Copilot should be prompted to respect:

1. ✅ Add **type hints** to all function signatures
2. ✅ Add **concise docstrings** with parameters and return values
3. ✅ **Validate inputs** and raise meaningful exceptions
4. ✅ Handle **edge cases** explicitly
5. ✅ Keep functions **small and readable**
6. ✅ Prefer the **standard library** unless there's a clear reason not to
7. ✅ Write tests for both **success and failure** scenarios

---

## 📅 Session Log

| Date | Session | Topics Covered |
|------|---------|----------------|
| Apr 2, 2025 | Day 1 | Copilot Intro, Prompt Engineering Basics |
| Apr 3, 2025 | Day 2 | Advanced Prompting, Code Generation, Testing |
| Apr 6, 2025 | Day 3 | *(in progress)* |

> This log will be updated after each session.

---

## 🔒 Access

This repository is **private**. Access is granted by the repository owner. Reach out to be added as a collaborator.

---

## 📬 Contact

Maintained by **Explieo** · Training delivered by **SandeepRDiddi**
