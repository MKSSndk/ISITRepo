import tkinter as tk
from tkinter import ttk, messagebox

from auth import authenticate
from permissions import has_permission
from services import (
    fetch_students,
    fetch_teachers,
    fetch_groups,
    fetch_disciplines,
    fetch_classes,
    fetch_classes_for_teacher,
    fetch_grades,
    fetch_grades_for_student,
    fetch_student_profile,
    fetch_applicants,
    fetch_applicant_profile,
    fetch_directions,
    fetch_directions_for_applicant,
    add_grade,
    fetch_student_choices,
    fetch_teacher_choices,
    fetch_discipline_choices,
    add_student,
    add_teacher,
    add_applicant,
    fetch_users,
)


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Dean Office - Login")
        self.root.geometry("420x280")
        self.root.resizable(False, False)
        self.build_ui()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Virtual Dean Office", font=("Arial", 16, "bold")).pack(pady=(10, 20))

        ttk.Label(frame, text="Username").pack(anchor="w")
        self.username_entry = ttk.Entry(frame)
        self.username_entry.pack(fill="x", pady=(5, 10))

        ttk.Label(frame, text="Password").pack(anchor="w")
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.pack(fill="x", pady=(5, 15))

        ttk.Button(frame, text="Login", command=self.login).pack(fill="x", pady=10)

        ttk.Label(
            frame,
            text="admin / dean / teacher / student / applicant",
            font=("Arial", 9)
        ).pack(pady=(10, 0))

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning", "Enter username and password")
            return

        try:
            user = authenticate(username, password)
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
            return

        if not user:
            messagebox.showerror("Error", "Invalid username or password")
            return

        self.root.destroy()
        new_root = tk.Tk()
        MainWindow(new_root, user)
        new_root.mainloop()


class MainWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Virtual Dean Office")
        self.root.geometry("1150x680")
        self.build_ui()

    def build_ui(self):
        header = ttk.Frame(self.root, padding=10)
        header.pack(fill="x")

        ttk.Label(
            header,
            text=f"User: {self.user['full_name']} | Login: {self.user['username']} | Role: {self.user['role']}",
            font=("Arial", 11, "bold")
        ).pack(anchor="w")

        body = ttk.Frame(self.root, padding=10)
        body.pack(fill="both", expand=True)

        self.menu_frame = ttk.Frame(body)
        self.menu_frame.pack(side="left", fill="y", padx=(0, 10))

        self.content_frame = ttk.Frame(body)
        self.content_frame.pack(side="left", fill="both", expand=True)

        role = self.user["role"]

        if role == "admin":
            ttk.Button(self.menu_frame, text="Users", command=self.show_users).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Students", command=self.show_students).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Teachers", command=self.show_teachers).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Applicants", command=self.show_applicants).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Groups", command=self.show_groups).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Disciplines", command=self.show_disciplines).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Classes", command=self.show_classes).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Grades", command=self.show_grades).pack(fill="x", pady=5)

        elif role == "dean":
            ttk.Button(self.menu_frame, text="Students", command=self.show_students).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Teachers", command=self.show_teachers).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Applicants", command=self.show_applicants).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Directions", command=self.show_directions).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Groups", command=self.show_groups).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Grades", command=self.show_grades).pack(fill="x", pady=5)

        elif role == "teacher":
            ttk.Button(self.menu_frame, text="My Classes", command=self.show_teacher_classes).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Grades", command=self.show_grades).pack(fill="x", pady=5)

        elif role == "student":
            ttk.Button(self.menu_frame, text="My Profile", command=self.show_student_profile).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="My Grades", command=self.show_student_grades).pack(fill="x", pady=5)

        elif role == "applicant":
            ttk.Button(self.menu_frame, text="My Profile", command=self.show_applicant_profile).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="My Directions", command=self.show_applicant_directions).pack(fill="x", pady=5)

        ttk.Button(self.menu_frame, text="Exit", command=self.root.destroy).pack(fill="x", pady=(20, 0))
        self.show_welcome()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def make_tree(self, columns, headers):
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        for col, header in zip(columns, headers):
            tree.heading(col, text=header)
            tree.column(col, width=150, anchor="center")
        tree.pack(fill="both", expand=True)
        return tree

    def show_welcome(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Welcome to Virtual Dean Office", font=("Arial", 16, "bold")).pack(pady=20)

    def show_users(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Users", font=("Arial", 14, "bold")).pack(pady=10)

        rows = fetch_users()
        tree = self.make_tree(("id", "username", "full_name", "role"), ("ID", "Username", "Full name", "Role"))
        for row in rows:
            tree.insert("", "end", values=(row["id"], row["username"], row["full_name"], row["role"]))

    def show_students(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Students", font=("Arial", 14, "bold")).pack(pady=10)

        if self.user["role"] == "admin":
            ttk.Button(self.content_frame, text="Add Student", command=self.open_add_student_window).pack(pady=(0, 10))

        rows = fetch_students()
        tree = self.make_tree(("id", "card", "fio", "status", "enrollment", "group"), ("ID", "Card", "FIO", "Status", "Enrollment", "Group"))
        for row in rows:
            fio = f"{row['last_name']} {row['first_name']} {row.get('middle_name') or ''}".strip()
            tree.insert("", "end", values=(row["id"], row["student_card_number"], fio, row["status"], row["enrollment_date"], row["group_name"]))

    def show_teachers(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Teachers", font=("Arial", 14, "bold")).pack(pady=10)

        if self.user["role"] == "admin":
            ttk.Button(self.content_frame, text="Add Teacher", command=self.open_add_teacher_window).pack(pady=(0, 10))

        rows = fetch_teachers()
        tree = self.make_tree(("id", "fio", "department", "email"), ("ID", "FIO", "Department", "Email"))
        for row in rows:
            fio = f"{row['last_name']} {row['first_name']} {row.get('middle_name') or ''}".strip()
            tree.insert("", "end", values=(row["id"], fio, row["department"], row["email"]))

    def show_applicants(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Applicants", font=("Arial", 14, "bold")).pack(pady=10)

        if self.user["role"] == "admin":
            ttk.Button(self.content_frame, text="Add Applicant", command=self.open_add_applicant_window).pack(pady=(0, 10))

        rows = fetch_applicants()
        tree = self.make_tree(
            ("id", "fio", "birth_date", "phone", "email", "reg_date", "status"),
            ("ID", "FIO", "Birth date", "Phone", "Email", "Registration", "Status")
        )
        for row in rows:
            fio = f"{row['last_name']} {row['first_name']} {row.get('middle_name') or ''}".strip()
            tree.insert("", "end", values=(row["id"], fio, row["birth_date"], row["phone"], row["email"], row["registration_date"], row["status"]))

    def show_groups(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Groups", font=("Arial", 14, "bold")).pack(pady=10)
        rows = fetch_groups()
        tree = self.make_tree(("id", "name", "year", "course", "active"), ("ID", "Name", "Year", "Course", "Active"))
        for row in rows:
            tree.insert("", "end", values=(row["id"], row["name"], row["year_of_admission"], row["course"], row["active"]))

    def show_disciplines(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Disciplines", font=("Arial", 14, "bold")).pack(pady=10)
        rows = fetch_disciplines()
        tree = self.make_tree(("id", "name", "credits", "description"), ("ID", "Name", "Credits", "Description"))
        for row in rows:
            tree.insert("", "end", values=(row["id"], row["name"], row["credits"], row["description"]))

    def show_classes(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Classes", font=("Arial", 14, "bold")).pack(pady=10)
        rows = fetch_classes()
        tree = self.make_tree(("id", "discipline", "group", "teacher", "date", "start", "end", "type"),
                              ("ID", "Discipline", "Group", "Teacher", "Date", "Start", "End", "Type"))
        for row in rows:
            tree.insert("", "end", values=(row["id"], row["discipline"], row["group_name"], row["teacher_name"], row["class_date"], row["time_start"], row["time_end"], row["class_type"]))

    def show_teacher_classes(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="My Classes", font=("Arial", 14, "bold")).pack(pady=10)
        rows = fetch_classes_for_teacher(self.user["teacher_id"])
        tree = self.make_tree(("id", "discipline", "group", "date", "start", "end", "type"),
                              ("ID", "Discipline", "Group", "Date", "Start", "End", "Type"))
        for row in rows:
            tree.insert("", "end", values=(row["id"], row["discipline"], row["group_name"], row["class_date"], row["time_start"], row["time_end"], row["class_type"]))

    def show_grades(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Grades", font=("Arial", 14, "bold")).pack(pady=10)

        if self.user["role"] in ("teacher", "admin"):
            ttk.Button(self.content_frame, text="Add Grade", command=self.open_add_grade_window).pack(pady=(0, 10))

        rows = fetch_grades()
        tree = self.make_tree(("id", "student", "discipline", "teacher", "grade", "date", "comment"),
                              ("ID", "Student", "Discipline", "Teacher", "Grade", "Date", "Comment"))
        for row in rows:
            tree.insert("", "end", values=(row["id"], row["student_name"], row["discipline"], row["teacher_name"], row["grade"], row["grade_date"], row["comment"]))

    def show_student_profile(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="My Profile", font=("Arial", 14, "bold")).pack(pady=10)

        row = fetch_student_profile(self.user["student_id"])
        if not row:
            ttk.Label(self.content_frame, text="Student profile not found").pack()
            return

        fio = f"{row['last_name']} {row['first_name']} {row.get('middle_name') or ''}".strip()
        text = (
            f"ID: {row['id']}\n"
            f"FIO: {fio}\n"
            f"Card: {row['student_card_number']}\n"
            f"Status: {row['status']}\n"
            f"Enrollment date: {row['enrollment_date']}\n"
            f"Group: {row['group_name']}"
        )
        ttk.Label(self.content_frame, text=text, font=("Arial", 11), justify="left").pack(anchor="w", padx=20, pady=20)

    def show_student_grades(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="My Grades", font=("Arial", 14, "bold")).pack(pady=10)

        rows = fetch_grades_for_student(self.user["student_id"])
        tree = self.make_tree(("discipline", "grade", "date", "comment"), ("Discipline", "Grade", "Date", "Comment"))
        for row in rows:
            tree.insert("", "end", values=(row["discipline"], row["grade"], row["grade_date"], row["comment"]))

    def show_applicant_profile(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="My Applicant Profile", font=("Arial", 14, "bold")).pack(pady=10)

        row = fetch_applicant_profile(self.user["applicant_id"])
        if not row:
            ttk.Label(self.content_frame, text="Applicant profile not found").pack()
            return

        fio = f"{row['last_name']} {row['first_name']} {row.get('middle_name') or ''}".strip()
        text = (
            f"ID: {row['id']}\n"
            f"FIO: {fio}\n"
            f"Birth date: {row['birth_date']}\n"
            f"Phone: {row['phone']}\n"
            f"Email: {row['email']}\n"
            f"Registration date: {row['registration_date']}\n"
            f"Status: {row['status']}"
        )
        ttk.Label(self.content_frame, text=text, font=("Arial", 11), justify="left").pack(anchor="w", padx=20, pady=20)

    def show_applicant_directions(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="My Directions", font=("Arial", 14, "bold")).pack(pady=10)

        rows = fetch_directions_for_applicant(self.user["applicant_id"])
        tree = self.make_tree(
            ("code", "name", "level", "form", "status", "date"),
            ("Code", "Direction", "Level", "Study form", "Application status", "Application date")
        )
        for row in rows:
            tree.insert("", "end", values=(
                row["code"],
                row["name"],
                row["education_level"],
                row["study_form"],
                row["application_status"],
                row["application_date"]
            ))

    def show_directions(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Directions", font=("Arial", 14, "bold")).pack(pady=10)

        rows = fetch_directions()
        tree = self.make_tree(("id", "code", "name", "level", "form", "active"),
                              ("ID", "Code", "Name", "Level", "Study form", "Active"))
        for row in rows:
            tree.insert("", "end", values=(row["id"], row["code"], row["name"], row["education_level"], row["study_form"], row["active"]))

    def open_add_grade_window(self):
        window = tk.Toplevel(self.root)
        window.title("Add Grade")
        window.geometry("430x320")

        frame = ttk.Frame(window, padding=15)
        frame.pack(fill="both", expand=True)

        students = fetch_student_choices()
        disciplines = fetch_discipline_choices()
        teachers = fetch_teacher_choices()

        ttk.Label(frame, text="Student").pack(anchor="w")
        student_cb = ttk.Combobox(frame, state="readonly", values=[f"{x['id']} - {x['full_name']}" for x in students])
        student_cb.pack(fill="x", pady=5)

        ttk.Label(frame, text="Discipline").pack(anchor="w")
        discipline_cb = ttk.Combobox(frame, state="readonly", values=[f"{x['id']} - {x['name']}" for x in disciplines])
        discipline_cb.pack(fill="x", pady=5)

        ttk.Label(frame, text="Teacher").pack(anchor="w")
        teacher_cb = ttk.Combobox(frame, state="readonly", values=[f"{x['id']} - {x['full_name']}" for x in teachers])
        teacher_cb.pack(fill="x", pady=5)

        if self.user["role"] == "teacher" and self.user["teacher_id"]:
            for i, value in enumerate(teacher_cb["values"]):
                if value.startswith(f"{self.user['teacher_id']} - "):
                    teacher_cb.current(i)
                    teacher_cb.configure(state="disabled")
                    break

        ttk.Label(frame, text="Grade").pack(anchor="w")
        grade_entry = ttk.Entry(frame)
        grade_entry.pack(fill="x", pady=5)

        ttk.Label(frame, text="Comment").pack(anchor="w")
        comment_entry = ttk.Entry(frame)
        comment_entry.pack(fill="x", pady=5)

        def save():
            try:
                student_id = int(student_cb.get().split(" - ")[0])
                discipline_id = int(discipline_cb.get().split(" - ")[0])
                teacher_id = self.user["teacher_id"] if self.user["role"] == "teacher" else int(teacher_cb.get().split(" - ")[0])
                grade_value = float(grade_entry.get().strip())
                comment = comment_entry.get().strip()

                add_grade(student_id, discipline_id, teacher_id, grade_value, comment)
                messagebox.showinfo("Success", "Grade added")
                window.destroy()
                self.show_grades()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(frame, text="Save", command=save).pack(fill="x", pady=15)

    def open_add_student_window(self):
        self.open_person_window(
            title="Add Student",
            fields=("Card number", "Last name", "First name", "Middle name", "Status", "Enrollment date YYYY-MM-DD"),
            save_callback=lambda values: add_student(*values)
        )

    def open_add_teacher_window(self):
        self.open_person_window(
            title="Add Teacher",
            fields=("Last name", "First name", "Middle name", "Department", "Email"),
            save_callback=lambda values: add_teacher(*values)
        )

    def open_add_applicant_window(self):
        self.open_person_window(
            title="Add Applicant",
            fields=("Last name", "First name", "Middle name", "Birth date YYYY-MM-DD", "Phone", "Email", "Registration date YYYY-MM-DD", "Status"),
            save_callback=lambda values: add_applicant(*values)
        )

    def open_person_window(self, title, fields, save_callback):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("420x420")

        frame = ttk.Frame(window, padding=15)
        frame.pack(fill="both", expand=True)

        entries = []
        for field in fields:
            ttk.Label(frame, text=field).pack(anchor="w")
            entry = ttk.Entry(frame)
            entry.pack(fill="x", pady=5)
            entries.append(entry)

        def save():
            try:
                values = [e.get().strip() or None for e in entries]
                save_callback(values)
                messagebox.showinfo("Success", f"{title} saved")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ttk.Button(frame, text="Save", command=save).pack(fill="x", pady=15)