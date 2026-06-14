# CampusFlow — AI Operating System for Student Life

> A multi-tenant campus assistant that combines a live SQLite academic database with Google Gemini to deliver personalized, data-grounded answers to every student question.

---

## Hackathon Submission — Amazon Leadership Principles

### Customer Obsession

Every decision in CampusFlow starts with one question: what does a stressed engineering student actually need right now? Not another app to install. Not another portal to log into. A single intelligent interface that already knows their schedule, their attendance risk, their upcoming deadlines, and what is being served for lunch — and answers in plain language.

Concrete examples of this principle in the product:

- A student whose Operating Systems attendance has dropped to 68% sees a red alert card the moment they open the dashboard — without asking for it.
- The AI knows the exact number of classes they can still miss before hitting the institutional 75% cutoff, and says so when asked.
- The mess menu shown is the one currently being served, not a static list — because the app reads the system clock and cross-references it against meal time windows.
- When a student asks "Am I safe to take a leave this Friday?", the AI has already loaded their full attendance history, leave log, and upcoming exam schedule before formulating a response.

### Invent and Simplify

Campus data is fragmented by design — timetables live on notice boards, marks on a separate ERP portal, mess menus on WhatsApp groups, events on physical posters. CampusFlow replaces this with a single local database that every feature reads from.

The AI architecture follows the same principle. Instead of a complex vector retrieval pipeline, the backend uses intent detection (keyword matching) to run targeted SQL queries and packs the results as structured plaintext into the Gemini prompt. The model reasons over real numbers, never guesses. The entire pattern requires no external services, no vector store, and no fine-tuning.

### Multi-Tenant, Secure Architecture — Scalability on AWS

CampusFlow v2 is built as a proper multi-tenant system from the ground up:

- Every student record (attendance, marks, leaves) carries a `user_id` foreign key. No query returns data across tenant boundaries.
- Passwords are hashed with bcrypt at work factor 12. Plaintext passwords are never stored or logged.
- Session state is server-side (`st.session_state`), not URL parameters or cookies.
- The database abstraction layer (`db.py`) isolates all SQL from the UI layer — swapping SQLite for PostgreSQL on Amazon RDS requires only the connection string.

The path to production AWS deployment is a straight line: containerize with Docker, deploy on ECS Fargate, move the database to RDS, manage secrets through AWS Secrets Manager, and put an Application Load Balancer in front. The application code does not change.

---

## Features

| Feature | Description |
|---|---|
| Secure authentication | bcrypt-hashed login and registration, scoped session tokens |
| Multi-tenant data isolation | All records filtered by `user_id` — no cross-user data exposure |
| Live status dashboard | Next class, current mess meal, overall attendance, nearest deadline |
| Attendance alert system | Red alert card auto-renders when any subject falls below 75% |
| College calendar integration | Today's date cross-referenced against official working days and holidays |
| Subject-wise attendance tracker | Per-subject counts, computed percentages, low-attendance flagging |
| Academic marks panel | Internal-1, Internal-2 scores per subject with average internals computed |
| Leave application system | Submit leave from sidebar, view history with approval status |
| BLACKY — AI chatbot | Gemini 1.5 Flash with full academic context injection per query |
| Smart context builder | Keyword intent detection routes each query to the correct DB tables |
| Tabbed detail panels | Schedule / Attendance / Marks / Leave History / Events in one view |
| Environment credential loading | API key loaded from `.env` automatically; sidebar fallback for sessions |

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI framework | Streamlit 1.x (Python 3.12) |
| Database | SQLite — `campus.db` |
| AI model | Google Gemini 1.5 Flash via `google-generativeai` SDK |
| Password security | bcrypt (work factor 12) |
| Environment config | python-dotenv |
| Theme | Custom CSS + `.streamlit/config.toml` dark base |

---

## Database Schema

### Per-user tables (tenant-scoped)

**`users`**
| Column | Type | Notes |
|---|---|---|
| id | INTEGER PK | Auto-increment |
| username | TEXT UNIQUE | Case-insensitive |
| password_hash | TEXT | bcrypt hash |
| name | TEXT | Full name |
| department | TEXT | CSE / ECE / MECH |
| semester | INTEGER | 1–8 |

**`attendance_records`**
| Column | Type | Notes |
|---|---|---|
| user_id | INTEGER FK | References users(id) |
| subject_name | TEXT | Subject name |
| total_classes_conducted | INTEGER | Classes held so far |
| classes_attended | INTEGER | Classes attended |

**`academic_marks`**
| Column | Type | Notes |
|---|---|---|
| user_id | INTEGER FK | References users(id) |
| subject_name | TEXT | Subject name |
| exam_type | TEXT | Internal-1 / Internal-2 / End-Semester |
| marks_obtained | REAL | Score |
| total_marks | REAL | Out of (default 50) |

**`leave_applications`**
| Column | Type | Notes |
|---|---|---|
| user_id | INTEGER FK | References users(id) |
| leave_date | TEXT | YYYY-MM-DD |
| reason | TEXT | Free text |
| status | TEXT | Pending / Approved |

### Shared tables (institution-wide)

**`timetables`** — Department, day, time slot, subject, room number (67 rows across CSE / ECE / MECH)

**`mess_menu`** — Day, meal type, time window, full menu items (28 rows, Mon–Sun, 4 meals/day)

**`college_events`** — Event name, type, date, description, venue, organizer (19 events: hackathons, exams, assignments, workshops, cultural)

**`college_calendar`** — Date, day type (Working Day / Official Holiday / Weekend), description (183 rows covering June–November 2025)

---

## Project Structure

```
campusflow/
├── app.py              # UI orchestrator — dashboard, chatbot, all page rendering
├── auth.py             # Login and Register pages + session gate
├── db.py               # All DB logic: connection, queries, LLM context builder
├── init_db.py          # Schema creation + mock data seeding script
├── campus.db           # SQLite database (generated by init_db.py)
├── .env                # Credentials — GEMINI_API_KEY (not committed to git)
├── .gitignore          # Excludes .env, .venv, campus.db, __pycache__
├── requirements.txt    # Pinned dependencies
├── .streamlit/
│   └── config.toml     # Dark theme configuration
├── WORKFLOW.md         # Full system architecture and AI orchestration guide
└── README.md           # This file
```

---

## Setup and Run

### Prerequisites

- Python 3.12
- A Google Gemini API key — free at [aistudio.google.com](https://aistudio.google.com/)

### 1. Install dependencies

```bash
.venv/bin/pip install -r requirements.txt
```

### 2. Configure your API key

Add your Gemini API key to the `.env` file:

```
GEMINI_API_KEY=your_actual_key_here
```

Alternatively, paste it directly into the sidebar when the app is running.

### 3. Initialize the database

```bash
.venv/bin/python3.12 init_db.py
```

This creates `campus.db` and seeds all tables with realistic mock data for three demo accounts.

### 4. Launch the app

```bash
.venv/bin/streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Demo Accounts

Three accounts are pre-seeded with distinct academic profiles for demonstration:

| Username | Password | Department | Academic Profile |
|---|---|---|---|
| `alex` | `alex123` | CSE | Two subjects below 75% attendance (OS: 68%, Networks: 69%), average internals 71% |
| `priya` | `priya123` | ECE | Strong attendance across all subjects, average internals 88% |
| `rahul` | `rahul123` | MECH | Thermodynamics attendance at 70%, mixed marks performance |

---

## How the AI Works

BLACKY is not a generic chatbot. It is a retrieval-augmented assistant — before every Gemini API call, the backend runs SQL queries against the logged-in student's records and injects the results as structured context into the model prompt.

```
User message
    → Intent detection (keyword matching)
    → Targeted SQL queries (attendance, marks, leaves, timetable, mess, events)
    → Context string assembled from real database rows
    → Gemini receives: system prompt + context block + user question
    → Response grounded in actual student data
```

When a student asks "Am I safe to take a leave this Friday?", the model receives their exact attendance counts per subject, their leave history, and the upcoming exam schedule. It does not estimate — it calculates.

For the complete architecture breakdown, see [WORKFLOW.md](WORKFLOW.md).

---

## Example Conversations

```
You: Which subject is most at risk for attendance?

BLACKY: Alex, your two subjects below the 75% cutoff are:
  - Operating Systems: 26/38 classes attended (68.4%)
  - Computer Networks: 25/36 classes attended (69.4%)

  For OS, you need to attend the next 4 consecutive classes
  to cross back above 75%. Missing any more will require a
  formal attendance shortage application.

---

You: What are my internal marks looking like?

BLACKY: Average across all internals: 71.0%

  Stronger subjects:
  - Database Management Systems: 82.0% avg
  - Machine Learning: 85.0% avg

  Needs attention:
  - Operating Systems: 58.0% avg
  - Computer Networks: 61.0% avg

  Recommend focusing revision on OS and Networks before
  the mid-semester on July 14.

---

You: What's for dinner tonight?

BLACKY: Tonight's dinner (7:30 PM - 9:30 PM):
  Chapati, Paneer Butter Masala, Steamed Rice,
  Mixed Veg Dal, Gulab Jamun, and Salad.
```

---

## Future Roadmap

The detailed multi-phase roadmap is documented in [WORKFLOW.md](WORKFLOW.md). Key planned additions:

- Attendance update UI and admin panel for faculty
- PostgreSQL migration for concurrent multi-user production deployments
- AWS deployment — ECS Fargate, RDS, Secrets Manager, ALB
- Streaming Gemini responses for real-time feel
- Proactive daily attendance alerts via scheduled jobs
- GPA prediction model for target score calculations
- Semantic search (embedding-based) to replace keyword intent detection
- Gemini function calling — model decides which DB tools to invoke
- College ERP integration to replace mock seeded data with live records

---

## Contributing

This is a hackathon prototype. The codebase is intentionally lean — one database file, four Python modules, one config file. If you are extending it, keep that principle: add to the abstraction in `db.py` before adding SQL anywhere else, and keep all AI prompt logic in `query_blacky()` and `build_llm_context()`.

---

*CampusFlow v2.0 — built for the Amazon Hackathon.*
