import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ============================================================
# DATABASE
# ============================================================

DATABASE = "subject_allocation.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            semester INTEGER NOT NULL
        )
    """)

    # Subjects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            semester INTEGER NOT NULL,
            capacity INTEGER NOT NULL,
            prerequisite TEXT
        )
    """)

    # Preferences table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            preference_order INTEGER NOT NULL,
            UNIQUE(student_id, subject_id),
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    """)

    # Allocations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS allocations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            preference_order INTEGER,
            allocation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(student_id, subject_id),
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(subject_id) REFERENCES subjects(id)
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# SAMPLE DATA
# ============================================================

def insert_sample_data():
    conn = get_connection()
    cursor = conn.cursor()

    students = [
        ("STU001", "Rahul Sharma", "Computer Science", 5),
        ("STU002", "Priya Singh", "Computer Science", 5),
        ("STU003", "Aman Kumar", "Information Technology", 5),
        ("STU004", "Sneha Das", "Computer Science", 5),
        ("STU005", "Arjun Roy", "Information Technology", 5)
    ]

    subjects = [
        ("CS501", "Artificial Intelligence", "Computer Science", 5, 3, ""),
        ("CS502", "Machine Learning", "Computer Science", 5, 3, "CS501"),
        ("CS503", "Data Science", "Computer Science", 5, 3, ""),
        ("CS504", "Cyber Security", "Computer Science", 5, 2, ""),
        ("CS505", "Cloud Computing", "Computer Science", 5, 2, ""),
        ("IT501", "Web Technologies", "Information Technology", 5, 3, ""),
        ("IT502", "Data Analytics", "Information Technology", 5, 3, ""),
    ]

    for student in students:
        try:
            cursor.execute("""
                INSERT INTO students
                (roll_no, name, department, semester)
                VALUES (?, ?, ?, ?)
            """, student)
        except sqlite3.IntegrityError:
            pass

    for subject in subjects:
        try:
            cursor.execute("""
                INSERT INTO subjects
                (code, name, department, semester, capacity, prerequisite)
                VALUES (?, ?, ?, ?, ?, ?)
            """, subject)
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()


# ============================================================
# MAIN APPLICATION
# ============================================================

class SubjectAllocationSystem:

    def __init__(self, root):
        self.root = root

        self.root.title("University Subject Allocation System")
        self.root.geometry("1200x720")
        self.root.minsize(1000, 650)

        self.style = ttk.Style()

        try:
            self.style.theme_use("clam")
        except:
            pass

        self.create_header()
        self.create_notebook()

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg="#1f4e78",
            height=80
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="UNIVERSITY SUBJECT ALLOCATION SYSTEM",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1f4e78"
        )

        title.pack(pady=12)

        subtitle = tk.Label(
            header,
            text="Preference Based Automatic Subject Allocation",
            font=("Arial", 10),
            fg="white",
            bg="#1f4e78"
        )

        subtitle.pack()

    # --------------------------------------------------------
    # NOTEBOOK
    # --------------------------------------------------------

    def create_notebook(self):

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.dashboard_tab = ttk.Frame(self.notebook)
        self.students_tab = ttk.Frame(self.notebook)
        self.subjects_tab = ttk.Frame(self.notebook)
        self.preferences_tab = ttk.Frame(self.notebook)
        self.allocation_tab = ttk.Frame(self.notebook)
        self.report_tab = ttk.Frame(self.notebook)

        self.notebook.add(
            self.dashboard_tab,
            text="Dashboard"
        )

        self.notebook.add(
            self.students_tab,
            text="Students"
        )

        self.notebook.add(
            self.subjects_tab,
            text="Subjects"
        )

        self.notebook.add(
            self.preferences_tab,
            text="Preferences"
        )

        self.notebook.add(
            self.allocation_tab,
            text="Allocation"
        )

        self.notebook.add(
            self.report_tab,
            text="Reports"
        )

        self.create_dashboard()
        self.create_students_tab()
        self.create_subjects_tab()
        self.create_preferences_tab()
        self.create_allocation_tab()
        self.create_report_tab()

    # ========================================================
    # DASHBOARD
    # ========================================================

    def create_dashboard(self):

        frame = tk.Frame(
            self.dashboard_tab,
            bg="#f5f7fa"
        )

        frame.pack(fill="both", expand=True)

        welcome = tk.Label(
            frame,
            text="Subject Allocation Dashboard",
            font=("Arial", 24, "bold"),
            bg="#f5f7fa",
            fg="#1f4e78"
        )

        welcome.pack(pady=30)

        cards_frame = tk.Frame(
            frame,
            bg="#f5f7fa"
        )

        cards_frame.pack(pady=20)

        self.student_count = tk.Label(
            cards_frame,
            text="Students\n0",
            font=("Arial", 18, "bold"),
            width=15,
            height=5,
            bg="#d9eaf7"
        )

        self.student_count.grid(
            row=0,
            column=0,
            padx=20
        )

        self.subject_count = tk.Label(
            cards_frame,
            text="Subjects\n0",
            font=("Arial", 18, "bold"),
            width=15,
            height=5,
            bg="#dff0d8"
        )

        self.subject_count.grid(
            row=0,
            column=1,
            padx=20
        )

        self.allocation_count = tk.Label(
            cards_frame,
            text="Allocations\n0",
            font=("Arial", 18, "bold"),
            width=15,
            height=5,
            bg="#fcf8e3"
        )

        self.allocation_count.grid(
            row=0,
            column=2,
            padx=20
        )

        refresh_button = ttk.Button(
            frame,
            text="Refresh Dashboard",
            command=self.refresh_dashboard
        )

        refresh_button.pack(pady=30)

        self.refresh_dashboard()

    def refresh_dashboard(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM students")
        students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM subjects")
        subjects = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM allocations")
        allocations = cursor.fetchone()[0]

        conn.close()

        self.student_count.config(
            text=f"Students\n{students}"
        )

        self.subject_count.config(
            text=f"Subjects\n{subjects}"
        )

        self.allocation_count.config(
            text=f"Allocations\n{allocations}"
        )

    # ========================================================
    # STUDENT TAB
    # ========================================================

    def create_students_tab(self):

        top = ttk.LabelFrame(
            self.students_tab,
            text="Add Student"
        )

        top.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            top,
            text="Roll Number:"
        ).grid(row=0, column=0, padx=5, pady=10)

        self.roll_entry = ttk.Entry(top, width=20)
        self.roll_entry.grid(row=0, column=1, padx=5)

        ttk.Label(
            top,
            text="Name:"
        ).grid(row=0, column=2, padx=5)

        self.name_entry = ttk.Entry(top, width=25)
        self.name_entry.grid(row=0, column=3, padx=5)

        ttk.Label(
            top,
            text="Department:"
        ).grid(row=1, column=0, padx=5, pady=10)

        self.department_entry = ttk.Entry(top, width=20)
        self.department_entry.grid(row=1, column=1, padx=5)

        ttk.Label(
            top,
            text="Semester:"
        ).grid(row=1, column=2, padx=5)

        self.semester_entry = ttk.Entry(top, width=10)
        self.semester_entry.grid(row=1, column=3, padx=5)

        ttk.Button(
            top,
            text="Add Student",
            command=self.add_student
        ).grid(
            row=0,
            column=4,
            rowspan=2,
            padx=20
        )

        table_frame = ttk.LabelFrame(
            self.students_tab,
            text="Registered Students"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        columns = (
            "ID",
            "Roll Number",
            "Name",
            "Department",
            "Semester"
        )

        self.student_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            self.student_tree.heading(
                column,
                text=column
            )

            self.student_tree.column(
                column,
                width=150
            )

        self.student_tree.pack(
            fill="both",
            expand=True
        )

        ttk.Button(
            self.students_tab,
            text="Refresh Students",
            command=self.load_students
        ).pack(pady=5)

        self.load_students()

    def add_student(self):

        roll = self.roll_entry.get().strip()
        name = self.name_entry.get().strip()
        department = self.department_entry.get().strip()
        semester = self.semester_entry.get().strip()

        if not roll or not name or not department or not semester:

            messagebox.showwarning(
                "Missing Data",
                "Please fill all fields."
            )

            return

        try:
            semester = int(semester)

        except ValueError:

            messagebox.showerror(
                "Invalid Semester",
                "Semester must be a number."
            )

            return

        conn = get_connection()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO students
                (roll_no, name, department, semester)
                VALUES (?, ?, ?, ?)
            """, (
                roll,
                name,
                department,
                semester
            ))

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Student added successfully."
            )

            self.roll_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.department_entry.delete(0, tk.END)
            self.semester_entry.delete(0, tk.END)

            self.load_students()
            self.refresh_dashboard()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "Roll number already exists."
            )

        finally:
            conn.close()

    def load_students(self):

        for item in self.student_tree.get_children():
            self.student_tree.delete(item)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, roll_no, name, department, semester
            FROM students
            ORDER BY id
        """)

        rows = cursor.fetchall()

        for row in rows:
            self.student_tree.insert(
                "",
                tk.END,
                values=row
            )

        conn.close()

    # ========================================================
    # SUBJECT TAB
    # ========================================================

    def create_subjects_tab(self):

        top = ttk.LabelFrame(
            self.subjects_tab,
            text="Add Subject"
        )

        top.pack(
            fill="x",
            padx=10,
            pady=10
        )

        fields = [
            ("Code:", 0, 0),
            ("Subject Name:", 0, 2),
            ("Department:", 1, 0),
            ("Semester:", 1, 2),
            ("Capacity:", 2, 0),
            ("Prerequisite:", 2, 2)
        ]

        for text, row, column in fields:

            ttk.Label(
                top,
                text=text
            ).grid(
                row=row,
                column=column,
                padx=5,
                pady=8
            )

        self.code_entry = ttk.Entry(
            top,
            width=20
        )

        self.code_entry.grid(
            row=0,
            column=1,
            padx=5
        )

        self.subject_name_entry = ttk.Entry(
            top,
            width=25
        )

        self.subject_name_entry.grid(
            row=0,
            column=3,
            padx=5
        )

        self.subject_department_entry = ttk.Entry(
            top,
            width=20
        )

        self.subject_department_entry.grid(
            row=1,
            column=1,
            padx=5
        )

        self.subject_semester_entry = ttk.Entry(
            top,
            width=10
        )

        self.subject_semester_entry.grid(
            row=1,
            column=3,
            padx=5
        )

        self.capacity_entry = ttk.Entry(
            top,
            width=10
        )

        self.capacity_entry.grid(
            row=2,
            column=1,
            padx=5
        )

        self.prerequisite_entry = ttk.Entry(
            top,
            width=20
        )

        self.prerequisite_entry.grid(
            row=2,
            column=3,
            padx=5
        )

        ttk.Button(
            top,
            text="Add Subject",
            command=self.add_subject
        ).grid(
            row=0,
            column=4,
            rowspan=3,
            padx=20
        )

        table_frame = ttk.LabelFrame(
            self.subjects_tab,
            text="Available Subjects"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        columns = (
            "ID",
            "Code",
            "Name",
            "Department",
            "Semester",
            "Capacity",
            "Prerequisite"
        )

        self.subject_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            self.subject_tree.heading(
                column,
                text=column
            )

            self.subject_tree.column(
                column,
                width=140
            )

        self.subject_tree.pack(
            fill="both",
            expand=True
        )

        ttk.Button(
            self.subjects_tab,
            text="Refresh Subjects",
            command=self.load_subjects
        ).pack(pady=5)

        self.load_subjects()

    def add_subject(self):

        code = self.code_entry.get().strip()
        name = self.subject_name_entry.get().strip()
        department = self.subject_department_entry.get().strip()
        semester = self.subject_semester_entry.get().strip()
        capacity = self.capacity_entry.get().strip()
        prerequisite = self.prerequisite_entry.get().strip()

        if not code or not name or not department:
            messagebox.showwarning(
                "Missing Data",
                "Please fill all required fields."
            )
            return

        try:
            semester = int(semester)
            capacity = int(capacity)

        except ValueError:
            messagebox.showerror(
                "Invalid Data",
                "Semester and capacity must be numbers."
            )
            return

        if capacity <= 0:
            messagebox.showerror(
                "Invalid Capacity",
                "Capacity must be greater than zero."
            )
            return

        conn = get_connection()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO subjects
                (
                    code,
                    name,
                    department,
                    semester,
                    capacity,
                    prerequisite
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                code,
                name,
                department,
                semester,
                capacity,
                prerequisite
            ))

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Subject added successfully."
            )

            for entry in [
                self.code_entry,
                self.subject_name_entry,
                self.subject_department_entry,
                self.subject_semester_entry,
                self.capacity_entry,
                self.prerequisite_entry
            ]:
                entry.delete(0, tk.END)

            self.load_subjects()
            self.refresh_dashboard()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "Subject code already exists."
            )

        finally:
            conn.close()

    def load_subjects(self):

        for item in self.subject_tree.get_children():
            self.subject_tree.delete(item)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                code,
                name,
                department,
                semester,
                capacity,
                prerequisite
            FROM subjects
            ORDER BY id
        """)

        rows = cursor.fetchall()

        for row in rows:
            self.subject_tree.insert(
                "",
                tk.END,
                values=row
            )

        conn.close()

    # ========================================================
    # PREFERENCE TAB
    # ========================================================

    def create_preferences_tab(self):

        frame = ttk.LabelFrame(
            self.preferences_tab,
            text="Set Student Preferences"
        )

        frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            frame,
            text="Student:"
        ).grid(row=0, column=0, padx=5, pady=10)

        self.preference_student_combo = ttk.Combobox(
            frame,
            width=40,
            state="readonly"
        )

        self.preference_student_combo.grid(
            row=0,
            column=1,
            padx=5
        )

        ttk.Button(
            frame,
            text="Load Students",
            command=self.load_preference_students
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        ttk.Label(
            frame,
            text="Subject:"
        ).grid(row=1, column=0, padx=5, pady=10)

        self.preference_subject_combo = ttk.Combobox(
            frame,
            width=40,
            state="readonly"
        )

        self.preference_subject_combo.grid(
            row=1,
            column=1,
            padx=5
        )

        ttk.Label(
            frame,
            text="Preference Order:"
        ).grid(row=2, column=0, padx=5, pady=10)

        self.preference_order_entry = ttk.Entry(
            frame,
            width=10
        )

        self.preference_order_entry.grid(
            row=2,
            column=1,
            sticky="w",
            padx=5
        )

        ttk.Button(
            frame,
            text="Add Preference",
            command=self.add_preference
        ).grid(
            row=3,
            column=1,
            pady=10
        )

        table_frame = ttk.LabelFrame(
            self.preferences_tab,
            text="Student Preferences"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        columns = (
            "Student",
            "Subject",
            "Preference"
        )

        self.preference_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            self.preference_tree.heading(
                column,
                text=column
            )

            self.preference_tree.column(
                column,
                width=250
            )

        self.preference_tree.pack(
            fill="both",
            expand=True
        )

        self.load_preference_students()
        self.load_preference_subjects()
        self.load_preferences()

    def load_preference_students(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, roll_no, name
            FROM students
            ORDER BY roll_no
        """)

        rows = cursor.fetchall()

        self.preference_students = rows

        values = [
            f"{row[0]} - {row[1]} - {row[2]}"
            for row in rows
        ]

        self.preference_student_combo["values"] = values

        conn.close()

    def load_preference_subjects(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, code, name
            FROM subjects
            ORDER BY code
        """)

        rows = cursor.fetchall()

        self.preference_subjects = rows

        values = [
            f"{row[0]} - {row[1]} - {row[2]}"
            for row in rows
        ]

        self.preference_subject_combo["values"] = values

        conn.close()

    def add_preference(self):

        student_value = self.preference_student_combo.get()
        subject_value = self.preference_subject_combo.get()
        order_value = self.preference_order_entry.get().strip()

        if not student_value or not subject_value or not order_value:

            messagebox.showwarning(
                "Missing Data",
                "Please select student, subject and preference order."
            )

            return

        try:
            student_id = int(student_value.split(" - ")[0])
            subject_id = int(subject_value.split(" - ")[0])
            preference_order = int(order_value)

        except ValueError:

            messagebox.showerror(
                "Error",
                "Invalid preference order."
            )

            return

        if preference_order <= 0:

            messagebox.showerror(
                "Error",
                "Preference order must be greater than zero."
            )

            return

        conn = get_connection()

        try:

            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO preferences
                (
                    student_id,
                    subject_id,
                    preference_order
                )
                VALUES (?, ?, ?)
            """, (
                student_id,
                subject_id,
                preference_order
            ))

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Preference added successfully."
            )

            self.preference_order_entry.delete(
                0,
                tk.END
            )

            self.load_preferences()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "This preference already exists."
            )

        finally:
            conn.close()

    def load_preferences(self):

        for item in self.preference_tree.get_children():
            self.preference_tree.delete(item)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                s.roll_no || ' - ' || s.name,
                sub.code || ' - ' || sub.name,
                p.preference_order

            FROM preferences p

            JOIN students s
                ON p.student_id = s.id

            JOIN subjects sub
                ON p.subject_id = sub.id

            ORDER BY
                s.roll_no,
                p.preference_order
        """)

        rows = cursor.fetchall()

        for row in rows:

            self.preference_tree.insert(
                "",
                tk.END,
                values=row
            )

        conn.close()

    # ========================================================
    # ALLOCATION TAB
    # ========================================================

    def create_allocation_tab(self):

        frame = ttk.Frame(
            self.allocation_tab
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        instruction = tk.Label(
            frame,
            text=(
                "The system allocates subjects according to student "
                "preference order while checking capacity and prerequisites."
            ),
            font=("Arial", 11),
            wraplength=900
        )

        instruction.pack(pady=10)

        ttk.Button(
            frame,
            text="RUN AUTOMATIC ALLOCATION",
            command=self.run_allocation
        ).pack(pady=10)

        ttk.Button(
            frame,
            text="Clear Existing Allocations",
            command=self.clear_allocations
        ).pack(pady=5)

        table_frame = ttk.LabelFrame(
            frame,
            text="Allocation Results"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            pady=10
        )

        columns = (
            "Roll No",
            "Student",
            "Subject",
            "Preference",
            "Status"
        )

        self.allocation_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            self.allocation_tree.heading(
                column,
                text=column
            )

            self.allocation_tree.column(
                column,
                width=180
            )

        self.allocation_tree.pack(
            fill="both",
            expand=True
        )

        self.load_allocations()

    def run_allocation(self):

        conn = get_connection()
        cursor = conn.cursor()

        # Remove previous allocation
        cursor.execute("DELETE FROM allocations")

        # Get all students
        cursor.execute("""
            SELECT id, roll_no, name, department, semester
            FROM students
            ORDER BY id
        """)

        students = cursor.fetchall()

        total_allocated = 0

        for student in students:

            student_id = student[0]

            # Get preferences in priority order
            cursor.execute("""
                SELECT
                    p.subject_id,
                    p.preference_order,
                    sub.capacity,
                    sub.prerequisite,
                    sub.code

                FROM preferences p

                JOIN subjects sub
                    ON p.subject_id = sub.id

                WHERE p.student_id = ?

                ORDER BY p.preference_order ASC
            """, (student_id,))

            preferences = cursor.fetchall()

            for preference in preferences:

                subject_id = preference[0]
                preference_order = preference[1]
                prerequisite = preference[3]

                # ------------------------------------------------
                # CHECK CAPACITY
                # ------------------------------------------------

                cursor.execute("""
                    SELECT COUNT(*)
                    FROM allocations
                    WHERE subject_id = ?
                """, (subject_id,))

                current_count = cursor.fetchone()[0]

                capacity = preference[2]

                if current_count >= capacity:
                    continue

                # ------------------------------------------------
                # CHECK PREREQUISITE
                # ------------------------------------------------

                if prerequisite:

                    cursor.execute("""
                        SELECT id
                        FROM subjects
                        WHERE code = ?
                    """, (prerequisite,))

                    prerequisite_subject = cursor.fetchone()

                    if prerequisite_subject:

                        prerequisite_id = prerequisite_subject[0]

                        # In a real system this could check completed
                        # previous-semester subjects.
                        # Here we check whether the student has the
                        # prerequisite in their preferences.

                        cursor.execute("""
                            SELECT id
                            FROM preferences
                            WHERE student_id = ?
                            AND subject_id = ?
                        """, (
                            student_id,
                            prerequisite_id
                        ))

                        if cursor.fetchone() is None:
                            continue

                # ------------------------------------------------
                # ALLOCATE SUBJECT
                # ------------------------------------------------

                try:

                    cursor.execute("""
                        INSERT INTO allocations
                        (
                            student_id,
                            subject_id,
                            preference_order
                        )
                        VALUES (?, ?, ?)
                    """, (
                        student_id,
                        subject_id,
                        preference_order
                    ))

                    total_allocated += 1

                except sqlite3.IntegrityError:

                    pass

        conn.commit()
        conn.close()

        self.load_allocations()
        self.refresh_dashboard()

        messagebox.showinfo(
            "Allocation Complete",
            f"Automatic allocation completed.\n\n"
            f"Total allocations: {total_allocated}"
        )

    def clear_allocations(self):

        answer = messagebox.askyesno(
            "Confirm",
            "Are you sure you want to clear all allocations?"
        )

        if not answer:
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM allocations")

        conn.commit()
        conn.close()

        self.load_allocations()
        self.refresh_dashboard()

    def load_allocations(self):

        for item in self.allocation_tree.get_children():
            self.allocation_tree.delete(item)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                s.roll_no,
                s.name,
                sub.code || ' - ' || sub.name,
                a.preference_order,
                'Allocated'

            FROM allocations a

            JOIN students s
                ON a.student_id = s.id

            JOIN subjects sub
                ON a.subject_id = sub.id

            ORDER BY
                s.roll_no,
                a.preference_order
        """)

        rows = cursor.fetchall()

        for row in rows:

            self.allocation_tree.insert(
                "",
                tk.END,
                values=row
            )

        conn.close()

    # ========================================================
    # REPORT TAB
    # ========================================================

    def create_report_tab(self):

        top = ttk.Frame(
            self.report_tab
        )

        top.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Button(
            top,
            text="Generate Report",
            command=self.generate_report
        ).pack(side="left", padx=5)

        ttk.Button(
            top,
            text="Subject Occupancy",
            command=self.subject_occupancy
        ).pack(side="left", padx=5)

        ttk.Button(
            top,
            text="Student Allocation",
            command=self.student_report
        ).pack(side="left", padx=5)

        self.report_text = tk.Text(
            self.report_tab,
            font=("Consolas", 11),
            wrap="word"
        )

        self.report_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    def generate_report(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM students"
        )

        students = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM subjects"
        )

        subjects = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM allocations"
        )

        allocations = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM students s
            WHERE NOT EXISTS (
                SELECT 1
                FROM allocations a
                WHERE a.student_id = s.id
            )
        """)

        unallocated_students = cursor.fetchone()[0]

        conn.close()

        report = f"""
========================================
       SUBJECT ALLOCATION REPORT
========================================

Total Students       : {students}
Total Subjects       : {subjects}
Total Allocations    : {allocations}
Unallocated Students : {unallocated_students}

Allocation Rate      : {
    round((allocations / students) * 100, 2)
    if students > 0 else 0
}%

========================================
"""

        self.report_text.delete(
            "1.0",
            tk.END
        )

        self.report_text.insert(
            tk.END,
            report
        )

    def subject_occupancy(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                sub.code,
                sub.name,
                sub.capacity,
                COUNT(a.id) AS allocated

            FROM subjects sub

            LEFT JOIN allocations a
                ON sub.id = a.subject_id

            GROUP BY sub.id

            ORDER BY sub.code
        """)

        rows = cursor.fetchall()

        conn.close()

        report = """
========================================
          SUBJECT OCCUPANCY
========================================

"""

        for row in rows:

            code = row[0]
            name = row[1]
            capacity = row[2]
            allocated = row[3]

            percentage = (
                allocated / capacity * 100
                if capacity > 0
                else 0
            )

            report += (
                f"{code:<10} "
                f"{name:<25} "
                f"{allocated}/{capacity} "
                f"({percentage:.1f}%)\n"
            )

        self.report_text.delete(
            "1.0",
            tk.END
        )

        self.report_text.insert(
            tk.END,
            report
        )

    def student_report(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                s.roll_no,
                s.name,
                sub.code,
                sub.name,
                a.preference_order

            FROM allocations a

            JOIN students s
                ON a.student_id = s.id

            JOIN subjects sub
                ON a.subject_id = sub.id

            ORDER BY
                s.roll_no,
                a.preference_order
        """)

        rows = cursor.fetchall()

        conn.close()

        report = """
========================================
       STUDENT ALLOCATION REPORT
========================================

"""

        current_student = ""

        for row in rows:

            roll = row[0]
            name = row[1]
            code = row[2]
            subject = row[3]
            preference = row[4]

            if roll != current_student:

                report += (
                    f"\n{roll} - {name}\n"
                    f"{'-' * 40}\n"
                )

                current_student = roll

            report += (
                f"Preference {preference}: "
                f"{code} - {subject}\n"
            )

        self.report_text.delete(
            "1.0",
            tk.END
        )

        self.report_text.insert(
            tk.END,
            report
        )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    initialize_database()
    insert_sample_data()

    root = tk.Tk()

    application = SubjectAllocationSystem(root)

    root.mainloop()