# ⚡ CampusFlow — AI Operating System for Student Life

> *"From scattered information to a single intelligent interface — CampusFlow is your Jarvis on campus."*

---

## 🏆 Hackathon Submission Pitch

### Built on Amazon's Leadership Principles

#### 1. Customer Obsession
Every feature in CampusFlow was designed by starting with one central question: *What does a stressed engineering student actually need in their day?* Not another notification app. Not another portal to remember credentials for. They need a **single intelligent assistant** that understands their schedule, their hunger, their deadlines, and their GPA — and proactively surfaces what matters, exactly when it matters.

- A student with 72% attendance gets a red warning badge **without asking**.
- Lunch menu appears on the dashboard at noon **without navigating anywhere**.
- The next class is always visible, pulling from their specific department's real timetable.
- JARVIS — the conversational AI brain — connects the dots between all data sources so the student only needs to ask naturally: *"Do I have any labs today?"*

This is Customer Obsession in code: we removed every unnecessary step between the student and the answer.

#### 2. Invent and Simplify
Campus information is notoriously fragmented — timetables on notice boards, menus on WhatsApp groups, events on posters. CampusFlow replaces this chaos with a radical simplification:

- **One SQLite database** as the single source of truth for all campus data.
- **One Streamlit interface** combining dashboard, schedule, events, and chat.
- **One AI model (Gemini)** that contextualizes all of this and responds conversationally.
- **Zero cloud infrastructure** required for the prototype — runs entirely on a laptop.

We didn't build complex microservices or require institutional IT buy-in. We invented a lean, local-first architecture that any campus can deploy in minutes — and that any student can start using without training.

---

## 🚀 Features

| Feature | Description |
|---|---|
| **Live Status Dashboard** | Real-time clock, next class, current mess menu, attendance alert, and nearest deadline — all on one screen |
| **JARVIS Chatbot** | Gemini 1.5 Flash–powered assistant with campus DB context injection |
| **Smart DB Queries** | App detects intent (food / class / event) and fetches the right DB rows before calling the AI |
| **Student Profile Portal** | Sidebar form to save/update Name, Dept, Semester, GPA, and Attendance |
| **Full Timetable View** | Expandable today's schedule for CSE, ECE, and MECH departments |
| **Events & Deadlines Feed** | Color-coded upcoming events: hackathons, exams, assignments, workshops |
| **Attendance Warning** | Visual badge turns red with explicit warning when attendance drops below 75% |
| **Secure API Key Input** | Password-type Streamlit input — no keys ever hardcoded |

---

## 🗄️ Database Schema

### `student_profile`
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| name | TEXT | Student full name |
| department | TEXT | CSE / ECE / MECH |
| semester | INTEGER | 1–8 |
| gpa | REAL | Current GPA |
| attendance | REAL | Attendance % |
| registered_events | TEXT | Comma-separated event names |

### `timetables`
| Column | Type | Description |
|---|---|---|
| department | TEXT | CSE / ECE / MECH |
| day | TEXT | Monday – Saturday |
| time_slot | TEXT | e.g. "09:00 AM - 10:00 AM" |
| subject | TEXT | Subject name |
| room | TEXT | Room / lab number |

### `mess_menu`
| Column | Type | Description |
|---|---|---|
| day | TEXT | Monday – Sunday |
| meal_type | TEXT | Breakfast / Lunch / Snacks / Dinner |
| time_window | TEXT | e.g. "12:00 PM - 02:00 PM" |
| menu_items | TEXT | Full menu description |

### `college_events`
| Column | Type | Description |
|---|---|---|
| event_name | TEXT | Event title |
| event_type | TEXT | Hackathon / Exam / Assignment / Workshop / etc. |
| due_date | TEXT | YYYY-MM-DD |
| description | TEXT | Full event description |
| venue | TEXT | Location |
| organizer | TEXT | Organizing body |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend / UI** | Streamlit 1.x (Python 3.12) |
| **Database** | SQLite (`campus.db`) |
| **AI Brain** | Google Gemini 1.5 Flash via `google-generativeai` SDK |
| **Styling** | Custom CSS injected via `st.markdown` |
| **Runtime** | Python 3.12, local virtual environment |

---

## ⚙️ Setup & Run

### Prerequisites
- Python 3.12
- A Google Gemini API key (free at [aistudio.google.com](https://aistudio.google.com/))

### 1. Activate the virtual environment
```bash
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install streamlit google-generativeai
```

### 3. Initialize the database
```bash
python3.12 init_db.py
```
This creates `campus.db` and seeds all tables with realistic engineering college mock data.

### 4. Launch the app
```bash
streamlit run app.py
```

### 5. Configure in the UI
- Open `http://localhost:8501` in your browser
- Paste your Gemini API key in the sidebar
- Update your student profile
- Start chatting with JARVIS!

---

## 💬 Example Jarvis Conversations

```
You: What's for lunch today?
JARVIS: Today's lunch (12:00 PM – 2:00 PM) is looking solid:
        Steamed Rice, Rajma Masala, Aloo Gobi Sabzi, Dal Tadka,
        Chapati (3), Cucumber Raita, Papad, and Pickle. Fuel up! 🍛

You: Do I have any classes after 2 PM?
JARVIS: Yes! You have Software Engineering Lab from 2:00 PM – 5:00 PM
        in CS-LAB-1. Don't forget your lab record book.

You: Any hackathons coming up?
JARVIS: Three hackathons on the radar:
        1. Hackathon 3.0 (July 5) — Smart Campus theme, ₹1.5L prizes
        2. CodeStorm (July 20) — AI & Sustainability focus
        3. BuildWith AWS (Aug 10) — Serverless/ML on AWS
        Want me to help you pick one based on your skills?
```

---

## 📁 Project Structure

```
campusflow/
├── .venv/              # Python 3.12 virtual environment
├── app.py              # Main Streamlit application
├── init_db.py          # Database initialization & seeding script
├── campus.db           # SQLite database (auto-generated)
└── README.md           # This file
```

---

## 🔮 Roadmap (Post-Hackathon)

- [ ] Push notification for class reminders (5 min before)
- [ ] Smart attendance predictor ("you need to attend 8 more classes to hit 75%")
- [ ] Peer chat / study group matching
- [ ] Faculty announcement feed integration
- [ ] Mobile-first PWA wrapper
- [ ] College ERP API integration (replace manual profile entry)
- [ ] Multi-user support with login system

---

## 🙏 Credits

Built with ❤️ for the Amazon Hackathon.
Powered by Google Gemini, Streamlit, and the vision that every student deserves a campus AI as smart as Jarvis.

---

*"Any sufficiently advanced campus OS is indistinguishable from magic."*
