"""
CampusFlow — AI Operating System for Student Life
Conversational campus assistant (BLACKY) powered by Google Gemini + SQLite.
"""

import sqlite3
import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

# Load .env credentials
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

DB_PATH = os.path.join(os.path.dirname(__file__), "campus.db")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CampusFlow",
    page_icon="assets/favicon.png" if os.path.exists("assets/favicon.png") else None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design tokens ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Base */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    background-color: #07111e;
    color: #ccd9e8;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0b1929;
    border-right: 1px solid #172a3f;
}
[data-testid="stSidebar"] * { color: #9ab8d4 !important; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Sidebar brand ── */
.brand-block {
    padding: 24px 0 8px;
    text-align: center;
}
.brand-name {
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    color: #e8f4ff;
}
.brand-name span { color: #3b9eff; }
.brand-tag {
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #3a6a96;
    margin-top: 2px;
}
.divider {
    border: none;
    border-top: 1px solid #172a3f;
    margin: 14px 0;
}

/* ── Section label ── */
.section-label {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #2e5c84;
    margin: 20px 0 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid #172a3f;
}

/* ── Profile summary card ── */
.profile-card {
    background: #0e2035;
    border: 1px solid #1a3a58;
    border-radius: 10px;
    padding: 14px 16px;
    font-size: 0.82rem;
    line-height: 1.8;
    color: #9ab8d4;
}
.profile-card strong { color: #ccd9e8; }
.att-warn { color: #e05c2e; font-weight: 600; }
.att-ok   { color: #27a560; font-weight: 600; }

/* ── Footer note ── */
.sidebar-footer {
    font-size: 0.6rem;
    color: #1e4468;
    text-align: center;
    letter-spacing: 0.08em;
}

/* ── Main header bar ── */
.header-bar {
    background: #0b1929;
    border: 1px solid #172a3f;
    border-radius: 12px;
    padding: 20px 28px;
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 18px;
}
.ai-badge {
    width: 52px;
    height: 52px;
    background: #0e2a48;
    border: 1px solid #1e4a70;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
    font-family: monospace;
    color: #3b9eff;
    font-weight: 700;
    letter-spacing: -1px;
}
.header-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #e8f4ff;
    letter-spacing: 0.01em;
}
.header-sub {
    font-size: 0.8rem;
    color: #4a7ca8;
    margin-top: 2px;
}

/* ── Status cards ── */
.stat-card {
    background: #0b1929;
    border: 1px solid #172a3f;
    border-top: 2px solid #1e5a96;
    border-radius: 10px;
    padding: 18px 16px;
    height: 100%;
    min-height: 120px;
}
.stat-label {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #2e5c84;
    margin-bottom: 10px;
}
.stat-value {
    font-size: 1rem;
    font-weight: 600;
    color: #d4e8ff;
    line-height: 1.35;
}
.stat-meta {
    font-size: 0.72rem;
    color: #4a7ca8;
    margin-top: 6px;
    line-height: 1.5;
}
.tag {
    display: inline-block;
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 4px;
    margin-top: 6px;
}
.tag-warn { background: #2e1208; color: #e05c2e; border: 1px solid #5a2010; }
.tag-ok   { background: #082e1a; color: #27a560; border: 1px solid #104a28; }
.tag-info { background: #0e2040; color: #3b9eff; border: 1px solid #1a4070; }

/* ── Clock card ── */
.clock-card {
    background: #0b1929;
    border: 1px solid #172a3f;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
}
.clock-time {
    font-size: 1.75rem;
    font-weight: 700;
    color: #3b9eff;
    letter-spacing: 0.03em;
    font-variant-numeric: tabular-nums;
}
.clock-day  { font-size: 0.82rem; color: #6a9ec4; margin-top: 2px; }
.clock-date { font-size: 0.7rem;  color: #3a6a96; margin-top: 2px; }

/* ── Table rows (schedule) ── */
.tbl-row {
    display: grid;
    grid-template-columns: 2fr 3fr 1fr;
    gap: 12px;
    padding: 9px 0;
    border-bottom: 1px solid #0e2035;
    font-size: 0.84rem;
    align-items: center;
}
.tbl-row:last-child { border-bottom: none; }
.tbl-head { color: #2e5c84; font-size: 0.62rem; letter-spacing: 0.15em; text-transform: uppercase; }
.tbl-time  { color: #3b9eff; font-weight: 500; }
.tbl-subj  { color: #ccd9e8; }
.tbl-room  { color: #4a7ca8; font-size: 0.78rem; }

/* ── Event rows ── */
.event-row {
    background: #0b1929;
    border: 1px solid #172a3f;
    border-left: 3px solid #1e5a96;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 6px 0;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
}
.event-name { font-size: 0.88rem; font-weight: 600; color: #ccd9e8; }
.event-desc { font-size: 0.76rem; color: #4a7ca8; margin-top: 3px; line-height: 1.4; }
.event-meta { font-size: 0.7rem; color: #2e5c84; margin-top: 4px; }
.event-date { font-size: 0.72rem; color: #3b9eff; white-space: nowrap; flex-shrink: 0; font-weight: 500; }

/* ── Chat messages ── */
.chat-wrap { margin: 6px 0; }
.msg-label {
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.msg-label-user { color: #3b9eff; }
.msg-label-ai   { color: #27a560; }
.msg-user {
    background: #0e2040;
    border: 1px solid #1a3a60;
    border-radius: 10px 10px 2px 10px;
    padding: 12px 16px;
    margin-left: 48px;
    font-size: 0.88rem;
    color: #ccd9e8;
    line-height: 1.6;
}
.msg-ai {
    background: #0b1929;
    border: 1px solid #172a3f;
    border-radius: 10px 10px 10px 2px;
    padding: 12px 16px;
    margin-right: 48px;
    font-size: 0.88rem;
    color: #b8d4e8;
    line-height: 1.7;
}

/* ── Chat input ── */
[data-testid="stChatInput"] > div {
    background: #0b1929 !important;
    border: 1px solid #1a3a58 !important;
    border-radius: 10px !important;
}
[data-testid="stChatInput"] textarea {
    color: #ccd9e8 !important;
    font-size: 0.88rem !important;
}

/* ── Streamlit form/input overrides ── */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] select {
    background: #0e2035 !important;
    border: 1px solid #1a3a58 !important;
    color: #9ab8d4 !important;
    border-radius: 6px !important;
    font-size: 0.84rem !important;
}
[data-testid="stSidebar"] button[kind="formSubmit"] {
    background: #103060 !important;
    border: 1px solid #1e5096 !important;
    color: #e8f4ff !important;
    border-radius: 6px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
}

/* Expander */
[data-testid="stExpander"] {
    background: #0b1929 !important;
    border: 1px solid #172a3f !important;
    border-radius: 10px !important;
}
details summary { color: #6a9ec4 !important; font-size: 0.84rem !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #07111e; }
::-webkit-scrollbar-thumb { background: #1a3a58; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── DB helpers ────────────────────────────────────────────────────────────────

def get_conn() -> sqlite3.Connection:
    if not os.path.exists(DB_PATH):
        st.error("campus.db not found. Run: python3.12 init_db.py")
        st.stop()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def load_profile() -> dict:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM student_profile LIMIT 1").fetchone()
    if row:
        return dict(row)
    return {"name": "Student", "department": "CSE", "semester": 5,
            "gpa": 8.0, "attendance": 85.0, "registered_events": ""}


def save_profile(name, dept, sem, gpa, attendance, events):
    with get_conn() as conn:
        existing = conn.execute("SELECT id FROM student_profile LIMIT 1").fetchone()
        if existing:
            conn.execute(
                "UPDATE student_profile SET name=?,department=?,semester=?,gpa=?,attendance=?,registered_events=? WHERE id=?",
                (name, dept, sem, gpa, attendance, events, existing["id"])
            )
        else:
            conn.execute(
                "INSERT INTO student_profile (name,department,semester,gpa,attendance,registered_events) VALUES (?,?,?,?,?,?)",
                (name, dept, sem, gpa, attendance, events)
            )
        conn.commit()


def get_next_class(dept, day, current_time):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM timetables WHERE department=? AND day=? ORDER BY time_slot",
            (dept, day)
        ).fetchall()
    for row in rows:
        slot_start = row["time_slot"].split(" - ")[0].strip()
        try:
            if datetime.strptime(slot_start, "%I:%M %p") >= datetime.strptime(current_time, "%I:%M %p"):
                return dict(row)
        except ValueError:
            continue
    return None


def get_current_meal(day, current_time):
    order = {"Breakfast": 0, "Lunch": 1, "Snacks": 2, "Dinner": 3}
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM mess_menu WHERE day=?", (day,)).fetchall()
    now = datetime.strptime(current_time, "%I:%M %p")
    for row in sorted(rows, key=lambda r: order.get(r["meal_type"], 9)):
        parts = row["time_window"].split(" - ")
        if len(parts) == 2:
            try:
                if datetime.strptime(parts[0].strip(), "%I:%M %p") <= now <= datetime.strptime(parts[1].strip(), "%I:%M %p"):
                    return dict(row)
            except ValueError:
                continue
    for row in sorted(rows, key=lambda r: order.get(r["meal_type"], 9)):
        parts = row["time_window"].split(" - ")
        if len(parts) == 2:
            try:
                if datetime.strptime(parts[0].strip(), "%I:%M %p") > now:
                    return dict(row)
            except ValueError:
                continue
    return None


def get_today_schedule(dept, day):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM timetables WHERE department=? AND day=? ORDER BY time_slot",
            (dept, day)
        ).fetchall()
    return [dict(r) for r in rows]


def get_upcoming_events(limit=10):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM college_events ORDER BY due_date ASC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_meal_by_type(day, meal_type):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM mess_menu WHERE day=? AND meal_type=? LIMIT 1",
            (day, meal_type)
        ).fetchone()
    return dict(row) if row else None


def get_all_meals_today(day):
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM mess_menu WHERE day=? ORDER BY id", (day,)).fetchall()
    return [dict(r) for r in rows]


def get_events_by_type(event_type):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM college_events WHERE event_type LIKE ? ORDER BY due_date",
            (f"%{event_type}%",)
        ).fetchall()
    return [dict(r) for r in rows]


# ── AI context builder ────────────────────────────────────────────────────────

def build_context(user_msg: str, profile: dict, day: str, time_str: str) -> str:
    msg = user_msg.lower()
    parts = [
        f"Student: {profile['name']}, {profile['department']}, Sem {profile['semester']}, "
        f"GPA {profile['gpa']}, Attendance {profile['attendance']}%.",
        f"Current: {day}, {time_str}.",
    ]

    if any(k in msg for k in ["class", "lecture", "schedule", "timetable", "subject", "room", "lab", "next"]):
        sched = get_today_schedule(profile["department"], day)
        if sched:
            lines = [f"  {r['time_slot']} | {r['subject']} | Room {r['room']}" for r in sched]
            parts.append(f"Today's {profile['department']} Schedule:\n" + "\n".join(lines))
        else:
            parts.append(f"No classes today for {profile['department']}.")

    if any(k in msg for k in ["eat", "food", "menu", "mess", "breakfast", "lunch", "dinner", "snack", "meal"]):
        if "breakfast" in msg:
            meal = get_meal_by_type(day, "Breakfast")
        elif "lunch" in msg:
            meal = get_meal_by_type(day, "Lunch")
        elif "dinner" in msg:
            meal = get_meal_by_type(day, "Dinner")
        elif "snack" in msg:
            meal = get_meal_by_type(day, "Snacks")
        else:
            meal = get_current_meal(day, time_str)
        if meal:
            parts.append(f"Mess — {meal['meal_type']} ({meal['time_window']}): {meal['menu_items']}")
        else:
            meals = get_all_meals_today(day)
            if meals:
                lines = [f"  {m['meal_type']} ({m['time_window']}): {m['menu_items']}" for m in meals]
                parts.append("Today's Mess Menu:\n" + "\n".join(lines))

    if any(k in msg for k in ["event", "hackathon", "fest", "deadline", "exam", "assignment",
                               "workshop", "seminar", "competition", "submit", "upcoming"]):
        if "hackathon" in msg:
            events = get_events_by_type("Hackathon")
        elif "exam" in msg:
            events = get_events_by_type("Exam")
        elif "assignment" in msg or "submit" in msg:
            events = get_events_by_type("Assignment")
        elif "workshop" in msg:
            events = get_events_by_type("Workshop")
        else:
            events = get_upcoming_events(8)
        if events:
            lines = [f"  [{e['event_type']}] {e['event_name']} — {e['due_date']}: {e['description'][:80]}" for e in events]
            parts.append("Upcoming Events/Deadlines:\n" + "\n".join(lines))

    return "\n\n".join(parts)


# ── Gemini call ───────────────────────────────────────────────────────────────

def query_blacky(api_key: str, user_msg: str, context: str, history: list[dict]) -> str:
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        system_prompt = """You are BLACKY, the AI assistant embedded in CampusFlow — a campus operating system for engineering students.
Tone: Professional, concise, and supportive. No excessive enthusiasm. Think of a knowledgeable senior who gives clear, direct answers.
You have access to real-time campus data: class schedules, mess menus, events, and the student's academic profile.

Guidelines:
- Answer using only the DATABASE CONTEXT provided. Never invent class times, menu items, or event dates.
- Keep responses structured and readable. Use short bullet lists for multi-item answers.
- Address the student by first name when it adds warmth.
- If attendance is below 75%, note the risk briefly but don't lecture.
- When asked about assignments or exams, state the due date and description clearly."""

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_prompt,
        )

        gemini_history = []
        for turn in history[:-1]:
            role = "user" if turn["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [turn["content"]]})

        chat = model.start_chat(history=gemini_history)
        full_prompt = f"DATABASE CONTEXT:\n---\n{context}\n---\n\nQuestion: {user_msg}"
        response = chat.send_message(full_prompt)
        return response.text

    except Exception as e:
        err = str(e)
        if "API_KEY" in err.upper() or "invalid" in err.lower():
            return "Invalid API key. Please verify the key entered in the sidebar."
        if "quota" in err.lower():
            return "API quota exceeded. Check your Gemini usage limits."
        return f"Error contacting Gemini: {err}"


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div class="brand-block">
        <div class="brand-name">Campus<span>Flow</span></div>
        <div class="brand-tag">AI Operating System</div>
    </div>
    <hr class="divider">
    """, unsafe_allow_html=True)

    # API Key — load from .env, allow sidebar override
    env_key = os.getenv("GEMINI_API_KEY", "")
    st.markdown('<div class="section-label">API Credentials</div>', unsafe_allow_html=True)

    if env_key and env_key != "your_gemini_api_key_here":
        st.success("Gemini API key loaded from .env", icon=None)
        api_key = env_key
    else:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="AIza...",
            help="Paste key here, or add GEMINI_API_KEY to .env",
        )
        if api_key:
            st.caption("Key active for this session only. Add to .env to persist.")
        else:
            st.warning("No API key — BLACKY is offline.")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Student Profile</div>', unsafe_allow_html=True)

    profile_db = load_profile()

    with st.form("profile_form", border=False):
        name = st.text_input("Full Name", value=profile_db["name"])
        dept = st.selectbox(
            "Department",
            ["CSE", "ECE", "MECH"],
            index=["CSE", "ECE", "MECH"].index(profile_db["department"]),
        )
        sem = st.number_input("Semester", min_value=1, max_value=8,
                              value=int(profile_db["semester"]))
        gpa = st.number_input("GPA (out of 10)", min_value=0.0, max_value=10.0,
                              step=0.1, value=float(profile_db["gpa"]))
        attendance = st.slider("Attendance %", 0.0, 100.0,
                               value=float(profile_db["attendance"]), step=0.5)
        events_reg = st.text_area(
            "Registered Events",
            value=profile_db.get("registered_events", ""),
            height=60,
            placeholder="e.g. TechFest, Hackathon 3.0",
        )
        if st.form_submit_button("Save Profile", use_container_width=True):
            save_profile(name, dept, int(sem), float(gpa), float(attendance), events_reg)
            st.success("Profile saved.")
            st.rerun()

    profile = load_profile()
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Profile Summary</div>', unsafe_allow_html=True)

    att_class = "att-warn" if profile["attendance"] < 75 else "att-ok"
    att_note  = "Below minimum (75%)" if profile["attendance"] < 75 else "Above minimum (75%)"
    st.markdown(f"""
    <div class="profile-card">
        <strong>{profile['name']}</strong><br>
        {profile['department']} &mdash; Semester {profile['semester']}<br>
        GPA: <strong>{profile['gpa']}</strong><br>
        Attendance: <span class="{att_class}">{profile['attendance']}% &mdash; {att_note}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-footer">CampusFlow v1.0 &nbsp;&bull;&nbsp; Powered by Gemini</div>',
                unsafe_allow_html=True)


# ── Main ──────────────────────────────────────────────────────────────────────

now        = datetime.now()
day_name   = now.strftime("%A")
date_str   = now.strftime("%B %d, %Y")
time_str   = now.strftime("%I:%M %p")
hour       = now.hour
greeting   = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"

profile    = load_profile()
first_name = profile["name"].split()[0]

# Header
col_main, col_clock = st.columns([3, 1], gap="medium")
with col_main:
    status_dot = "online" if api_key else "offline"
    st.markdown(f"""
    <div class="header-bar">
        <div class="ai-badge">BK</div>
        <div>
            <div class="header-title">BLACKY &mdash; CampusFlow AI</div>
            <div class="header-sub">
                {greeting}, {first_name} &nbsp;|&nbsp;
                {profile['department']} Department &nbsp;|&nbsp;
                Semester {profile['semester']} &nbsp;|&nbsp;
                <span style="color:{'#27a560' if api_key else '#e05c2e'};">
                    {'Online' if api_key else 'Offline — no API key'}
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_clock:
    st.markdown(f"""
    <div class="clock-card">
        <div class="clock-time">{time_str}</div>
        <div class="clock-day">{day_name}</div>
        <div class="clock-date">{date_str}</div>
    </div>
    """, unsafe_allow_html=True)

# Status cards
st.markdown('<div class="section-label">Live Campus Status</div>', unsafe_allow_html=True)

next_class     = get_next_class(profile["department"], day_name, time_str)
current_meal   = get_current_meal(day_name, time_str)
upcoming_events = get_upcoming_events(3)

c1, c2, c3, c4 = st.columns(4, gap="small")

with c1:
    if next_class:
        nxt_val  = next_class["subject"]
        nxt_meta = f"{next_class['time_slot']}<br>Room {next_class['room']}"
    else:
        nxt_val  = "No further classes today"
        nxt_meta = ""
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Next Class</div>
        <div class="stat-value">{nxt_val}</div>
        <div class="stat-meta">{nxt_meta}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    if current_meal:
        meal_val  = current_meal["meal_type"]
        meal_meta = f"{current_meal['time_window']}<br>{current_meal['menu_items'][:60]}..."
    else:
        meal_val  = "Mess Closed"
        meal_meta = "No active meal service"
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Mess — Current Meal</div>
        <div class="stat-value">{meal_val}</div>
        <div class="stat-meta">{meal_meta}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    att_val   = f"{profile['attendance']}%"
    att_tag   = '<span class="tag tag-warn">Below Minimum</span>' if profile["attendance"] < 75 \
                else '<span class="tag tag-ok">Satisfactory</span>'
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Attendance</div>
        <div class="stat-value">{att_val}</div>
        <div class="stat-meta">Minimum required: 75%</div>
        {att_tag}
    </div>
    """, unsafe_allow_html=True)

with c4:
    if upcoming_events:
        ev = upcoming_events[0]
        ev_name = ev["event_name"]
        ev_date = ev["due_date"]
        ev_type = ev["event_type"]
    else:
        ev_name = "No upcoming events"
        ev_date = ""
        ev_type = ""
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Nearest Deadline</div>
        <div class="stat-value" style="font-size:0.9rem;">{ev_name}</div>
        <div class="stat-meta">{ev_date}</div>
        <span class="tag tag-info">{ev_type}</span>
    </div>
    """, unsafe_allow_html=True)

# Today's schedule expander
st.markdown("")
with st.expander(f"Today's Schedule — {profile['department']} / {day_name}"):
    schedule = get_today_schedule(profile["department"], day_name)
    if schedule:
        st.markdown("""
        <div class="tbl-row">
            <span class="tbl-head">Time Slot</span>
            <span class="tbl-head">Subject</span>
            <span class="tbl-head">Room</span>
        </div>""", unsafe_allow_html=True)
        for row in schedule:
            st.markdown(f"""
            <div class="tbl-row">
                <span class="tbl-time">{row['time_slot']}</span>
                <span class="tbl-subj">{row['subject']}</span>
                <span class="tbl-room">{row['room']}</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.caption(f"No classes scheduled on {day_name}.")

# Events expander
with st.expander("Upcoming Events and Deadlines"):
    all_events = get_upcoming_events(12)
    type_colors = {
        "Hackathon":     "#4a7eff",
        "Exam":          "#e05c2e",
        "Assignment":    "#c08020",
        "Lab Record":    "#c08020",
        "Workshop":      "#27a560",
        "Tech Fest":     "#3b9eff",
        "Guest Lecture": "#3b9eff",
        "Cultural":      "#a060d0",
        "Sports":        "#20a080",
        "Competition":   "#4a7eff",
        "Research Event":"#3b9eff",
    }
    if all_events:
        for ev in all_events:
            border_color = type_colors.get(ev["event_type"], "#2e5c84")
            st.markdown(f"""
            <div class="event-row" style="border-left-color:{border_color};">
                <div style="flex:1;">
                    <div class="event-name">{ev['event_name']}</div>
                    <div class="event-desc">{ev['description'][:110]}...</div>
                    <div class="event-meta">{ev['event_type']} &nbsp;|&nbsp; {ev['venue']}</div>
                </div>
                <div class="event-date">{ev['due_date']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.caption("No events found.")

# Chat section
st.markdown('<hr style="border-color:#172a3f;margin:24px 0 16px;">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Conversation with BLACKY</div>', unsafe_allow_html=True)

# Init chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                f"Hello {first_name}. I am BLACKY, your CampusFlow assistant. "
                f"I have access to your timetable, mess menu, upcoming events, and academic profile. "
                f"Ask me anything about your day on campus."
            ),
        }
    ]

# Render history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="chat-wrap">
            <div class="msg-label msg-label-user">You</div>
            <div class="msg-user">{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-wrap">
            <div class="msg-label msg-label-ai">BLACKY</div>
            <div class="msg-ai">{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)

# Input
if prompt := st.chat_input("Ask BLACKY about your schedule, meals, events, or deadlines..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    if not api_key:
        reply = (
            "BLACKY is currently offline. Please provide a Gemini API key in the sidebar, "
            "or add GEMINI_API_KEY to your .env file."
        )
    else:
        current_profile = load_profile()
        context = build_context(prompt, current_profile, day_name, time_str)
        with st.spinner("BLACKY is processing..."):
            reply = query_blacky(api_key, prompt, context, st.session_state.messages)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
