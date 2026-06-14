"""
CampusFlow v2 — Multi-tenant AI Operating System for Student Life.
Architecture: auth gate -> per-user dashboard + BLACKY chatbot.
"""

import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

import db
from auth import render_auth_page

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# ─────────────────────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="CampusFlow",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# Global CSS — black/white professional
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main .block-container {
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
    background-color: #0a0a0a !important;
    color: #e8e8e8 !important;
}
[data-testid="stSidebar"] > div:first-child {
    background-color: #111111 !important;
    border-right: 1px solid #2a2a2a !important;
}
#MainMenu, footer { visibility: hidden; }

/* ── Typography helpers ── */
.brand-name        { font-size:1.25rem; font-weight:700; color:#ffffff; letter-spacing:.03em; }
.brand-name span   { color:#777777; }
.brand-tag         { font-size:.6rem; letter-spacing:.2em; text-transform:uppercase; color:#444444; margin-top:2px; }
.section-label     { font-size:.6rem; font-weight:600; letter-spacing:.22em; text-transform:uppercase;
                     color:#555555; padding-bottom:6px; border-bottom:1px solid #222222; margin:18px 0 12px; }
.sidebar-footer    { font-size:.6rem; color:#333333; text-align:center; letter-spacing:.08em; }

/* ── Profile card ── */
.profile-card      { background:#161616; border:1px solid #2a2a2a; border-radius:8px;
                     padding:14px 16px; font-size:.82rem; line-height:1.85; color:#aaaaaa; }
.profile-card strong { color:#e8e8e8; }
.att-warn          { color:#cc3333; font-weight:600; }
.att-ok            { color:#448844; font-weight:600; }

/* ── Header bar ── */
.header-bar        { background:#111111; border:1px solid #2a2a2a; border-radius:10px;
                     padding:18px 26px; display:flex; align-items:center; gap:18px; margin-bottom:16px; }
.ai-badge          { width:48px; height:48px; background:#1a1a1a; border:1px solid #333333;
                     border-radius:8px; display:flex; align-items:center; justify-content:center;
                     font-family:'Inter',monospace; font-size:.85rem; font-weight:700;
                     color:#ffffff; letter-spacing:.04em; flex-shrink:0; }
.header-title      { font-size:1.1rem; font-weight:700; color:#ffffff; }
.header-sub        { font-size:.78rem; color:#555555; margin-top:3px; }
.status-online     { color:#448844; }
.status-offline    { color:#cc3333; }

/* ── Clock ── */
.clock-card        { background:#111111; border:1px solid #2a2a2a; border-radius:10px;
                     padding:16px; text-align:center; }
.clock-time        { font-size:1.6rem; font-weight:700; color:#ffffff;
                     font-variant-numeric:tabular-nums; letter-spacing:.04em; }
.clock-day         { font-size:.8rem; color:#666666; margin-top:3px; }
.clock-date        { font-size:.68rem; color:#444444; margin-top:2px; }

/* ── Stat cards ── */
.stat-card         { background:#111111; border:1px solid #2a2a2a; border-top:2px solid #333333;
                     border-radius:10px; padding:16px; min-height:130px; }
.stat-label        { font-size:.6rem; font-weight:600; letter-spacing:.2em; text-transform:uppercase;
                     color:#555555; margin-bottom:10px; }
.stat-value        { font-size:.97rem; font-weight:600; color:#e8e8e8; line-height:1.35; }
.stat-meta         { font-size:.72rem; color:#555555; margin-top:6px; line-height:1.55; }

/* ── Alert card (attendance warning) ── */
.alert-card        { background:#1a0808; border:1px solid #551111; border-left:3px solid #cc3333;
                     border-radius:8px; padding:14px 16px; margin:5px 0; }
.alert-title       { font-size:.72rem; font-weight:600; color:#cc3333;
                     letter-spacing:.1em; text-transform:uppercase; margin-bottom:8px; }
.alert-row         { font-size:.82rem; color:#ddaaaa; line-height:1.7; }
.alert-pct         { color:#cc3333; font-weight:700; }

/* ── Calendar badge ── */
.cal-badge         { display:inline-block; font-size:.7rem; padding:4px 12px;
                     border-radius:4px; font-weight:500; margin-bottom:12px; }
.cal-working       { background:#0d1a0d; color:#448844; border:1px solid #1a3a1a; }
.cal-holiday       { background:#1a0d0d; color:#cc3333; border:1px solid #3a1a1a; }
.cal-weekend       { background:#161616; color:#888888; border:1px solid #2a2a2a; }

/* ── Tags ── */
.tag               { display:inline-block; font-size:.58rem; font-weight:600;
                     letter-spacing:.1em; text-transform:uppercase; padding:2px 8px;
                     border-radius:3px; margin-top:8px; border:1px solid #333333;
                     color:#888888; background:#161616; }
.tag-warn          { border-color:#551111; color:#cc3333; background:#1a0808; }
.tag-ok            { border-color:#1a3a1a; color:#448844; background:#0a160a; }
.tag-info          { border-color:#333333; color:#aaaaaa; background:#161616; }

/* ── Schedule table ── */
.tbl-row           { display:grid; grid-template-columns:2fr 3fr 1fr; gap:12px;
                     padding:9px 4px; border-bottom:1px solid #1a1a1a; align-items:center; }
.tbl-row:last-child { border-bottom:none; }
.tbl-head          { font-size:.58rem; font-weight:600; letter-spacing:.18em;
                     text-transform:uppercase; color:#444444; }
.tbl-time          { font-size:.82rem; color:#cccccc; font-weight:500; }
.tbl-subj          { font-size:.82rem; color:#e8e8e8; }
.tbl-room          { font-size:.76rem; color:#666666; }

/* ── Event rows ── */
.event-row         { background:#111111; border:1px solid #222222; border-left:2px solid #444444;
                     border-radius:6px; padding:12px 16px; margin:5px 0;
                     display:flex; justify-content:space-between; align-items:flex-start; gap:14px; }
.event-name        { font-size:.86rem; font-weight:600; color:#e8e8e8; }
.event-desc        { font-size:.74rem; color:#555555; margin-top:3px; line-height:1.45; }
.event-meta        { font-size:.68rem; color:#444444; margin-top:4px; }
.event-date        { font-size:.7rem; color:#aaaaaa; white-space:nowrap; flex-shrink:0; font-weight:500; }

/* ── Marks table ── */
.marks-row         { display:grid; grid-template-columns:3fr 2fr 1fr 1fr; gap:10px;
                     padding:8px 4px; border-bottom:1px solid #1a1a1a; align-items:center;
                     font-size:.82rem; }
.marks-row:last-child { border-bottom:none; }
.marks-subj        { color:#e8e8e8; }
.marks-exam        { color:#888888; font-size:.76rem; }
.marks-score       { color:#cccccc; font-weight:500; }
.marks-pct         { font-weight:600; }
.marks-pct-hi      { color:#448844; }
.marks-pct-mid     { color:#ccaa44; }
.marks-pct-lo      { color:#cc3333; }

/* ── Chat ── */
.chat-wrap         { margin:8px 0; }
.msg-label         { font-size:.58rem; font-weight:600; letter-spacing:.18em;
                     text-transform:uppercase; margin-bottom:5px; }
.msg-label-user    { color:#aaaaaa; }
.msg-label-ai      { color:#666666; }
.msg-user          { background:#161616; border:1px solid #2a2a2a;
                     border-radius:10px 10px 2px 10px; padding:12px 16px;
                     margin-left:40px; font-size:.86rem; color:#e8e8e8; line-height:1.65; }
.msg-ai            { background:#0f0f0f; border:1px solid #222222;
                     border-radius:10px 10px 10px 2px; padding:12px 16px;
                     margin-right:40px; font-size:.86rem; color:#cccccc;
                     line-height:1.75; white-space:pre-wrap; }

/* ── Leave form ── */
.leave-row         { background:#111111; border:1px solid #222222; border-radius:6px;
                     padding:10px 14px; margin:4px 0; font-size:.82rem;
                     display:flex; justify-content:space-between; align-items:center; }
.leave-date        { color:#aaaaaa; font-weight:500; }
.leave-reason      { color:#888888; font-size:.78rem; flex:1; padding:0 12px; }
.status-approved   { color:#448844; font-size:.7rem; font-weight:600; }
.status-pending    { color:#cc9933; font-size:.7rem; font-weight:600; }

::-webkit-scrollbar       { width:4px; height:4px; }
::-webkit-scrollbar-track { background:#0a0a0a; }
::-webkit-scrollbar-thumb { background:#2a2a2a; border-radius:2px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Auth gate — blocks everything until logged in
# ─────────────────────────────────────────────────────────────────────────────

render_auth_page()

# ─────────────────────────────────────────────────────────────────────────────
# Gemini call
# ─────────────────────────────────────────────────────────────────────────────

def query_blacky(api_key: str, user_msg: str, context: str,
                 history: list[dict]) -> str:
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        system_prompt = (
            "You are BLACKY, the AI assistant embedded in CampusFlow — a campus operating system "
            "for engineering students.\n\n"
            "You have COMPLETE ACCESS to the following data. Use ALL of it to answer any question:\n"
            "- Student's subject-wise attendance counts and percentages\n"
            "- Student's internal exam marks across all subjects\n"
            "- Student's leave history (dates, reasons, approval status)\n"
            "- FULL WEEKLY class schedule (every day, not just today)\n"
            "- FULL WEEKLY mess menu (every day, every meal, not just today)\n"
            "- ALL upcoming campus events, hackathons, exams, deadlines and workshops\n"
            "- Today's date, day and time, plus the college calendar status\n\n"
            "You can answer questions about:\n"
            "  - Any day's schedule: 'What classes do I have on Thursday?'\n"
            "  - Any future meal: 'What is for dinner on Saturday?'\n"
            "  - Any event: 'When is Sports Day?', 'List all hackathons'\n"
            "  - Attendance safety: 'Am I safe to take a leave this Friday?'\n"
            "  - Academic performance: 'What are my marks in Machine Learning?'\n"
            "  - Planning: 'What is happening next month?'\n\n"
            "Tone: Professional, direct, and supportive. Like a knowledgeable academic advisor.\n\n"
            "Rules:\n"
            "- Use ONLY the DATABASE CONTEXT provided. Never fabricate marks, attendance, or dates.\n"
            "- For attendance safety questions, calculate exactly: "
            "classes_needed = ceil(0.75 * (total + future_classes) - attended)\n"
            "- Format multi-item answers as short bullet lists.\n"
            "- If the student has no records yet, gracefully guide them.\n"
            "- Address the student by their first name.\n"
            "- Never say you only know about today — you have the full weekly data."
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
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def pct_color_class(pct: float) -> str:
    if pct >= 85:
        return "marks-pct-hi"
    if pct >= 60:
        return "marks-pct-mid"
    return "marks-pct-lo"


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────

user = st.session_state.user   # guaranteed set by render_auth_page

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

    # ── Logged-in user summary ──
    st.markdown('<div class="section-label">Logged In As</div>', unsafe_allow_html=True)

    att_records = db.get_attendance(user["id"])
    overall_att = db.get_overall_attendance(user["id"])
    low_att     = db.get_low_attendance(user["id"])
    avg_int     = db.get_average_internal_marks(user["id"])

    att_cls  = "att-warn" if overall_att < 75 else "att-ok"
    avg_disp = f"{avg_int}%" if avg_int is not None else "No data"

    st.markdown(f"""
    <div class="profile-card">
        <strong>{user['name']}</strong><br>
        {user['department']} &mdash; Semester {user['semester']}<br>
        Overall Attendance: <span class="{att_cls}">{overall_att}%</span><br>
        Avg Internal Marks: <strong>{avg_disp}</strong>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Leave application ──
    st.markdown('<div class="section-label">Apply for Leave</div>', unsafe_allow_html=True)
    with st.form("leave_form", border=False):
        l_date   = st.date_input("Leave Date")
        l_reason = st.text_input("Reason", placeholder="Brief reason for leave")
        if st.form_submit_button("Submit Application", use_container_width=True):
            if l_reason.strip():
                ok, msg = db.apply_leave(user["id"], str(l_date), l_reason.strip())
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)
            else:
                st.warning("Please enter a reason.")

    st.divider()

    # ── Sign out ──
    if st.button("Sign Out", use_container_width=True):
        st.session_state.user     = None
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        '<div class="sidebar-footer">CampusFlow v2.0 &nbsp;&bull;&nbsp; Powered by Gemini</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Live time context
# ─────────────────────────────────────────────────────────────────────────────

now        = datetime.now()
day_name   = now.strftime("%A")
date_str   = now.strftime("%B %d, %Y")
time_str   = now.strftime("%I:%M %p")
today_iso  = now.strftime("%Y-%m-%d")
hour       = now.hour
greeting   = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"
first_name = user["name"].split()[0]


# ─────────────────────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────────────────────

col_hdr, col_clock = st.columns([3, 1], gap="medium")

with col_hdr:
    online_cls = "status-online"  if api_key else "status-offline"
    online_txt = "Online"         if api_key else "Offline — no API key"

    st.markdown(f"""
    <div class="header-bar">
        <div class="ai-badge">BK</div>
        <div>
            <div class="header-title">BLACKY &mdash; CampusFlow AI</div>
            <div class="header-sub">
                {greeting}, {first_name}
                &nbsp;&middot;&nbsp; {user['department']} Department
                &nbsp;&middot;&nbsp; Semester {user['semester']}
                &nbsp;&middot;&nbsp;
                <span class="{online_cls}">{online_txt}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Calendar badge rendered separately — only when data exists
    cal_entry = db.get_calendar_entry(today_iso)
    if cal_entry:
        cal_type = cal_entry["day_type"]
        cal_desc = cal_entry["description"]
        cal_cls  = ("cal-working"  if cal_type == "Working Day"
                    else "cal-holiday" if cal_type == "Official Holiday"
                    else "cal-weekend")
        st.markdown(
            f'<div style="margin-top:-6px;padding-left:4px;">'
            f'<span class="cal-badge {cal_cls}">{cal_type} &mdash; {cal_desc}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

with col_clock:
    st.markdown(f"""
    <div class="clock-card">
        <div class="clock-time">{time_str}</div>
        <div class="clock-day">{day_name}</div>
        <div class="clock-date">{date_str}</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Attendance alert banner
# ─────────────────────────────────────────────────────────────────────────────

if low_att:
    st.markdown('<div class="section-label">Attendance Alert</div>', unsafe_allow_html=True)
    rows_html = "".join(
        f'<div class="alert-row">'
        f'{r["subject_name"]} &mdash; '
        f'<span class="alert-pct">{r["percentage"]}%</span> '
        f'({r["classes_attended"]}/{r["total_classes_conducted"]} classes)'
        f'</div>'
        for r in low_att
    )
    st.markdown(f"""
    <div class="alert-card">
        <div class="alert-title">Subjects Below 75% Attendance</div>
        {rows_html}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Status cards
# ─────────────────────────────────────────────────────────────────────────────

st.markdown('<div class="section-label">Live Campus Status</div>', unsafe_allow_html=True)

next_class      = db.get_next_class(user["department"], day_name, time_str)
current_meal    = db.get_current_meal(day_name, time_str)
upcoming_events = db.get_upcoming_events(3)
avg_int_disp    = f"{avg_int}%" if avg_int is not None else "—"

c1, c2, c3, c4 = st.columns(4, gap="small")

with c1:
    nv = next_class["subject"] if next_class else "No further classes today"
    nm = f"{next_class['time_slot']}<br>Room {next_class['room']}" if next_class else ""
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Next Class</div>
        <div class="stat-value">{nv}</div>
        <div class="stat-meta">{nm}</div>
    </div>""", unsafe_allow_html=True)

with c2:
    mv = current_meal["meal_type"]  if current_meal else "Mess Closed"
    mm = (f"{current_meal['time_window']}<br>{current_meal['menu_items'][:55]}..."
          if current_meal else "No active meal service")
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Mess — Current Meal</div>
        <div class="stat-value">{mv}</div>
        <div class="stat-meta">{mm}</div>
    </div>""", unsafe_allow_html=True)

with c3:
    att_tag = (
        '<span class="tag tag-warn">Below Minimum</span>'
        if overall_att < 75 else
        '<span class="tag tag-ok">Satisfactory</span>'
    )
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Overall Attendance</div>
        <div class="stat-value">{overall_att}%</div>
        <div class="stat-meta">Minimum required: 75%</div>
        {att_tag}
    </div>""", unsafe_allow_html=True)

with c4:
    ev = upcoming_events[0] if upcoming_events else None
    en = ev["event_name"] if ev else "No upcoming events"
    ed = ev["due_date"]   if ev else ""
    et = ev["event_type"] if ev else ""
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Nearest Deadline</div>
        <div class="stat-value" style="font-size:.88rem;">{en}</div>
        <div class="stat-meta">{ed}</div>
        <span class="tag tag-info">{et}</span>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Detailed panels (expanders)
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("")

exp1, exp2, exp3, exp4, exp5 = st.tabs([
    "Schedule",
    "Attendance",
    "Academic Marks",
    "Leave History",
    "Events & Deadlines",
])

# ── Schedule ──
with exp1:
    schedule = db.get_today_schedule(user["department"], day_name)
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

# ── Attendance ──
with exp2:
    if att_records:
        st.markdown("""
        <div class="tbl-row" style="grid-template-columns:3fr 1fr 1fr 1fr;">
            <span class="tbl-head">Subject</span>
            <span class="tbl-head">Attended</span>
            <span class="tbl-head">Total</span>
            <span class="tbl-head">Percentage</span>
        </div>""", unsafe_allow_html=True)
        for r in att_records:
            pct_cls  = "att-warn" if r["percentage"] < 75 else "att-ok"
            warn_txt = " (low)" if r["percentage"] < 75 else ""
            st.markdown(f"""
        <div class="tbl-row" style="grid-template-columns:3fr 1fr 1fr 1fr;">
            <span class="tbl-subj">{r['subject_name']}</span>
            <span class="tbl-time">{r['classes_attended']}</span>
            <span class="tbl-room">{r['total_classes_conducted']}</span>
            <span class="{pct_cls}" style="font-size:.82rem;font-weight:600;">
                {r['percentage']}%{warn_txt}
            </span>
        </div>""", unsafe_allow_html=True)
    else:
        st.caption("No attendance records found for your account.")

# ── Academic Marks ──
with exp3:
    marks = db.get_marks(user["id"])
    if marks:
        avg_disp2 = f"{avg_int}%" if avg_int is not None else "—"
        st.caption(f"Average Internal Marks: {avg_disp2}")
        st.markdown("""
        <div class="marks-row">
            <span class="tbl-head">Subject</span>
            <span class="tbl-head">Exam</span>
            <span class="tbl-head">Score</span>
            <span class="tbl-head">Percentage</span>
        </div>""", unsafe_allow_html=True)
        for r in marks:
            pcls = pct_color_class(r["percentage"])
            st.markdown(f"""
        <div class="marks-row">
            <span class="marks-subj">{r['subject_name']}</span>
            <span class="marks-exam">{r['exam_type']}</span>
            <span class="marks-score">{int(r['marks_obtained'])}/{int(r['total_marks'])}</span>
            <span class="marks-pct {pcls}">{r['percentage']}%</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.caption("No marks recorded for your account yet.")

# ── Leave History ──
with exp4:
    leaves = db.get_leaves(user["id"])
    if leaves:
        for lv in leaves:
            s_cls = "status-approved" if lv["status"] == "Approved" else "status-pending"
            st.markdown(f"""
        <div class="leave-row">
            <span class="leave-date">{lv['leave_date']}</span>
            <span class="leave-reason">{lv['reason']}</span>
            <span class="{s_cls}">{lv['status']}</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.caption("No leave applications submitted.")

# ── Events & Deadlines ──
with exp5:
    all_events = db.get_upcoming_events(14)
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


# ─────────────────────────────────────────────────────────────────────────────
# BLACKY Chatbot
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(
    '<hr style="border-color:#1e1e1e;margin:24px 0 16px;">',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="section-label">Conversation with BLACKY</div>',
    unsafe_allow_html=True
)

if "messages" not in st.session_state or not st.session_state.messages:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                f"Hello {first_name}. I am BLACKY, your CampusFlow assistant.\n\n"
                "I have access to your complete academic profile: attendance per subject, "
                "internal exam scores, leave history, today's schedule, and upcoming deadlines.\n\n"
                "Ask me anything — from 'Am I safe to take a leave tomorrow?' to "
                "'Which subject needs the most attention?'"
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
    "Ask BLACKY about attendance safety, marks, schedule, deadlines..."
):
    st.session_state.messages.append({"role": "user", "content": prompt})

    if not api_key:
        reply = (
            "BLACKY is offline. Please provide a Gemini API key in the sidebar "
            "or set GEMINI_API_KEY in your .env file."
        )
    else:
        context = db.build_llm_context(prompt, user, day_name, time_str)
        with st.spinner("BLACKY is processing..."):
            reply = query_blacky(api_key, prompt, context, st.session_state.messages)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
