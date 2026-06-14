"""
CampusFlow — AI Operating System for Student Life
BLACKY assistant powered by Google Gemini + SQLite.
"""

import sqlite3
import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

DB_PATH = os.path.join(os.path.dirname(__file__), "campus.db")

st.set_page_config(
    page_title="CampusFlow",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS — black/white professional theme
# Does NOT touch sidebar toggle, collapse arrow, or any Streamlit chrome.
# All native Streamlit controls remain fully functional.
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Reset & base ─────────────────────────────────── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main .block-container {
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
    background-color: #0a0a0a !important;
    color: #e8e8e8 !important;
}

/* ── Sidebar background only — no controls touched ── */
[data-testid="stSidebar"] > div:first-child {
    background-color: #111111 !important;
    border-right: 1px solid #2a2a2a !important;
}

/* ── Hide Streamlit footer/menu ── */
#MainMenu  { visibility: hidden; }
footer     { visibility: hidden; }

/* ── Custom component classes ─────────────────────── */

.brand-name {
    font-size: 1.3rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.03em;
}
.brand-name span { color: #888888; }
.brand-tag {
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #555555;
    margin-top: 2px;
}

.section-label {
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #555555;
    padding-bottom: 6px;
    border-bottom: 1px solid #222222;
    margin: 18px 0 12px;
}

.profile-card {
    background: #161616;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    padding: 14px 16px;
    font-size: 0.82rem;
    line-height: 1.85;
    color: #aaaaaa;
}
.profile-card strong { color: #e8e8e8; }
.att-warn { color: #cc3333; font-weight: 600; }
.att-ok   { color: #448844; font-weight: 600; }
.sidebar-footer {
    font-size: 0.6rem;
    color: #333333;
    text-align: center;
    letter-spacing: 0.08em;
}

/* ── Main header ── */
.header-bar {
    background: #111111;
    border: 1px solid #2a2a2a;
    border-radius: 10px;
    padding: 20px 26px;
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 16px;
}
.ai-badge {
    width: 48px;
    height: 48px;
    background: #1a1a1a;
    border: 1px solid #333333;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Inter', monospace;
    font-size: 0.85rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.04em;
    flex-shrink: 0;
}
.header-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.01em;
}
.header-sub {
    font-size: 0.78rem;
    color: #555555;
    margin-top: 3px;
}
.status-online  { color: #448844; }
.status-offline { color: #cc3333; }

/* ── Clock card ── */
.clock-card {
    background: #111111;
    border: 1px solid #2a2a2a;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    height: 100%;
}
.clock-time {
    font-size: 1.65rem;
    font-weight: 700;
    color: #ffffff;
    font-variant-numeric: tabular-nums;
    letter-spacing: 0.04em;
}
.clock-day  { font-size: 0.8rem;  color: #666666; margin-top: 3px; }
.clock-date { font-size: 0.68rem; color: #444444; margin-top: 2px; }

/* ── Status cards ── */
.stat-card {
    background: #111111;
    border: 1px solid #2a2a2a;
    border-top: 2px solid #333333;
    border-radius: 10px;
    padding: 16px;
    min-height: 130px;
}
.stat-label {
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #555555;
    margin-bottom: 10px;
}
.stat-value {
    font-size: 0.97rem;
    font-weight: 600;
    color: #e8e8e8;
    line-height: 1.35;
}
.stat-meta {
    font-size: 0.72rem;
    color: #555555;
    margin-top: 6px;
    line-height: 1.55;
}
.tag {
    display: inline-block;
    font-size: 0.58rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 3px;
    margin-top: 8px;
    border: 1px solid #333333;
    color: #888888;
    background: #161616;
}
.tag-warn { border-color: #551111; color: #cc3333; background: #1a0a0a; }
.tag-ok   { border-color: #1a3a1a; color: #448844; background: #0a160a; }
.tag-info { border-color: #333333; color: #aaaaaa; background: #161616; }

/* ── Schedule table ── */
.tbl-wrap { margin: 4px 0; }
.tbl-row {
    display: grid;
    grid-template-columns: 2fr 3fr 1fr;
    gap: 12px;
    padding: 9px 4px;
    border-bottom: 1px solid #1a1a1a;
    align-items: center;
}
.tbl-row:last-child { border-bottom: none; }
.tbl-head {
    font-size: 0.58rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #444444;
}
.tbl-time { font-size: 0.82rem; color: #cccccc; font-weight: 500; }
.tbl-subj { font-size: 0.82rem; color: #e8e8e8; }
.tbl-room { font-size: 0.76rem; color: #666666; }

/* ── Event rows ── */
.event-row {
    background: #111111;
    border: 1px solid #222222;
    border-left: 2px solid #444444;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 5px 0;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 14px;
}
.event-name { font-size: 0.86rem; font-weight: 600; color: #e8e8e8; }
.event-desc { font-size: 0.74rem; color: #555555; margin-top: 3px; line-height: 1.45; }
.event-meta { font-size: 0.68rem; color: #444444; margin-top: 4px; }
.event-date { font-size: 0.7rem; color: #aaaaaa; white-space: nowrap; flex-shrink: 0; font-weight: 500; }

/* ── Chat bubbles ── */
.chat-wrap  { margin: 8px 0; }
.msg-label  {
    font-size: 0.58rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 5px;
}
.msg-label-user { color: #aaaaaa; }
.msg-label-ai   { color: #666666; }
.msg-user {
    background: #161616;
    border: 1px solid #2a2a2a;
    border-radius: 10px 10px 2px 10px;
    padding: 12px 16px;
    margin-left: 40px;
    font-size: 0.86rem;
    color: #e8e8e8;
    line-height: 1.65;
}
.msg-ai {
    background: #0f0f0f;
    border: 1px solid #222222;
    border-radius: 10px 10px 10px 2px;
    padding: 12px 16px;
    margin-right: 40px;
    font-size: 0.86rem;
    color: #cccccc;
    line-height: 1.75;
    white-space: pre-wrap;
}

/* ── Divider ── */
.hr-line {
    border: none;
    border-top: 1px solid #1e1e1e;
    margin: 22px 0 16px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar       { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DB helpers
# ─────────────────────────────────────────────────────────────────────────────

def get_conn() -> sqlite3.Connection:
    if not os.path.exists(DB_PATH):
        st.error("campus.db not found — run: python3.12 init_db.py")
        st.stop()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def load_profile() -> dict:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM student_profile LIMIT 1").fetchone()
    return dict(row) if row else {
        "name": "Student", "department": "CSE", "semester": 5,
        "gpa": 8.0, "attendance": 85.0, "registered_events": ""
    }


def save_profile(name, dept, sem, gpa, attendance, events):
    with get_conn() as conn:
        ex = conn.execute("SELECT id FROM student_profile LIMIT 1").fetchone()
        if ex:
            conn.execute(
                "UPDATE student_profile SET name=?,department=?,semester=?,gpa=?,"
                "attendance=?,registered_events=? WHERE id=?",
                (name, dept, sem, gpa, attendance, events, ex["id"])
            )
        else:
            conn.execute(
                "INSERT INTO student_profile (name,department,semester,gpa,attendance,registered_events)"
                " VALUES (?,?,?,?,?,?)",
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
        try:
            start = row["time_slot"].split(" - ")[0].strip()
            if datetime.strptime(start, "%I:%M %p") >= datetime.strptime(current_time, "%I:%M %p"):
                return dict(row)
        except ValueError:
            continue
    return None


def get_current_meal(day, current_time):
    order = {"Breakfast": 0, "Lunch": 1, "Snacks": 2, "Dinner": 3}
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM mess_menu WHERE day=?", (day,)).fetchall()
    now = datetime.strptime(current_time, "%I:%M %p")
    sorted_rows = sorted(rows, key=lambda r: order.get(r["meal_type"], 9))
    for row in sorted_rows:
        parts = row["time_window"].split(" - ")
        if len(parts) == 2:
            try:
                s = datetime.strptime(parts[0].strip(), "%I:%M %p")
                e = datetime.strptime(parts[1].strip(), "%I:%M %p")
                if s <= now <= e:
                    return dict(row)
            except ValueError:
                continue
    for row in sorted_rows:
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


# ─────────────────────────────────────────────────────────────────────────────
# AI helpers
# ─────────────────────────────────────────────────────────────────────────────

def build_context(user_msg: str, profile: dict, day: str, time_str: str) -> str:
    msg   = user_msg.lower()
    parts = [
        f"Student: {profile['name']}, {profile['department']}, Sem {profile['semester']}, "
        f"GPA {profile['gpa']}, Attendance {profile['attendance']}%.",
        f"Current: {day}, {time_str}.",
    ]
    if any(k in msg for k in ["class", "lecture", "schedule", "timetable",
                               "subject", "room", "lab", "next"]):
        sched = get_today_schedule(profile["department"], day)
        if sched:
            lines = [f"  {r['time_slot']} | {r['subject']} | Room {r['room']}" for r in sched]
            parts.append(f"Today's {profile['department']} Schedule:\n" + "\n".join(lines))
        else:
            parts.append(f"No classes today for {profile['department']}.")

    if any(k in msg for k in ["eat", "food", "menu", "mess", "breakfast",
                               "lunch", "dinner", "snack", "meal"]):
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

    if any(k in msg for k in ["event", "hackathon", "fest", "deadline", "exam",
                               "assignment", "workshop", "seminar", "competition",
                               "submit", "upcoming"]):
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
            lines = [
                f"  [{e['event_type']}] {e['event_name']} — {e['due_date']}: {e['description'][:80]}"
                for e in events
            ]
            parts.append("Upcoming Events/Deadlines:\n" + "\n".join(lines))

    return "\n\n".join(parts)


def query_blacky(api_key: str, user_msg: str, context: str,
                 history: list[dict]) -> str:
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        system_prompt = (
            "You are BLACKY, the AI assistant in CampusFlow — a campus OS for engineering students.\n"
            "Tone: Professional, concise, and supportive. Clear and direct, like a knowledgeable senior.\n"
            "You have access to real-time campus data: class schedules, mess menus, events, "
            "and the student's academic profile.\n\n"
            "Guidelines:\n"
            "- Answer using only the DATABASE CONTEXT provided. Never invent data.\n"
            "- Use short bullet lists for multi-item answers.\n"
            "- Address the student by first name when natural.\n"
            "- If attendance is below 75%, note the risk briefly.\n"
            "- For assignments/exams, state the due date and details clearly."
        )

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_prompt,
        )

        gemini_history = []
        for turn in history[:-1]:
            role = "user" if turn["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [turn["content"]]})

        chat     = model.start_chat(history=gemini_history)
        response = chat.send_message(
            f"DATABASE CONTEXT:\n---\n{context}\n---\n\nQuestion: {user_msg}"
        )
        return response.text

    except Exception as e:
        err = str(e)
        if "API_KEY" in err.upper() or "invalid" in err.lower():
            return "Invalid API key. Please verify the key in the sidebar."
        if "quota" in err.lower():
            return "API quota exceeded. Check your Gemini usage limits."
        return f"Error contacting Gemini: {err}"


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="padding:20px 0 8px;">
        <div class="brand-name">Campus<span>Flow</span></div>
        <div class="brand-tag">AI Operating System</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── API Key ──
    st.markdown('<div class="section-label">API Credentials</div>', unsafe_allow_html=True)
    env_key = os.getenv("GEMINI_API_KEY", "")
    if env_key and env_key != "your_gemini_api_key_here":
        st.success("Gemini API key loaded from .env")
        api_key = env_key
    else:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="AIza...",
            help="Paste your key, or set GEMINI_API_KEY in .env",
        )
        if api_key:
            st.caption("Session key active. Add to .env to persist.")
        else:
            st.warning("No API key — BLACKY is offline.")

    st.divider()

    # ── Profile form ──
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
            save_profile(name, dept, int(sem), float(gpa),
                         float(attendance), events_reg)
            st.success("Profile saved.")
            st.rerun()

    st.divider()

    # ── Profile summary ──
    st.markdown('<div class="section-label">Profile Summary</div>', unsafe_allow_html=True)
    profile = load_profile()
    att_cls  = "att-warn" if profile["attendance"] < 75 else "att-ok"
    att_note = "Below minimum (75%)" if profile["attendance"] < 75 else "Above minimum"
    st.markdown(f"""
    <div class="profile-card">
        <strong>{profile['name']}</strong><br>
        {profile['department']} &mdash; Semester {profile['semester']}<br>
        GPA: <strong>{profile['gpa']}</strong><br>
        Attendance: <span class="{att_cls}">{profile['attendance']}% &mdash; {att_note}</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown(
        '<div class="sidebar-footer">CampusFlow v1.0 &nbsp;&bull;&nbsp; Powered by Gemini</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Main content
# ─────────────────────────────────────────────────────────────────────────────

now        = datetime.now()
day_name   = now.strftime("%A")
date_str   = now.strftime("%B %d, %Y")
time_str   = now.strftime("%I:%M %p")
hour       = now.hour
greeting   = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"

profile    = load_profile()
first_name = profile["name"].split()[0]

# ── Header ──
col_hdr, col_clock = st.columns([3, 1], gap="medium")

with col_hdr:
    online_class = "status-online" if api_key else "status-offline"
    online_text  = "Online" if api_key else "Offline — no API key"
    st.markdown(f"""
    <div class="header-bar">
        <div class="ai-badge">BK</div>
        <div>
            <div class="header-title">BLACKY &mdash; CampusFlow AI</div>
            <div class="header-sub">
                {greeting}, {first_name}
                &nbsp;&middot;&nbsp;
                {profile['department']} Department
                &nbsp;&middot;&nbsp;
                Semester {profile['semester']}
                &nbsp;&middot;&nbsp;
                <span class="{online_class}">{online_text}</span>
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

# ── Status cards ──
st.markdown('<div class="section-label">Live Campus Status</div>', unsafe_allow_html=True)

next_class      = get_next_class(profile["department"], day_name, time_str)
current_meal    = get_current_meal(day_name, time_str)
upcoming_events = get_upcoming_events(3)

c1, c2, c3, c4 = st.columns(4, gap="small")

with c1:
    if next_class:
        nv = next_class["subject"]
        nm = f"{next_class['time_slot']}<br>Room {next_class['room']}"
    else:
        nv, nm = "No further classes today", ""
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Next Class</div>
        <div class="stat-value">{nv}</div>
        <div class="stat-meta">{nm}</div>
    </div>""", unsafe_allow_html=True)

with c2:
    if current_meal:
        mv = current_meal["meal_type"]
        mm = f"{current_meal['time_window']}<br>{current_meal['menu_items'][:58]}..."
    else:
        mv, mm = "Mess Closed", "No active meal service"
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Mess — Current Meal</div>
        <div class="stat-value">{mv}</div>
        <div class="stat-meta">{mm}</div>
    </div>""", unsafe_allow_html=True)

with c3:
    att_tag = (
        '<span class="tag tag-warn">Below Minimum</span>'
        if profile["attendance"] < 75
        else '<span class="tag tag-ok">Satisfactory</span>'
    )
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Attendance</div>
        <div class="stat-value">{profile['attendance']}%</div>
        <div class="stat-meta">Minimum required: 75%</div>
        {att_tag}
    </div>""", unsafe_allow_html=True)

with c4:
    if upcoming_events:
        ev = upcoming_events[0]
        en, ed, et = ev["event_name"], ev["due_date"], ev["event_type"]
    else:
        en, ed, et = "No upcoming events", "", ""
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Nearest Deadline</div>
        <div class="stat-value" style="font-size:0.88rem;">{en}</div>
        <div class="stat-meta">{ed}</div>
        <span class="tag tag-info">{et}</span>
    </div>""", unsafe_allow_html=True)

# ── Schedule expander ──
st.markdown("")
with st.expander(f"Today's Schedule — {profile['department']} / {day_name}"):
    schedule = get_today_schedule(profile["department"], day_name)
    if schedule:
        st.markdown("""
        <div class="tbl-wrap">
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
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.caption(f"No classes scheduled on {day_name}.")

# ── Events expander ──
with st.expander("Upcoming Events and Deadlines"):
    all_events = get_upcoming_events(12)
    if all_events:
        for ev in all_events:
            st.markdown(f"""
            <div class="event-row">
                <div style="flex:1;">
                    <div class="event-name">{ev['event_name']}</div>
                    <div class="event-desc">{ev['description'][:110]}...</div>
                    <div class="event-meta">{ev['event_type']} &nbsp;&middot;&nbsp; {ev['venue']}</div>
                </div>
                <div class="event-date">{ev['due_date']}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.caption("No events found.")

# ── Chat ──
st.markdown('<hr class="hr-line">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Conversation with BLACKY</div>',
            unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                f"Hello {first_name}. I am BLACKY, your CampusFlow assistant. "
                "I have access to your timetable, mess menu, upcoming events, "
                "and academic profile. Ask me anything about your day on campus."
            ),
        }
    ]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="chat-wrap">
            <div class="msg-label msg-label-user">You</div>
            <div class="msg-user">{msg['content']}</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-wrap">
            <div class="msg-label msg-label-ai">BLACKY</div>
            <div class="msg-ai">{msg['content']}</div>
        </div>""", unsafe_allow_html=True)

if prompt := st.chat_input(
    "Ask BLACKY about your schedule, meals, events, or deadlines..."
):
    st.session_state.messages.append({"role": "user", "content": prompt})

    if not api_key:
        reply = (
            "BLACKY is offline. Please provide a Gemini API key in the sidebar "
            "or set GEMINI_API_KEY in your .env file."
        )
    else:
        ctx = build_context(prompt, load_profile(), day_name, time_str)
        with st.spinner("BLACKY is processing..."):
            reply = query_blacky(api_key, prompt, ctx, st.session_state.messages)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
