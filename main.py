import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import date


# ================= DATABASE =================

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date TEXT,
    status TEXT
)
""")

conn.commit()


# ================= MAIN WINDOW =================

root = tk.Tk()
root.title("Student Attendance System")
root.geometry("600x650")
root.configure(bg="#eaf2ff")


# ================= FRAMES =================

login_frame = tk.Frame(root, bg="#eaf2ff")
dashboard_frame = tk.Frame(root, bg="#eaf2ff")
student_frame = tk.Frame(root, bg="#eaf2ff")
attendance_frame = tk.Frame(root, bg="#eaf2ff")
report_frame = tk.Frame(root, bg="#eaf2ff")
student_list_frame = tk.Frame(root, bg="#eaf2ff")


# ================= LOGIN =================

def login():

    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "1234":

        login_frame.pack_forget()
        show_dashboard()

    else:

        messagebox.showerror(
            "Login Error",
            "Invalid Username or Password"
        )


def logout():

    dashboard_frame.pack_forget()
    student_frame.pack_forget()
    attendance_frame.pack_forget()
    report_frame.pack_forget()
    student_list_frame.pack_forget()

    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    login_frame.pack(pady=30)


# ================= DASHBOARD =================

def show_dashboard():

    student_frame.pack_forget()

    for widget in dashboard_frame.winfo_children():
        widget.destroy()

    dashboard_frame.pack(pady=20)

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM attendance
        WHERE status='Present'
    """)
    present = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM attendance
        WHERE status='Absent'
    """)
    absent = cursor.fetchone()[0]

    tk.Label(
        dashboard_frame,
        text="Student Attendance System",
        font=("Arial", 24, "bold"),
        bg="#eaf2ff",
        fg="#174a8b"
    ).pack(pady=15)

    tk.Label(
        dashboard_frame,
        text="Dashboard",
        font=("Arial", 20, "bold"),
        bg="#eaf2ff"
    ).pack(pady=10)

    tk.Label(
        dashboard_frame,
        text=f"Total Students : {total_students}",
        font=("Arial", 14),
        bg="#eaf2ff"
    ).pack(pady=8)

    tk.Label(
        dashboard_frame,
        text=f"Present : {present}",
        font=("Arial", 14),
        bg="#eaf2ff"
    ).pack(pady=8)

    tk.Label(
        dashboard_frame,
        text=f"Absent : {absent}",
        font=("Arial", 14),
        bg="#eaf2ff"
    ).pack(pady=8)

    tk.Button(
        dashboard_frame,
        text="Add Student",
        width=25,
        command=show_student_page
    ).pack(pady=8)

    tk.Button(
        dashboard_frame,
        text="Student List",
        width=25,
        command=show_students
    ).pack(pady=8)

    tk.Button(
        dashboard_frame,
        text="Mark Attendance",
        width=25,
        command=show_attendance
    ).pack(pady=8)

    tk.Button(
        dashboard_frame,
        text="Attendance Report",
        width=25,
        command=show_report
    ).pack(pady=8)

    tk.Button(
        dashboard_frame,
        text="Logout",
        width=25,
        command=logout
    ).pack(pady=15)


# ================= ADD STUDENT =================

def show_student_page():

    dashboard_frame.pack_forget()
    attendance_frame.pack_forget()
    report_frame.pack_forget()
    student_list_frame.pack_forget()

    student_frame.pack(pady=20)


def add_student():

    name = name_entry.get()
    roll = roll_entry.get()

    if name == "" or roll == "":
        messagebox.showwarning(
            "Warning",
            "Please enter Student Name and Roll Number"
        )
        return

    cursor.execute(
        "INSERT INTO students (name, roll_no) VALUES (?, ?)",
        (name, roll)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Student Added Successfully!"
    )

    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)


# ================= STUDENT LIST =================

def show_students():

    dashboard_frame.pack_forget()
    student_frame.pack_forget()
    attendance_frame.pack_forget()
    report_frame.pack_forget()

    for widget in student_list_frame.winfo_children():
        widget.destroy()

    student_list_frame.pack(pady=20)

    tk.Label(
        student_list_frame,
        text="Student List",
        font=("Arial", 22, "bold"),
        bg="#eaf2ff",
        fg="#174a8b"
    ).pack(pady=15)

    cursor.execute(
        "SELECT name, roll_no FROM students"
    )

    students = cursor.fetchall()

    if not students:

        tk.Label(
            student_list_frame,
            text="No students found.",
            bg="#eaf2ff"
        ).pack(pady=10)

    else:

        for name, roll in students:

            tk.Label(
                student_list_frame,
                text=f"{roll} - {name}",
                font=("Arial", 13),
                bg="#eaf2ff"
            ).pack(pady=5)

    tk.Button(
        student_list_frame,
        text="Back to Dashboard",
        width=20,
        command=lambda: [
            student_list_frame.pack_forget(),
            show_dashboard()
        ]
    ).pack(pady=20)


# ================= MARK ATTENDANCE =================

attendance_vars = {}


def show_attendance():

    dashboard_frame.pack_forget()
    student_frame.pack_forget()
    report_frame.pack_forget()
    student_list_frame.pack_forget()

    for widget in attendance_frame.winfo_children():
        widget.destroy()

    attendance_frame.pack(pady=20)

    tk.Label(
        attendance_frame,
        text="Mark Attendance",
        font=("Arial", 22, "bold"),
        bg="#eaf2ff",
        fg="#174a8b"
    ).pack(pady=15)

    cursor.execute(
        "SELECT id, name, roll_no FROM students"
    )

    students = cursor.fetchall()

    if not students:

        tk.Label(
            attendance_frame,
            text="No students added yet.",
            bg="#eaf2ff"
        ).pack(pady=20)

        return

    attendance_vars.clear()

    for student_id, name, roll_no in students:

        tk.Label(
            attendance_frame,
            text=f"{roll_no} - {name}",
            font=("Arial", 12, "bold"),
            bg="#eaf2ff"
        ).pack(pady=3)

        status = tk.StringVar(value="Present")

        attendance_vars[student_id] = status

        tk.Radiobutton(
            attendance_frame,
            text="Present",
            variable=status,
            value="Present",
            bg="#eaf2ff"
        ).pack()

        tk.Radiobutton(
            attendance_frame,
            text="Absent",
            variable=status,
            value="Absent",
            bg="#eaf2ff"
        ).pack()

    tk.Button(
        attendance_frame,
        text="Save Attendance",
        width=20,
        command=save_attendance
    ).pack(pady=15)

    tk.Button(
        attendance_frame,
        text="View Report",
        width=20,
        command=show_report
    ).pack(pady=5)

    tk.Button(
        attendance_frame,
        text="Back to Dashboard",
        width=20,
        command=lambda: [
            attendance_frame.pack_forget(),
            show_dashboard()
        ]
    ).pack(pady=5)


# ================= SAVE ATTENDANCE =================

def save_attendance():

    today = str(date.today())

    for student_id, status in attendance_vars.items():

        cursor.execute(
            """
            INSERT INTO attendance
            (student_id, date, status)
            VALUES (?, ?, ?)
            """,
            (
                student_id,
                today,
                status.get()
            )
        )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Attendance Saved Successfully!"
    )


# ================= REPORT =================

def show_report():

    dashboard_frame.pack_forget()
    attendance_frame.pack_forget()
    student_frame.pack_forget()
    student_list_frame.pack_forget()

    for widget in report_frame.winfo_children():
        widget.destroy()

    report_frame.pack(pady=20)

    tk.Label(
        report_frame,
        text="Attendance Report",
        font=("Arial", 22, "bold"),
        bg="#eaf2ff",
        fg="#174a8b"
    ).pack(pady=15)

    cursor.execute("""
    SELECT students.name,
           students.roll_no,
           attendance.date,
           attendance.status
    FROM students
    LEFT JOIN attendance
    ON students.id = attendance.student_id
    ORDER BY attendance.id DESC
    """)

    records = cursor.fetchall()

    if not records:

        tk.Label(
            report_frame,
            text="No attendance records found.",
            bg="#eaf2ff"
        ).pack(pady=20)

    else:

        for name, roll_no, att_date, status in records:

            if status is None:
                status = "Not Marked"

            if att_date is None:
                att_date = "-"

            tk.Label(
                report_frame,
                text=f"{roll_no} - {name} - {att_date} - {status}",
                font=("Arial", 11),
                bg="#eaf2ff"
            ).pack(pady=4)

    tk.Button(
        report_frame,
        text="Back to Dashboard",
        width=20,
        command=lambda: [
            report_frame.pack_forget(),
            show_dashboard()
        ]
    ).pack(pady=20)


# ================= LOGIN PAGE UI =================

tk.Label(
    login_frame,
    text="Student Attendance System",
    font=("Arial", 22, "bold"),
    bg="#eaf2ff",
    fg="#174a8b"
).pack(pady=25)

tk.Label(
    login_frame,
    text="Username",
    font=("Arial", 12),
    bg="#eaf2ff"
).pack()

username_entry = tk.Entry(
    login_frame,
    width=30
)
username_entry.pack(pady=5)

tk.Label(
    login_frame,
    text="Password",
    font=("Arial", 12),
    bg="#eaf2ff"
).pack()

password_entry = tk.Entry(
    login_frame,
    width=30,
    show="*"
)
password_entry.pack(pady=5)

tk.Button(
    login_frame,
    text="Login",
    width=15,
    command=login
).pack(pady=20)

login_frame.pack(pady=30)


# ================= ADD STUDENT PAGE UI =================

tk.Label(
    student_frame,
    text="Add Student",
    font=("Arial", 22, "bold"),
    bg="#eaf2ff",
    fg="#174a8b"
).pack(pady=20)

tk.Label(
    student_frame,
    text="Student Name",
    bg="#eaf2ff"
).pack()

name_entry = tk.Entry(
    student_frame,
    width=30
)
name_entry.pack(pady=5)

tk.Label(
    student_frame,
    text="Roll Number",
    bg="#eaf2ff"
).pack()

roll_entry = tk.Entry(
    student_frame,
    width=30
)
roll_entry.pack(pady=5)

tk.Button(
    student_frame,
    text="Add Student",
    width=20,
    command=add_student
).pack(pady=15)

tk.Button(
    student_frame,
    text="Back to Dashboard",
    width=20,
    command=lambda: [
        student_frame.pack_forget(),
        show_dashboard()
    ]
).pack(pady=5)


# ================= START =================

root.mainloop()