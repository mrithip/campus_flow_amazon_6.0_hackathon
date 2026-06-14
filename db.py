"""
CampusFlow — db.py
All database connection logic, schema constants, and query helpers.
Single source of truth for data access across the app.
"""

import sqlite3
import os
import bcrypt
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "campus.db")


# ─────────────────────────────────────────────────────────────────────────────
# Connection
# ─────────────────────────────────────────────────────────────────────────────

def get_conn() -> sqlite3.Connection:
    """Return a row-factory enabled connection. Caller manages lifecycle."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ─────────────────────────────────────────────────────────────────────────────
# Auth helpers
# ─────────────────────────────────────────────────────────────────────────────

def _hash_password(password: str) -> str:
    """bcrypt hash. Work factor 12 — safe for prototype and production."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(12)).decode()


def _verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def register_user(username: str, password: str, name: str,
                  department: str, semester: int) -> tuple[bool, str]:
    """Create a new user. Returns (success, message)."""
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM users WHERE username=?", (username.strip().lower(),)
        ).fetchone()
        if existing:
            return False, "Username already exists. Please choose a different one."
        conn.execute(
            "INSERT INTO users (username, password_hash, name, department, semester) VALUES (?,?,?,?,?)",
            (username.strip().lower(), _hash_password(password),
             name.strip(), department, semester)
        )
        conn.commit()
    return True, "Account created successfully."


def login_user(username: str, password: str) -> dict | None:
    """Validate credentials. Returns user dict or None."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username=?", (username.strip().lower(),)
        ).fetchone()
    if row and _verify_password(password, row["password_hash"]):
        return dict(row)
    return None


def get_user_by_id(user_id: int) -> dict | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    return dict(row) if row else None


# ─────────────────────────────────────────────────────────────────────────────
# Timetable
# ─────────────────────────────────────────────────────────────────────────────

def get_today_schedule(dept: str, day: str) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM timetables WHERE department=? AND day=? ORDER BY time_slot",
            (dept, day)
        ).fetchall()
    return [dict(r) for r in rows]


def get_next_class(dept: str, day: str, current_time: str) -> dict | None:
    for row in get_today_schedule(dept, day):
        try:
            start = row["time_slot"].split(" - ")[0].strip()
            if datetime.strptime(start, "%I:%M %p") >= datetime.strptime(current_time, "%I:%M %p"):
                return row
        except ValueError:
            continue
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Mess menu
# ─────────────────────────────────────────────────────────────────────────────

def get_current_meal(day: str, current_time: str) -> dict | None:
    order = {"Breakfast": 0, "Lunch": 1, "Snacks": 2, "Dinner": 3}
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM mess_menu WHERE day=?", (day,)).fetchall()
    now  = datetime.strptime(current_time, "%I:%M %p")
    srt  = sorted([dict(r) for r in rows], key=lambda r: order.get(r["meal_type"], 9))
    for row in srt:
        parts = row["time_window"].split(" - ")
        if len(parts) == 2:
            try:
                s = datetime.strptime(parts[0].strip(), "%I:%M %p")
                e = datetime.strptime(parts[1].strip(), "%I:%M %p")
                if s <= now <= e:
                    return row
            except ValueError:
                continue
    for row in srt:
        parts = row["time_window"].split(" - ")
        if len(parts) == 2:
            try:
                if datetime.strptime(parts[0].strip(), "%I:%M %p") > now:
                    return row
            except ValueError:
                continue
    return None


def get_meal_by_type(day: str, meal_type: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM mess_menu WHERE day=? AND meal_type=? LIMIT 1",
            (day, meal_type)
        ).fetchone()
    return dict(row) if row else None


def get_all_meals_today(day: str) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM mess_menu WHERE day=? ORDER BY id", (day,)
        ).fetchall()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────────────────────────────────────
# Events
# ─────────────────────────────────────────────────────────────────────────────

def get_upcoming_events(limit: int = 10) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM college_events ORDER BY due_date ASC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_events_by_type(event_type: str) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM college_events WHERE event_type LIKE ? ORDER BY due_date",
            (f"%{event_type}%",)
        ).fetchall()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────────────────────────────────────
# College calendar
# ─────────────────────────────────────────────────────────────────────────────

def get_calendar_entry(date_str: str) -> dict | None:
    """Return calendar entry for a given YYYY-MM-DD date string."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM college_calendar WHERE date=?", (date_str,)
        ).fetchone()
    return dict(row) if row else None


# ─────────────────────────────────────────────────────────────────────────────
# Attendance records (per user)
# ─────────────────────────────────────────────────────────────────────────────

def get_attendance(user_id: int) -> list[dict]:
    """Return all attendance records for a user with computed percentage."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM attendance_records WHERE user_id=? ORDER BY subject_name",
            (user_id,)
        ).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        d["percentage"] = round(
            (d["classes_attended"] / d["total_classes_conducted"] * 100)
            if d["total_classes_conducted"] > 0 else 0.0, 1
        )
        result.append(d)
    return result


def get_low_attendance(user_id: int, threshold: float = 75.0) -> list[dict]:
    return [r for r in get_attendance(user_id) if r["percentage"] < threshold]


def get_overall_attendance(user_id: int) -> float:
    records = get_attendance(user_id)
    if not records:
        return 0.0
    total_c = sum(r["total_classes_conducted"] for r in records)
    total_a = sum(r["classes_attended"] for r in records)
    return round((total_a / total_c * 100) if total_c > 0 else 0.0, 1)


# ─────────────────────────────────────────────────────────────────────────────
# Academic marks (per user)
# ─────────────────────────────────────────────────────────────────────────────

def get_marks(user_id: int) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM academic_marks WHERE user_id=? ORDER BY subject_name, exam_type",
            (user_id,)
        ).fetchall()
    result = []
    for r in rows:
        d = dict(r)
        d["percentage"] = round(
            (d["marks_obtained"] / d["total_marks"] * 100)
            if d["total_marks"] > 0 else 0.0, 1
        )
        result.append(d)
    return result


def get_average_internal_marks(user_id: int) -> float | None:
    """Average percentage across Internal-1 and Internal-2 exams."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT marks_obtained, total_marks FROM academic_marks "
            "WHERE user_id=? AND exam_type IN ('Internal-1','Internal-2')",
            (user_id,)
        ).fetchall()
    if not rows:
        return None
    pcts = [r["marks_obtained"] / r["total_marks"] * 100
            for r in rows if r["total_marks"] > 0]
    return round(sum(pcts) / len(pcts), 1) if pcts else None


def get_upcoming_exams(user_id: int) -> list[dict]:
    """Return exam events that match the user's department."""
    user = get_user_by_id(user_id)
    if not user:
        return []
    dept = user["department"]
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM college_events WHERE event_type='Exam' "
            "AND (event_name LIKE ? OR event_name LIKE ?) "
            "ORDER BY due_date",
            (f"%{dept}%", "%All%")
        ).fetchall()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────────────────────────────────────
# Leave applications (per user)
# ─────────────────────────────────────────────────────────────────────────────

def get_leaves(user_id: int) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM leave_applications WHERE user_id=? ORDER BY leave_date DESC",
            (user_id,)
        ).fetchall()
    return [dict(r) for r in rows]


def apply_leave(user_id: int, leave_date: str, reason: str) -> tuple[bool, str]:
    """Insert a new leave application with Pending status."""
    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO leave_applications (user_id, leave_date, reason, status) VALUES (?,?,?,?)",
                (user_id, leave_date, reason, "Pending")
            )
            conn.commit()
        return True, "Leave application submitted successfully."
    except Exception as e:
        return False, str(e)


# ─────────────────────────────────────────────────────────────────────────────
# Rich LLM context builder
# ─────────────────────────────────────────────────────────────────────────────

def build_llm_context(user_msg: str, user: dict, day: str, time_str: str) -> str:
    """
    Fetch all relevant records for the logged-in user and pack into a
    structured context string for the Gemini model.
    """
    msg   = user_msg.lower()
    uid   = user["id"]
    parts = []

    # ── Identity ──
    parts.append(
        f"STUDENT PROFILE:\n"
        f"  Name: {user['name']}\n"
        f"  Department: {user['department']} | Semester: {user['semester']}\n"
        f"  Current Day: {day} | Time: {time_str}"
    )

    # ── Attendance ──
    att_records = get_attendance(uid)
    if att_records:
        overall = get_overall_attendance(uid)
        low     = get_low_attendance(uid)
        lines   = [f"  {r['subject_name']}: {r['classes_attended']}/{r['total_classes_conducted']} "
                   f"({r['percentage']}%)" for r in att_records]
        att_block = (
            f"ATTENDANCE RECORDS (Overall: {overall}%):\n" + "\n".join(lines)
        )
        if low:
            att_block += "\n  [WARNING] Subjects below 75%: " + \
                         ", ".join(f"{r['subject_name']} ({r['percentage']}%)" for r in low)
        parts.append(att_block)

    # ── Marks ──
    marks = get_marks(uid)
    if marks:
        avg_int = get_average_internal_marks(uid)
        m_lines = [f"  {r['subject_name']} [{r['exam_type']}]: "
                   f"{r['marks_obtained']}/{r['total_marks']} ({r['percentage']}%)"
                   for r in marks]
        parts.append(
            f"ACADEMIC MARKS (Avg internals: {avg_int}%):\n" + "\n".join(m_lines)
        )

    # ── Leaves ──
    leaves = get_leaves(uid)
    if leaves:
        l_lines = [f"  {l['leave_date']} — {l['reason']} [{l['status']}]" for l in leaves]
        parts.append("LEAVE HISTORY:\n" + "\n".join(l_lines))

    # ── Timetable ──
    if any(k in msg for k in ["class", "lecture", "schedule", "timetable",
                               "subject", "room", "lab", "next"]):
        sched = get_today_schedule(user["department"], day)
        if sched:
            s_lines = [f"  {r['time_slot']} | {r['subject']} | Room {r['room']}"
                       for r in sched]
            parts.append(f"TODAY'S {user['department']} SCHEDULE:\n" + "\n".join(s_lines))
        else:
            parts.append(f"No classes scheduled today for {user['department']}.")

    # ── Mess menu ──
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
            parts.append(
                f"MESS — {meal['meal_type']} ({meal['time_window']}):\n  {meal['menu_items']}"
            )
        else:
            all_meals = get_all_meals_today(day)
            if all_meals:
                m_lines = [f"  {m['meal_type']} ({m['time_window']}): {m['menu_items']}"
                           for m in all_meals]
                parts.append("TODAY'S MESS MENU:\n" + "\n".join(m_lines))

    # ── Events / deadlines ──
    if any(k in msg for k in ["event", "hackathon", "fest", "deadline", "exam",
                               "assignment", "workshop", "seminar", "competition",
                               "submit", "upcoming", "leave", "safe"]):
        if "hackathon" in msg:
            events = get_events_by_type("Hackathon")
        elif "exam" in msg:
            events = get_upcoming_exams(uid)
            if not events:
                events = get_events_by_type("Exam")
        elif "assignment" in msg or "submit" in msg:
            events = get_events_by_type("Assignment")
        elif "workshop" in msg:
            events = get_events_by_type("Workshop")
        else:
            events = get_upcoming_events(8)
        if events:
            e_lines = [
                f"  [{e['event_type']}] {e['event_name']} — {e['due_date']}: "
                f"{e['description'][:80]}"
                for e in events
            ]
            parts.append("UPCOMING EVENTS / DEADLINES:\n" + "\n".join(e_lines))

    # ── Calendar ──
    today_str = datetime.now().strftime("%Y-%m-%d")
    cal = get_calendar_entry(today_str)
    if cal:
        parts.append(
            f"COLLEGE CALENDAR: Today ({today_str}) is a "
            f"{cal['day_type']} — {cal['description']}"
        )

    return "\n\n".join(parts)
