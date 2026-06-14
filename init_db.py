"""
CampusFlow - Database Initialization Script
Creates and seeds campus.db with realistic engineering college mock data.
Run with: python3.12 init_db.py
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "campus.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables(conn: sqlite3.Connection):
    cursor = conn.cursor()

    cursor.executescript("""
        DROP TABLE IF EXISTS student_profile;
        DROP TABLE IF EXISTS timetables;
        DROP TABLE IF EXISTS mess_menu;
        DROP TABLE IF EXISTS college_events;

        CREATE TABLE student_profile (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT    NOT NULL DEFAULT 'Student',
            department      TEXT    NOT NULL DEFAULT 'CSE',
            semester        INTEGER NOT NULL DEFAULT 1,
            gpa             REAL    NOT NULL DEFAULT 8.0,
            attendance      REAL    NOT NULL DEFAULT 85.0,
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
    """)
    conn.commit()
    print("[DB] Tables created successfully.")


def seed_student_profile(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO student_profile (name, department, semester, gpa, attendance, registered_events)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("Alex Johnson", "CSE", 5, 8.6, 82.0, "TechFest 2025,Hackathon 3.0"))
    conn.commit()
    print("[DB] student_profile seeded.")


def seed_timetables(conn: sqlite3.Connection):
    cursor = conn.cursor()

    # ── CSE Timetable ─────────────────────────────────────────────────────────
    cse_schedule = [
        # Monday
        ("CSE", "Monday",    "09:00 AM - 10:00 AM", "Data Structures & Algorithms",       "CS-101"),
        ("CSE", "Monday",    "10:00 AM - 11:00 AM", "Operating Systems",                  "CS-204"),
        ("CSE", "Monday",    "11:15 AM - 12:15 PM", "Database Management Systems",        "CS-301"),
        ("CSE", "Monday",    "02:00 PM - 03:00 PM", "Computer Networks",                  "CS-305"),
        ("CSE", "Monday",    "03:00 PM - 05:00 PM", "Software Engineering Lab",           "CS-LAB-1"),
        # Tuesday
        ("CSE", "Tuesday",   "09:00 AM - 10:00 AM", "Machine Learning",                   "CS-402"),
        ("CSE", "Tuesday",   "10:00 AM - 11:00 AM", "Compiler Design",                    "CS-303"),
        ("CSE", "Tuesday",   "11:15 AM - 12:15 PM", "Operating Systems",                  "CS-204"),
        ("CSE", "Tuesday",   "02:00 PM - 04:00 PM", "Machine Learning Lab",               "CS-LAB-2"),
        # Wednesday
        ("CSE", "Wednesday", "09:00 AM - 10:00 AM", "Database Management Systems",        "CS-301"),
        ("CSE", "Wednesday", "10:00 AM - 11:00 AM", "Data Structures & Algorithms",       "CS-101"),
        ("CSE", "Wednesday", "11:15 AM - 12:15 PM", "Computer Networks",                  "CS-305"),
        ("CSE", "Wednesday", "02:00 PM - 03:00 PM", "Compiler Design",                    "CS-303"),
        ("CSE", "Wednesday", "03:00 PM - 05:00 PM", "DBMS Lab",                           "CS-LAB-3"),
        # Thursday
        ("CSE", "Thursday",  "09:00 AM - 10:00 AM", "Machine Learning",                   "CS-402"),
        ("CSE", "Thursday",  "10:00 AM - 11:00 AM", "Theory of Computation",              "CS-302"),
        ("CSE", "Thursday",  "11:15 AM - 12:15 PM", "Data Structures & Algorithms",       "CS-101"),
        ("CSE", "Thursday",  "02:00 PM - 03:00 PM", "Operating Systems",                  "CS-204"),
        ("CSE", "Thursday",  "03:00 PM - 05:00 PM", "Networks Lab",                       "CS-LAB-4"),
        # Friday
        ("CSE", "Friday",    "09:00 AM - 10:00 AM", "Theory of Computation",              "CS-302"),
        ("CSE", "Friday",    "10:00 AM - 11:00 AM", "Computer Networks",                  "CS-305"),
        ("CSE", "Friday",    "11:15 AM - 12:15 PM", "Machine Learning",                   "CS-402"),
        ("CSE", "Friday",    "02:00 PM - 03:00 PM", "Compiler Design",                    "CS-303"),
        # Saturday
        ("CSE", "Saturday",  "09:00 AM - 10:00 AM", "Seminar / Guest Lecture",            "Seminar Hall"),
        ("CSE", "Saturday",  "10:00 AM - 12:00 PM", "Project Work",                       "CS-LAB-1"),
    ]

    # ── ECE Timetable ─────────────────────────────────────────────────────────
    ece_schedule = [
        ("ECE", "Monday",    "09:00 AM - 10:00 AM", "Signals & Systems",                  "EC-101"),
        ("ECE", "Monday",    "10:00 AM - 11:00 AM", "VLSI Design",                        "EC-203"),
        ("ECE", "Monday",    "11:15 AM - 12:15 PM", "Analog Circuits",                    "EC-202"),
        ("ECE", "Monday",    "02:00 PM - 04:00 PM", "Electronics Lab",                    "EC-LAB-1"),
        ("ECE", "Tuesday",   "09:00 AM - 10:00 AM", "Digital Communication",              "EC-301"),
        ("ECE", "Tuesday",   "10:00 AM - 11:00 AM", "Signals & Systems",                  "EC-101"),
        ("ECE", "Tuesday",   "11:15 AM - 12:15 PM", "Microprocessors & Microcontrollers", "EC-204"),
        ("ECE", "Tuesday",   "02:00 PM - 04:00 PM", "VLSI Lab",                           "EC-LAB-2"),
        ("ECE", "Wednesday", "09:00 AM - 10:00 AM", "Analog Circuits",                    "EC-202"),
        ("ECE", "Wednesday", "10:00 AM - 11:00 AM", "Digital Communication",              "EC-301"),
        ("ECE", "Wednesday", "11:15 AM - 12:15 PM", "VLSI Design",                        "EC-203"),
        ("ECE", "Wednesday", "02:00 PM - 04:00 PM", "Signals Lab",                        "EC-LAB-3"),
        ("ECE", "Thursday",  "09:00 AM - 10:00 AM", "Microprocessors & Microcontrollers", "EC-204"),
        ("ECE", "Thursday",  "10:00 AM - 11:00 AM", "Analog Circuits",                    "EC-202"),
        ("ECE", "Thursday",  "11:15 AM - 12:15 PM", "Signals & Systems",                  "EC-101"),
        ("ECE", "Thursday",  "02:00 PM - 04:00 PM", "Communication Lab",                  "EC-LAB-4"),
        ("ECE", "Friday",    "09:00 AM - 10:00 AM", "Digital Communication",              "EC-301"),
        ("ECE", "Friday",    "10:00 AM - 11:00 AM", "VLSI Design",                        "EC-203"),
        ("ECE", "Friday",    "11:15 AM - 12:15 PM", "Microprocessors & Microcontrollers", "EC-204"),
        ("ECE", "Friday",    "02:00 PM - 03:00 PM", "Seminar",                            "Seminar Hall"),
        ("ECE", "Saturday",  "09:00 AM - 12:00 PM", "Project Work",                       "EC-LAB-1"),
    ]

    # ── MECH Timetable ────────────────────────────────────────────────────────
    mech_schedule = [
        ("MECH", "Monday",    "09:00 AM - 10:00 AM", "Thermodynamics",                    "ME-101"),
        ("MECH", "Monday",    "10:00 AM - 11:00 AM", "Fluid Mechanics",                   "ME-201"),
        ("MECH", "Monday",    "11:15 AM - 12:15 PM", "Engineering Drawing",               "ME-103"),
        ("MECH", "Monday",    "02:00 PM - 04:00 PM", "CAD/CAM Lab",                       "ME-LAB-1"),
        ("MECH", "Tuesday",   "09:00 AM - 10:00 AM", "Machine Design",                    "ME-301"),
        ("MECH", "Tuesday",   "10:00 AM - 11:00 AM", "Thermodynamics",                    "ME-101"),
        ("MECH", "Tuesday",   "11:15 AM - 12:15 PM", "Manufacturing Processes",           "ME-202"),
        ("MECH", "Tuesday",   "02:00 PM - 04:00 PM", "Fluid Mechanics Lab",               "ME-LAB-2"),
        ("MECH", "Wednesday", "09:00 AM - 10:00 AM", "Fluid Mechanics",                   "ME-201"),
        ("MECH", "Wednesday", "10:00 AM - 11:00 AM", "Machine Design",                    "ME-301"),
        ("MECH", "Wednesday", "11:15 AM - 12:15 PM", "Thermodynamics",                    "ME-101"),
        ("MECH", "Wednesday", "02:00 PM - 04:00 PM", "Manufacturing Lab",                 "ME-LAB-3"),
        ("MECH", "Thursday",  "09:00 AM - 10:00 AM", "Manufacturing Processes",           "ME-202"),
        ("MECH", "Thursday",  "10:00 AM - 11:00 AM", "Engineering Drawing",               "ME-103"),
        ("MECH", "Thursday",  "11:15 AM - 12:15 PM", "Machine Design",                    "ME-301"),
        ("MECH", "Thursday",  "02:00 PM - 04:00 PM", "Thermodynamics Lab",                "ME-LAB-4"),
        ("MECH", "Friday",    "09:00 AM - 10:00 AM", "Fluid Mechanics",                   "ME-201"),
        ("MECH", "Friday",    "10:00 AM - 11:00 AM", "Manufacturing Processes",           "ME-202"),
        ("MECH", "Friday",    "11:15 AM - 12:15 PM", "Engineering Drawing",               "ME-103"),
        ("MECH", "Friday",    "02:00 PM - 03:00 PM", "Technical Seminar",                 "Seminar Hall"),
        ("MECH", "Saturday",  "09:00 AM - 12:00 PM", "Workshop Practice",                 "ME-WORKSHOP"),
    ]

    all_rows = cse_schedule + ece_schedule + mech_schedule
    cursor.executemany(
        "INSERT INTO timetables (department, day, time_slot, subject, room) VALUES (?,?,?,?,?)",
        all_rows
    )
    conn.commit()
    print(f"[DB] timetables seeded with {len(all_rows)} rows.")


def seed_mess_menu(conn: sqlite3.Connection):
    cursor = conn.cursor()

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    menus = {
        "Monday": {
            "Breakfast": ("07:00 AM - 09:00 AM", "Idli (3 pcs) with Sambar & Coconut Chutney, Boiled Egg, Banana, Tea/Coffee, Cornflakes with Milk"),
            "Lunch":     ("12:00 PM - 02:00 PM", "Steamed Rice, Rajma Masala, Aloo Gobi Sabzi, Dal Tadka, Chapati (3), Cucumber Raita, Papad, Pickle"),
            "Snacks":    ("04:30 PM - 05:30 PM", "Samosa (2 pcs), Masala Chai, Roasted Chana"),
            "Dinner":    ("07:30 PM - 09:30 PM", "Chapati (3), Paneer Butter Masala, Steamed Rice, Mixed Veg Dal, Sweet (Gulab Jamun 2 pcs), Salad"),
        },
        "Tuesday": {
            "Breakfast": ("07:00 AM - 09:00 AM", "Poha with Green Peas & Peanuts, Masala Omelette, Bread & Butter, Banana, Tea/Coffee"),
            "Lunch":     ("12:00 PM - 02:00 PM", "Steamed Rice, Chole Masala, Palak Paneer, Yellow Dal, Chapati (3), Onion Raita, Papad"),
            "Snacks":    ("04:30 PM - 05:30 PM", "Bread Pakora (2 pcs), Ginger Chai, Fruit Bowl"),
            "Dinner":    ("07:30 PM - 09:30 PM", "Chapati (3), Egg Curry / Paneer Tikka Masala, Jeera Rice, Moong Dal, Kheer, Salad"),
        },
        "Wednesday": {
            "Breakfast": ("07:00 AM - 09:00 AM", "Dosa (2 pcs) with Sambar & Red Chutney, Boiled Eggs, Sprouts Salad, Tea/Coffee, Juice"),
            "Lunch":     ("12:00 PM - 02:00 PM", "Jeera Rice, Matar Paneer, Aloo Fry, Toor Dal, Chapati (3), Boondi Raita, Sweet (Halwa)"),
            "Snacks":    ("04:30 PM - 05:30 PM", "Pav Bhaji (1 plate), Masala Chai"),
            "Dinner":    ("07:30 PM - 09:30 PM", "Chapati (3), Chicken Curry / Shahi Paneer, Steamed Rice, Dal Makhani, Ice Cream, Salad"),
        },
        "Thursday": {
            "Breakfast": ("07:00 AM - 09:00 AM", "Upma with Cashews, Boiled Egg, White Bread Toast with Jam, Banana, Tea/Coffee"),
            "Lunch":     ("12:00 PM - 02:00 PM", "Steamed Rice, Kadai Paneer, Bhindi Masala, Dal Fry, Chapati (3), Plain Curd, Papad, Pickle"),
            "Snacks":    ("04:30 PM - 05:30 PM", "Vada Pav (2 pcs), Cutting Chai, Boiled Eggs"),
            "Dinner":    ("07:30 PM - 09:30 PM", "Chapati (3), Dum Aloo, Steamed Rice, Rajma Dal, Payasam, Salad"),
        },
        "Friday": {
            "Breakfast": ("07:00 AM - 09:00 AM", "Paratha (2 pcs) with Pickle & Curd, Boiled Eggs, Seasonal Fruit, Tea/Coffee, Cornflakes"),
            "Lunch":     ("12:00 PM - 02:00 PM", "Biryani (Veg/Chicken), Mirchi Ka Salan, Raita, Chapati (2), Sherbet"),
            "Snacks":    ("04:30 PM - 05:30 PM", "Maggi Noodles, Masala Chai, Biscuits"),
            "Dinner":    ("07:30 PM - 09:30 PM", "Chapati (3), Paneer Lababdar / Fish Curry, Steamed Rice, Dal Palak, Rasmalai (2 pcs), Salad"),
        },
        "Saturday": {
            "Breakfast": ("07:30 AM - 09:30 AM", "Chole Bhature (1 plate), Boiled Egg, Mango Juice, Tea/Coffee"),
            "Lunch":     ("12:00 PM - 02:00 PM", "Special Pulao, Paneer Pasanda, Mix Veg Sabzi, Dal Tadka, Chapati (3), Boondi Raita, Gulab Jamun"),
            "Snacks":    ("04:30 PM - 05:30 PM", "Aloo Tikki (2 pcs) with Chutney, Masala Chai"),
            "Dinner":    ("07:30 PM - 09:30 PM", "Chapati (3), Mutton Curry / Paneer Kofta, Jeera Rice, Kadhi, Gajar Halwa, Salad"),
        },
        "Sunday": {
            "Breakfast": ("08:00 AM - 10:00 AM", "Masala Dosa (2 pcs) with Sambar & Chutney, Scrambled Eggs, Bread & Butter, Mango Juice, Tea/Coffee"),
            "Lunch":     ("12:30 PM - 02:30 PM", "Special Sunday Thali: Steamed Rice, Roti (3), Paneer Tikka Masala, Dal Makhani, Jeera Aloo, Raita, Papad, Sweet (Kheer)"),
            "Snacks":    ("04:00 PM - 05:30 PM", "Pizza Slice (2 pcs) / Sandwich, Cold Drinks, Nachos"),
            "Dinner":    ("07:30 PM - 09:30 PM", "Chapati (3), Butter Chicken / Veg Kofta, Steamed Rice, Moong Dal, Shahi Tukda, Salad, Ice Cream"),
        },
    }

    rows = []
    for day in days:
        for meal_type, (time_window, menu_items) in menus[day].items():
            rows.append((day, meal_type, time_window, menu_items))

    cursor.executemany(
        "INSERT INTO mess_menu (day, meal_type, time_window, menu_items) VALUES (?,?,?,?)",
        rows
    )
    conn.commit()
    print(f"[DB] mess_menu seeded with {len(rows)} rows.")


def seed_college_events(conn: sqlite3.Connection):
    cursor = conn.cursor()

    events = [
        # Hackathons
        ("Hackathon 3.0 - Smart Campus",    "Hackathon",       "2025-07-05", "24-hour inter-college hackathon on Smart Campus Solutions. Team size: 2–4. Prizes worth ₹1,50,000.",      "CS Innovation Hub",     "ACM Student Chapter"),
        ("CodeStorm Hackathon",              "Hackathon",       "2025-07-20", "Competitive coding + system design hackathon. Focus: AI & Sustainability. Online + Offline hybrid.",       "Online / CS-LAB-2",     "IEEE CS Society"),
        ("BuildWith AWS Hackathon",          "Hackathon",       "2025-08-10", "Cloud-first hackathon in association with AWS Educate. Build serverless or ML solutions on AWS.",         "Seminar Hall",          "AWS Cloud Club"),

        # Tech Events
        ("TechFest 2025 - Annual Fest",      "Tech Fest",       "2025-07-12", "3-day annual tech festival: paper presentations, robotics, coding contests, gaming, and cultural events.", "Main Auditorium",       "Student Council"),
        ("AI/ML Workshop by Google",         "Workshop",        "2025-06-28", "Two-day hands-on workshop on TensorFlow, Keras, and Google Colab by Google Developer Experts.",           "CS-LAB-3",              "GDSC Campus"),
        ("Open Source Contribution Drive",   "Workshop",        "2025-07-03", "Learn Git, GitHub, open source etiquette, and contribute to real-world projects with mentorship.",         "CS-LAB-1",              "GitHub Campus Experts"),
        ("Startup Pitch Competition",        "Competition",     "2025-07-18", "Present your startup idea to a panel of investors & alumni. Top 3 teams get seed funding support.",       "Seminar Hall",          "E-Cell"),

        # Cultural & Non-Tech
        ("Cultural Night - Rangmanch",       "Cultural",        "2025-07-15", "Annual cultural night with music, dance, drama, and stand-up comedy. Open to all students.",             "Open Air Theatre",      "Cultural Committee"),
        ("Sports Day 2025",                  "Sports",          "2025-07-22", "Inter-department sports tournament: cricket, football, badminton, and athletics.",                        "College Sports Ground",  "Sports Committee"),

        # Academic Deadlines
        ("DSA Assignment Submission",        "Assignment",      "2025-06-25", "Submit Data Structures & Algorithms assignment on AVL Trees and Graph Traversals. Submit on LMS.",        "Online (LMS Portal)",   "Dr. R. Sharma (CSE)"),
        ("DBMS Mini Project Submission",     "Assignment",      "2025-07-01", "Submit DBMS mini project: ER diagrams, normalized schema, and SQL scripts. Max team size: 3.",            "Online (LMS Portal)",   "Prof. M. Patel (CSE)"),
        ("Machine Learning Lab Record",      "Lab Record",      "2025-06-30", "Submit completed ML Lab record book. Must include all experiments from Exp-1 to Exp-8.",                 "CS-LAB-2",              "Dr. Anjali Nair (CSE)"),
        ("Networks Assignment",              "Assignment",      "2025-07-08", "Computer Networks assignment on TCP/IP stack, subnetting, and routing protocols.",                        "Online (LMS Portal)",   "Prof. K. Mehta (CSE)"),

        # Exams
        ("Mid-Semester Examination (CSE)",   "Exam",            "2025-07-14", "Mid-semester exams for CSE 5th Semester. Syllabus: Units 1–3 of all theory subjects.",                  "Exam Halls A, B, C",    "Exam Cell"),
        ("Mid-Semester Examination (ECE)",   "Exam",            "2025-07-14", "Mid-semester exams for ECE 5th Semester. Syllabus: Units 1–3 of all theory subjects.",                  "Exam Halls D, E",       "Exam Cell"),
        ("Mid-Semester Examination (MECH)",  "Exam",            "2025-07-14", "Mid-semester exams for MECH 5th Semester. Syllabus: Units 1–3 of all theory subjects.",                 "Exam Halls F, G",       "Exam Cell"),
        ("End-Semester Examination",         "Exam",            "2025-11-10", "End-semester exams for all departments, all semesters. Detailed schedule on college portal.",            "All Exam Halls",        "Exam Cell"),

        # Seminars / Guest Lectures
        ("Industry Talk: FAANG Careers",     "Guest Lecture",   "2025-06-27", "Panel discussion with engineers from Google, Microsoft & Amazon. Topic: How to crack FAANG interviews.",  "Seminar Hall",          "Training & Placement Cell"),
        ("Research Expo 2025",               "Research Event",  "2025-08-02", "Showcase your research papers. Best paper awards with cash prizes. Open to UG and PG students.",         "Main Auditorium",       "Research & Development Cell"),
    ]

    cursor.executemany(
        """INSERT INTO college_events 
           (event_name, event_type, due_date, description, venue, organizer)
           VALUES (?,?,?,?,?,?)""",
        events
    )
    conn.commit()
    print(f"[DB] college_events seeded with {len(events)} events.")


def main():
    print("=" * 55)
    print("  CampusFlow — Database Initialization")
    print("=" * 55)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"[DB] Removed existing {DB_PATH}")

    conn = get_connection()
    try:
        create_tables(conn)
        seed_student_profile(conn)
        seed_timetables(conn)
        seed_mess_menu(conn)
        seed_college_events(conn)
        print("\n✅  campus.db initialized successfully!")
        print(f"    Location: {DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
