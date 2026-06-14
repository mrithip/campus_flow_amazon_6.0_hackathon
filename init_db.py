"""
CampusFlow — init_db.py
Full database initialization: schema + rich mock data for 3 demo students.
Run: python3.12 init_db.py
"""

import sqlite3
import os
import bcrypt

DB_PATH = os.path.join(os.path.dirname(__file__), "campus.db")


def get_conn():
    return sqlite3.connect(DB_PATH)


def _hash(pw: str) -> str:
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt(12)).decode()


# ─────────────────────────────────────────────────────────────────────────────
# Schema
# ─────────────────────────────────────────────────────────────────────────────

def create_tables(conn):
    conn.executescript("""
        DROP TABLE IF EXISTS leave_applications;
        DROP TABLE IF EXISTS academic_marks;
        DROP TABLE IF EXISTS attendance_records;
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS student_profile;
        DROP TABLE IF EXISTS timetables;
        DROP TABLE IF EXISTS mess_menu;
        DROP TABLE IF EXISTS college_events;
        DROP TABLE IF EXISTS college_calendar;

        CREATE TABLE users (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            username        TEXT    NOT NULL UNIQUE COLLATE NOCASE,
            password_hash   TEXT    NOT NULL,
            name            TEXT    NOT NULL,
            department      TEXT    NOT NULL,
            semester        INTEGER NOT NULL DEFAULT 5
        );

        CREATE TABLE student_profile (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER REFERENCES users(id),
            name            TEXT    NOT NULL DEFAULT 'Student',
            department      TEXT    NOT NULL DEFAULT 'CSE',
            semester        INTEGER NOT NULL DEFAULT 1,
            registered_events TEXT  DEFAULT ''
        );

        CREATE TABLE timetables (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            department  TEXT    NOT NULL,
            day         TEXT    NOT NULL,
            time_slot   TEXT    NOT NULL,
            subject     TEXT    NOT NULL,
            room        TEXT    NOT NULL
        );

        CREATE TABLE mess_menu (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            day         TEXT    NOT NULL,
            meal_type   TEXT    NOT NULL,
            time_window TEXT    NOT NULL,
            menu_items  TEXT    NOT NULL
        );

        CREATE TABLE college_events (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name  TEXT    NOT NULL,
            event_type  TEXT    NOT NULL,
            due_date    TEXT    NOT NULL,
            description TEXT    NOT NULL,
            venue       TEXT    NOT NULL DEFAULT 'TBD',
            organizer   TEXT    NOT NULL DEFAULT 'College'
        );

        CREATE TABLE college_calendar (
            date        TEXT    PRIMARY KEY,
            day_type    TEXT    NOT NULL,
            description TEXT    NOT NULL DEFAULT ''
        );

        CREATE TABLE attendance_records (
            id                      INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id                 INTEGER NOT NULL REFERENCES users(id),
            subject_name            TEXT    NOT NULL,
            total_classes_conducted INTEGER NOT NULL DEFAULT 0,
            classes_attended        INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE academic_marks (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER NOT NULL REFERENCES users(id),
            subject_name    TEXT    NOT NULL,
            exam_type       TEXT    NOT NULL,
            marks_obtained  REAL    NOT NULL,
            total_marks     REAL    NOT NULL DEFAULT 50
        );

        CREATE TABLE leave_applications (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            leave_date  TEXT    NOT NULL,
            reason      TEXT    NOT NULL,
            status      TEXT    NOT NULL DEFAULT 'Pending'
        );
    """)
    conn.commit()
    print("[DB] Schema created.")


# ─────────────────────────────────────────────────────────────────────────────
# Users (3 demo accounts)
# ─────────────────────────────────────────────────────────────────────────────

def seed_users(conn) -> dict:
    """Returns {username: id} mapping for FK references."""
    users = [
        ("alex",   _hash("alex123"),   "Alex Johnson",   "CSE",  5),
        ("priya",  _hash("priya123"),  "Priya Sharma",   "ECE",  5),
        ("rahul",  _hash("rahul123"),  "Rahul Mehta",    "MECH", 5),
    ]
    cur = conn.cursor()
    id_map = {}
    for username, pw_hash, name, dept, sem in users:
        cur.execute(
            "INSERT INTO users (username,password_hash,name,department,semester) VALUES (?,?,?,?,?)",
            (username, pw_hash, name, dept, sem)
        )
        id_map[username] = cur.lastrowid
    conn.commit()
    print(f"[DB] users seeded: {list(id_map.keys())} (passwords: <name>123)")
    return id_map


# ─────────────────────────────────────────────────────────────────────────────
# Timetables
# ─────────────────────────────────────────────────────────────────────────────

def seed_timetables(conn):
    cse = [
        ("CSE","Monday",   "09:00 AM - 10:00 AM","Data Structures & Algorithms","CS-101"),
        ("CSE","Monday",   "10:00 AM - 11:00 AM","Operating Systems","CS-204"),
        ("CSE","Monday",   "11:15 AM - 12:15 PM","Database Management Systems","CS-301"),
        ("CSE","Monday",   "02:00 PM - 03:00 PM","Computer Networks","CS-305"),
        ("CSE","Monday",   "03:00 PM - 05:00 PM","Software Engineering Lab","CS-LAB-1"),
        ("CSE","Tuesday",  "09:00 AM - 10:00 AM","Machine Learning","CS-402"),
        ("CSE","Tuesday",  "10:00 AM - 11:00 AM","Compiler Design","CS-303"),
        ("CSE","Tuesday",  "11:15 AM - 12:15 PM","Operating Systems","CS-204"),
        ("CSE","Tuesday",  "02:00 PM - 04:00 PM","Machine Learning Lab","CS-LAB-2"),
        ("CSE","Wednesday","09:00 AM - 10:00 AM","Database Management Systems","CS-301"),
        ("CSE","Wednesday","10:00 AM - 11:00 AM","Data Structures & Algorithms","CS-101"),
        ("CSE","Wednesday","11:15 AM - 12:15 PM","Computer Networks","CS-305"),
        ("CSE","Wednesday","02:00 PM - 03:00 PM","Compiler Design","CS-303"),
        ("CSE","Wednesday","03:00 PM - 05:00 PM","DBMS Lab","CS-LAB-3"),
        ("CSE","Thursday", "09:00 AM - 10:00 AM","Machine Learning","CS-402"),
        ("CSE","Thursday", "10:00 AM - 11:00 AM","Theory of Computation","CS-302"),
        ("CSE","Thursday", "11:15 AM - 12:15 PM","Data Structures & Algorithms","CS-101"),
        ("CSE","Thursday", "02:00 PM - 03:00 PM","Operating Systems","CS-204"),
        ("CSE","Thursday", "03:00 PM - 05:00 PM","Networks Lab","CS-LAB-4"),
        ("CSE","Friday",   "09:00 AM - 10:00 AM","Theory of Computation","CS-302"),
        ("CSE","Friday",   "10:00 AM - 11:00 AM","Computer Networks","CS-305"),
        ("CSE","Friday",   "11:15 AM - 12:15 PM","Machine Learning","CS-402"),
        ("CSE","Friday",   "02:00 PM - 03:00 PM","Compiler Design","CS-303"),
        ("CSE","Saturday", "09:00 AM - 10:00 AM","Seminar / Guest Lecture","Seminar Hall"),
        ("CSE","Saturday", "10:00 AM - 12:00 PM","Project Work","CS-LAB-1"),
    ]
    ece = [
        ("ECE","Monday",   "09:00 AM - 10:00 AM","Signals & Systems","EC-101"),
        ("ECE","Monday",   "10:00 AM - 11:00 AM","VLSI Design","EC-203"),
        ("ECE","Monday",   "11:15 AM - 12:15 PM","Analog Circuits","EC-202"),
        ("ECE","Monday",   "02:00 PM - 04:00 PM","Electronics Lab","EC-LAB-1"),
        ("ECE","Tuesday",  "09:00 AM - 10:00 AM","Digital Communication","EC-301"),
        ("ECE","Tuesday",  "10:00 AM - 11:00 AM","Signals & Systems","EC-101"),
        ("ECE","Tuesday",  "11:15 AM - 12:15 PM","Microprocessors & Microcontrollers","EC-204"),
        ("ECE","Tuesday",  "02:00 PM - 04:00 PM","VLSI Lab","EC-LAB-2"),
        ("ECE","Wednesday","09:00 AM - 10:00 AM","Analog Circuits","EC-202"),
        ("ECE","Wednesday","10:00 AM - 11:00 AM","Digital Communication","EC-301"),
        ("ECE","Wednesday","11:15 AM - 12:15 PM","VLSI Design","EC-203"),
        ("ECE","Wednesday","02:00 PM - 04:00 PM","Signals Lab","EC-LAB-3"),
        ("ECE","Thursday", "09:00 AM - 10:00 AM","Microprocessors & Microcontrollers","EC-204"),
        ("ECE","Thursday", "10:00 AM - 11:00 AM","Analog Circuits","EC-202"),
        ("ECE","Thursday", "11:15 AM - 12:15 PM","Signals & Systems","EC-101"),
        ("ECE","Thursday", "02:00 PM - 04:00 PM","Communication Lab","EC-LAB-4"),
        ("ECE","Friday",   "09:00 AM - 10:00 AM","Digital Communication","EC-301"),
        ("ECE","Friday",   "10:00 AM - 11:00 AM","VLSI Design","EC-203"),
        ("ECE","Friday",   "11:15 AM - 12:15 PM","Microprocessors & Microcontrollers","EC-204"),
        ("ECE","Friday",   "02:00 PM - 03:00 PM","Seminar","Seminar Hall"),
        ("ECE","Saturday", "09:00 AM - 12:00 PM","Project Work","EC-LAB-1"),
    ]
    mech = [
        ("MECH","Monday",   "09:00 AM - 10:00 AM","Thermodynamics","ME-101"),
        ("MECH","Monday",   "10:00 AM - 11:00 AM","Fluid Mechanics","ME-201"),
        ("MECH","Monday",   "11:15 AM - 12:15 PM","Engineering Drawing","ME-103"),
        ("MECH","Monday",   "02:00 PM - 04:00 PM","CAD/CAM Lab","ME-LAB-1"),
        ("MECH","Tuesday",  "09:00 AM - 10:00 AM","Machine Design","ME-301"),
        ("MECH","Tuesday",  "10:00 AM - 11:00 AM","Thermodynamics","ME-101"),
        ("MECH","Tuesday",  "11:15 AM - 12:15 PM","Manufacturing Processes","ME-202"),
        ("MECH","Tuesday",  "02:00 PM - 04:00 PM","Fluid Mechanics Lab","ME-LAB-2"),
        ("MECH","Wednesday","09:00 AM - 10:00 AM","Fluid Mechanics","ME-201"),
        ("MECH","Wednesday","10:00 AM - 11:00 AM","Machine Design","ME-301"),
        ("MECH","Wednesday","11:15 AM - 12:15 PM","Thermodynamics","ME-101"),
        ("MECH","Wednesday","02:00 PM - 04:00 PM","Manufacturing Lab","ME-LAB-3"),
        ("MECH","Thursday", "09:00 AM - 10:00 AM","Manufacturing Processes","ME-202"),
        ("MECH","Thursday", "10:00 AM - 11:00 AM","Engineering Drawing","ME-103"),
        ("MECH","Thursday", "11:15 AM - 12:15 PM","Machine Design","ME-301"),
        ("MECH","Thursday", "02:00 PM - 04:00 PM","Thermodynamics Lab","ME-LAB-4"),
        ("MECH","Friday",   "09:00 AM - 10:00 AM","Fluid Mechanics","ME-201"),
        ("MECH","Friday",   "10:00 AM - 11:00 AM","Manufacturing Processes","ME-202"),
        ("MECH","Friday",   "11:15 AM - 12:15 PM","Engineering Drawing","ME-103"),
        ("MECH","Friday",   "02:00 PM - 03:00 PM","Technical Seminar","Seminar Hall"),
        ("MECH","Saturday", "09:00 AM - 12:00 PM","Workshop Practice","ME-WORKSHOP"),
    ]
    rows = cse + ece + mech
    conn.executemany(
        "INSERT INTO timetables (department,day,time_slot,subject,room) VALUES (?,?,?,?,?)", rows
    )
    conn.commit()
    print(f"[DB] timetables: {len(rows)} rows")


# ─────────────────────────────────────────────────────────────────────────────
# Mess menu
# ─────────────────────────────────────────────────────────────────────────────

def seed_mess_menu(conn):
    menus = {
        "Monday":    [("Breakfast","07:00 AM - 09:00 AM","Idli (3 pcs) with Sambar & Coconut Chutney, Boiled Egg, Banana, Tea/Coffee, Cornflakes with Milk"),
                      ("Lunch",    "12:00 PM - 02:00 PM","Steamed Rice, Rajma Masala, Aloo Gobi Sabzi, Dal Tadka, Chapati (3), Cucumber Raita, Papad, Pickle"),
                      ("Snacks",   "04:30 PM - 05:30 PM","Samosa (2 pcs), Masala Chai, Roasted Chana"),
                      ("Dinner",   "07:30 PM - 09:30 PM","Chapati (3), Paneer Butter Masala, Steamed Rice, Mixed Veg Dal, Sweet (Gulab Jamun 2 pcs), Salad")],
        "Tuesday":   [("Breakfast","07:00 AM - 09:00 AM","Poha with Green Peas & Peanuts, Masala Omelette, Bread & Butter, Banana, Tea/Coffee"),
                      ("Lunch",    "12:00 PM - 02:00 PM","Steamed Rice, Chole Masala, Palak Paneer, Yellow Dal, Chapati (3), Onion Raita, Papad"),
                      ("Snacks",   "04:30 PM - 05:30 PM","Bread Pakora (2 pcs), Ginger Chai, Fruit Bowl"),
                      ("Dinner",   "07:30 PM - 09:30 PM","Chapati (3), Egg Curry / Paneer Tikka Masala, Jeera Rice, Moong Dal, Kheer, Salad")],
        "Wednesday": [("Breakfast","07:00 AM - 09:00 AM","Dosa (2 pcs) with Sambar & Red Chutney, Boiled Eggs, Sprouts Salad, Tea/Coffee, Juice"),
                      ("Lunch",    "12:00 PM - 02:00 PM","Jeera Rice, Matar Paneer, Aloo Fry, Toor Dal, Chapati (3), Boondi Raita, Sweet (Halwa)"),
                      ("Snacks",   "04:30 PM - 05:30 PM","Pav Bhaji (1 plate), Masala Chai"),
                      ("Dinner",   "07:30 PM - 09:30 PM","Chapati (3), Chicken Curry / Shahi Paneer, Steamed Rice, Dal Makhani, Ice Cream, Salad")],
        "Thursday":  [("Breakfast","07:00 AM - 09:00 AM","Upma with Cashews, Boiled Egg, White Bread Toast with Jam, Banana, Tea/Coffee"),
                      ("Lunch",    "12:00 PM - 02:00 PM","Steamed Rice, Kadai Paneer, Bhindi Masala, Dal Fry, Chapati (3), Plain Curd, Papad, Pickle"),
                      ("Snacks",   "04:30 PM - 05:30 PM","Vada Pav (2 pcs), Cutting Chai, Boiled Eggs"),
                      ("Dinner",   "07:30 PM - 09:30 PM","Chapati (3), Dum Aloo, Steamed Rice, Rajma Dal, Payasam, Salad")],
        "Friday":    [("Breakfast","07:00 AM - 09:00 AM","Paratha (2 pcs) with Pickle & Curd, Boiled Eggs, Seasonal Fruit, Tea/Coffee, Cornflakes"),
                      ("Lunch",    "12:00 PM - 02:00 PM","Biryani (Veg/Chicken), Mirchi Ka Salan, Raita, Chapati (2), Sherbet"),
                      ("Snacks",   "04:30 PM - 05:30 PM","Maggi Noodles, Masala Chai, Biscuits"),
                      ("Dinner",   "07:30 PM - 09:30 PM","Chapati (3), Paneer Lababdar / Fish Curry, Steamed Rice, Dal Palak, Rasmalai (2 pcs), Salad")],
        "Saturday":  [("Breakfast","07:30 AM - 09:30 AM","Chole Bhature (1 plate), Boiled Egg, Mango Juice, Tea/Coffee"),
                      ("Lunch",    "12:00 PM - 02:00 PM","Special Pulao, Paneer Pasanda, Mix Veg Sabzi, Dal Tadka, Chapati (3), Boondi Raita, Gulab Jamun"),
                      ("Snacks",   "04:30 PM - 05:30 PM","Aloo Tikki (2 pcs) with Chutney, Masala Chai"),
                      ("Dinner",   "07:30 PM - 09:30 PM","Chapati (3), Mutton Curry / Paneer Kofta, Jeera Rice, Kadhi, Gajar Halwa, Salad")],
        "Sunday":    [("Breakfast","08:00 AM - 10:00 AM","Masala Dosa (2 pcs) with Sambar & Chutney, Scrambled Eggs, Bread & Butter, Mango Juice, Tea/Coffee"),
                      ("Lunch",    "12:30 PM - 02:30 PM","Special Sunday Thali: Steamed Rice, Roti (3), Paneer Tikka Masala, Dal Makhani, Jeera Aloo, Raita, Papad, Sweet (Kheer)"),
                      ("Snacks",   "04:00 PM - 05:30 PM","Pizza Slice (2 pcs) / Sandwich, Cold Drinks, Nachos"),
                      ("Dinner",   "07:30 PM - 09:30 PM","Chapati (3), Butter Chicken / Veg Kofta, Steamed Rice, Moong Dal, Shahi Tukda, Salad, Ice Cream")],
    }
    rows = [(day, mt, tw, mi) for day, items in menus.items() for mt, tw, mi in items]
    conn.executemany(
        "INSERT INTO mess_menu (day,meal_type,time_window,menu_items) VALUES (?,?,?,?)", rows
    )
    conn.commit()
    print(f"[DB] mess_menu: {len(rows)} rows")


# ─────────────────────────────────────────────────────────────────────────────
# College events
# ─────────────────────────────────────────────────────────────────────────────

def seed_college_events(conn):
    events = [
        ("Hackathon 3.0 - Smart Campus","Hackathon","2025-07-05","24-hour inter-college hackathon on Smart Campus Solutions. Team: 2-4. Prizes worth Rs.1,50,000.","CS Innovation Hub","ACM Student Chapter"),
        ("CodeStorm Hackathon","Hackathon","2025-07-20","Competitive coding + system design hackathon. Focus: AI & Sustainability. Online + Offline hybrid.","Online / CS-LAB-2","IEEE CS Society"),
        ("BuildWith AWS Hackathon","Hackathon","2025-08-10","Cloud-first hackathon in association with AWS Educate. Build serverless or ML solutions on AWS.","Seminar Hall","AWS Cloud Club"),
        ("TechFest 2025 - Annual Fest","Tech Fest","2025-07-12","3-day annual tech festival: paper presentations, robotics, coding contests, gaming, and cultural events.","Main Auditorium","Student Council"),
        ("AI/ML Workshop by Google","Workshop","2025-06-28","Two-day hands-on workshop on TensorFlow, Keras, and Google Colab by Google Developer Experts.","CS-LAB-3","GDSC Campus"),
        ("Open Source Contribution Drive","Workshop","2025-07-03","Learn Git, GitHub, open source etiquette, and contribute to real-world projects with mentorship.","CS-LAB-1","GitHub Campus Experts"),
        ("Startup Pitch Competition","Competition","2025-07-18","Present your startup idea to a panel of investors & alumni. Top 3 teams get seed funding support.","Seminar Hall","E-Cell"),
        ("Cultural Night - Rangmanch","Cultural","2025-07-15","Annual cultural night with music, dance, drama, and stand-up comedy. Open to all students.","Open Air Theatre","Cultural Committee"),
        ("Sports Day 2025","Sports","2025-07-22","Inter-department sports tournament: cricket, football, badminton, and athletics.","College Sports Ground","Sports Committee"),
        ("DSA Assignment Submission","Assignment","2025-06-25","Submit Data Structures & Algorithms assignment on AVL Trees and Graph Traversals. Submit on LMS.","Online (LMS Portal)","Dr. R. Sharma (CSE)"),
        ("DBMS Mini Project Submission","Assignment","2025-07-01","Submit DBMS mini project: ER diagrams, normalized schema, and SQL scripts. Max team size: 3.","Online (LMS Portal)","Prof. M. Patel (CSE)"),
        ("Machine Learning Lab Record","Lab Record","2025-06-30","Submit completed ML Lab record book. Must include all experiments from Exp-1 to Exp-8.","CS-LAB-2","Dr. Anjali Nair (CSE)"),
        ("Networks Assignment","Assignment","2025-07-08","Computer Networks assignment on TCP/IP stack, subnetting, and routing protocols.","Online (LMS Portal)","Prof. K. Mehta (CSE)"),
        ("Mid-Semester Examination (CSE)","Exam","2025-07-14","Mid-semester exams for CSE 5th Semester. Syllabus: Units 1-3 of all theory subjects.","Exam Halls A, B, C","Exam Cell"),
        ("Mid-Semester Examination (ECE)","Exam","2025-07-14","Mid-semester exams for ECE 5th Semester. Syllabus: Units 1-3 of all theory subjects.","Exam Halls D, E","Exam Cell"),
        ("Mid-Semester Examination (MECH)","Exam","2025-07-14","Mid-semester exams for MECH 5th Semester. Syllabus: Units 1-3 of all theory subjects.","Exam Halls F, G","Exam Cell"),
        ("End-Semester Examination","Exam","2025-11-10","End-semester exams for all departments, all semesters. Detailed schedule on college portal.","All Exam Halls","Exam Cell"),
        ("Industry Talk: FAANG Careers","Guest Lecture","2025-06-27","Panel discussion with engineers from Google, Microsoft & Amazon. Topic: How to crack FAANG interviews.","Seminar Hall","Training & Placement Cell"),
        ("Research Expo 2025","Research Event","2025-08-02","Showcase your research papers. Best paper awards with cash prizes. Open to UG and PG students.","Main Auditorium","Research & Development Cell"),
    ]
    conn.executemany(
        "INSERT INTO college_events (event_name,event_type,due_date,description,venue,organizer) VALUES (?,?,?,?,?,?)",
        events
    )
    conn.commit()
    print(f"[DB] college_events: {len(events)} rows")


# ─────────────────────────────────────────────────────────────────────────────
# College calendar  (June–July 2025 + surrounding)
# ─────────────────────────────────────────────────────────────────────────────

def seed_college_calendar(conn):
    from datetime import date, timedelta
    holidays = {
        "2025-06-21": "Official Holiday — Founders Day",
        "2025-06-27": "Official Holiday — Guest Lecture Day (No regular classes)",
        "2025-07-04": "Official Holiday — Independence Day Preparation",
        "2025-07-14": "Official Holiday — Mid-Semester Examination begins",
        "2025-07-15": "Official Holiday — Mid-Semester Examination (Day 2)",
        "2025-07-16": "Official Holiday — Mid-Semester Examination (Day 3)",
        "2025-08-15": "Official Holiday — Independence Day",
        "2025-10-02": "Official Holiday — Gandhi Jayanti",
        "2025-10-20": "Official Holiday — Diwali",
        "2025-10-21": "Official Holiday — Diwali Holiday",
        "2025-11-10": "Official Holiday — End-Semester Examination begins",
    }
    rows = []
    start = date(2025, 6, 1)
    end   = date(2025, 11, 30)
    cur   = start
    while cur <= end:
        ds = cur.strftime("%Y-%m-%d")
        if ds in holidays:
            rows.append((ds, "Official Holiday", holidays[ds]))
        elif cur.weekday() == 6:  # Sunday
            rows.append((ds, "Weekend", "Sunday — No classes"))
        else:
            rows.append((ds, "Working Day", "Regular academic day"))
        cur += timedelta(days=1)
    conn.executemany(
        "INSERT INTO college_calendar (date,day_type,description) VALUES (?,?,?)", rows
    )
    conn.commit()
    print(f"[DB] college_calendar: {len(rows)} rows")


# ─────────────────────────────────────────────────────────────────────────────
# Attendance records (per user — varied, realistic)
# ─────────────────────────────────────────────────────────────────────────────

def seed_attendance(conn, id_map):
    # alex (CSE) — two subjects below 75%
    alex_att = [
        (id_map["alex"], "Data Structures & Algorithms", 40, 38),
        (id_map["alex"], "Operating Systems",            38, 26),  # 68% — low
        (id_map["alex"], "Database Management Systems",  42, 40),
        (id_map["alex"], "Computer Networks",            36, 25),  # 69% — low
        (id_map["alex"], "Machine Learning",             40, 35),
        (id_map["alex"], "Compiler Design",              38, 30),
    ]
    # priya (ECE) — healthy overall
    priya_att = [
        (id_map["priya"], "Signals & Systems",                  44, 42),
        (id_map["priya"], "VLSI Design",                        40, 38),
        (id_map["priya"], "Analog Circuits",                    42, 40),
        (id_map["priya"], "Digital Communication",              38, 36),
        (id_map["priya"], "Microprocessors & Microcontrollers", 44, 40),
    ]
    # rahul (MECH) — one subject borderline low
    rahul_att = [
        (id_map["rahul"], "Thermodynamics",        40, 28),  # 70% — low
        (id_map["rahul"], "Fluid Mechanics",        38, 36),
        (id_map["rahul"], "Engineering Drawing",   42, 39),
        (id_map["rahul"], "Machine Design",         40, 37),
        (id_map["rahul"], "Manufacturing Processes",38, 35),
    ]
    rows = alex_att + priya_att + rahul_att
    conn.executemany(
        "INSERT INTO attendance_records "
        "(user_id,subject_name,total_classes_conducted,classes_attended) VALUES (?,?,?,?)",
        rows
    )
    conn.commit()
    print(f"[DB] attendance_records: {len(rows)} rows")


# ─────────────────────────────────────────────────────────────────────────────
# Academic marks (Internal-1, Internal-2, some End-Semester)
# ─────────────────────────────────────────────────────────────────────────────

def seed_marks(conn, id_map):
    # alex (CSE) — average performer
    alex_marks = [
        (id_map["alex"], "Data Structures & Algorithms", "Internal-1", 38, 50),
        (id_map["alex"], "Data Structures & Algorithms", "Internal-2", 34, 50),
        (id_map["alex"], "Operating Systems",            "Internal-1", 30, 50),
        (id_map["alex"], "Operating Systems",            "Internal-2", 28, 50),
        (id_map["alex"], "Database Management Systems",  "Internal-1", 42, 50),
        (id_map["alex"], "Database Management Systems",  "Internal-2", 40, 50),
        (id_map["alex"], "Computer Networks",            "Internal-1", 32, 50),
        (id_map["alex"], "Computer Networks",            "Internal-2", 29, 50),
        (id_map["alex"], "Machine Learning",             "Internal-1", 44, 50),
        (id_map["alex"], "Machine Learning",             "Internal-2", 41, 50),
        (id_map["alex"], "Compiler Design",              "Internal-1", 35, 50),
        (id_map["alex"], "Compiler Design",              "Internal-2", 33, 50),
    ]
    # priya (ECE) — high performer
    priya_marks = [
        (id_map["priya"], "Signals & Systems",                  "Internal-1", 46, 50),
        (id_map["priya"], "Signals & Systems",                  "Internal-2", 44, 50),
        (id_map["priya"], "VLSI Design",                        "Internal-1", 43, 50),
        (id_map["priya"], "VLSI Design",                        "Internal-2", 45, 50),
        (id_map["priya"], "Analog Circuits",                    "Internal-1", 47, 50),
        (id_map["priya"], "Analog Circuits",                    "Internal-2", 46, 50),
        (id_map["priya"], "Digital Communication",              "Internal-1", 42, 50),
        (id_map["priya"], "Digital Communication",              "Internal-2", 40, 50),
        (id_map["priya"], "Microprocessors & Microcontrollers", "Internal-1", 44, 50),
        (id_map["priya"], "Microprocessors & Microcontrollers", "Internal-2", 43, 50),
    ]
    # rahul (MECH) — mixed performer
    rahul_marks = [
        (id_map["rahul"], "Thermodynamics",          "Internal-1", 28, 50),
        (id_map["rahul"], "Thermodynamics",          "Internal-2", 26, 50),
        (id_map["rahul"], "Fluid Mechanics",         "Internal-1", 38, 50),
        (id_map["rahul"], "Fluid Mechanics",         "Internal-2", 36, 50),
        (id_map["rahul"], "Engineering Drawing",     "Internal-1", 44, 50),
        (id_map["rahul"], "Engineering Drawing",     "Internal-2", 43, 50),
        (id_map["rahul"], "Machine Design",          "Internal-1", 35, 50),
        (id_map["rahul"], "Machine Design",          "Internal-2", 33, 50),
        (id_map["rahul"], "Manufacturing Processes", "Internal-1", 40, 50),
        (id_map["rahul"], "Manufacturing Processes", "Internal-2", 38, 50),
    ]
    rows = alex_marks + priya_marks + rahul_marks
    conn.executemany(
        "INSERT INTO academic_marks "
        "(user_id,subject_name,exam_type,marks_obtained,total_marks) VALUES (?,?,?,?,?)",
        rows
    )
    conn.commit()
    print(f"[DB] academic_marks: {len(rows)} rows")


# ─────────────────────────────────────────────────────────────────────────────
# Leave applications
# ─────────────────────────────────────────────────────────────────────────────

def seed_leaves(conn, id_map):
    rows = [
        (id_map["alex"],  "2025-06-10", "Fever and cold — medical leave", "Approved"),
        (id_map["alex"],  "2025-06-18", "Family function out of city",     "Approved"),
        (id_map["alex"],  "2025-06-25", "Doctor appointment — follow-up",  "Pending"),
        (id_map["priya"], "2025-06-12", "Sister's wedding ceremony",        "Approved"),
        (id_map["priya"], "2025-06-20", "Participating in State-level quiz","Approved"),
        (id_map["rahul"], "2025-06-08", "Sports tournament — inter-college","Approved"),
        (id_map["rahul"], "2025-06-22", "Severe migraine — medical leave",  "Pending"),
    ]
    conn.executemany(
        "INSERT INTO leave_applications (user_id,leave_date,reason,status) VALUES (?,?,?,?)",
        rows
    )
    conn.commit()
    print(f"[DB] leave_applications: {len(rows)} rows")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 58)
    print("  CampusFlow v2 — Full Database Initialization")
    print("=" * 58)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"[DB] Removed existing {DB_PATH}")

    conn = get_conn()
    try:
        create_tables(conn)
        id_map = seed_users(conn)
        seed_timetables(conn)
        seed_mess_menu(conn)
        seed_college_events(conn)
        seed_college_calendar(conn)
        seed_attendance(conn, id_map)
        seed_marks(conn, id_map)
        seed_leaves(conn, id_map)
        print("\n  campus.db v2 initialized successfully.")
        print(f"  Location : {DB_PATH}")
        print("\n  Demo accounts:")
        print("    Username: alex   | Password: alex123   | Dept: CSE")
        print("    Username: priya  | Password: priya123  | Dept: ECE")
        print("    Username: rahul  | Password: rahul123  | Dept: MECH")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
