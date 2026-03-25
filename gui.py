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


BG_MAIN = "#F4FBFB"
BG_PANEL = "#FFFDFD"

ACCENT = "#2FB8B8"
ACCENT_DARK = "#238F8F"
ACCENT_LIGHT = "#DDF6F6"

PINK_TEXT = "#C96F8D"
PINK_TITLE = "#B85D7A"
PINK_SOFT = "#F8DCE7"
PINK_LIGHT = "#FCEAF1"
PINK_ACCENT = "#E79AB0"

TEXT_MAIN = "#1F2D3D"
TEXT_MUTED = "#6B7280"
BORDER = "#CDECEC"
TREE_HEADING = "#D9F3F3"
WHITE = "#FFFFFF"


#стили тут 

def setup_styles(root):
    root.configure(bg=BG_MAIN)

    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        ".",
        background=BG_MAIN,
        foreground=TEXT_MAIN,
        font=("Segoe UI", 10)
    )

    style.configure("TFrame", background=BG_MAIN)

    style.configure(
        "Card.TFrame",
        background=BG_PANEL,
        relief="flat",
        borderwidth=1
    )

    style.configure(
        "TLabel",
        background=BG_MAIN,
        foreground=PINK_TEXT,
        font=("Segoe UI", 10)
    )

    style.configure(
        "Title.TLabel",
        background=BG_PANEL,
        foreground=PINK_TITLE,
        font=("Segoe UI", 18, "bold"),
        padding=0
    )

    style.configure(
        "Subtitle.TLabel",
        background=BG_PANEL,
        foreground=PINK_TEXT,
        font=("Segoe UI", 10),
        padding=0
    )

    style.configure(
        "Section.TLabel",
        background=BG_MAIN,
        foreground=PINK_TITLE,
        font=("Segoe UI", 14, "bold")
    )

    style.configure(
        "Info.TLabel",
        background=BG_PANEL,
        foreground=PINK_TEXT,
        font=("Segoe UI", 10)
    )

    style.configure(
        "BrandIcon.TLabel",
        background=BG_MAIN,
        foreground=ACCENT,
        font=("Segoe UI", 14, "bold")
    )

    style.configure(
        "BrandText.TLabel",
        background=BG_MAIN,
        foreground=PINK_TITLE,
        font=("Segoe UI", 10, "bold")
    )

    style.configure(
        "TButton",
        font=("Segoe UI", 10, "bold"),
        padding=(10, 8),
        background=ACCENT,
        foreground=WHITE,
        borderwidth=0,
        focusthickness=0
    )
    style.map(
        "TButton",
        background=[
            ("active", ACCENT_DARK),
            ("pressed", ACCENT_DARK)
        ],
        foreground=[
            ("disabled", "#DCE3E6"),
            ("!disabled", WHITE)
        ]
    )

    style.configure(
        "Menu.TButton",
        font=("Segoe UI", 10, "bold"),
        padding=(12, 10),
        background=ACCENT_LIGHT,
        foreground=PINK_TITLE,
        borderwidth=0
    )
    style.map(
        "Menu.TButton",
        background=[
            ("active", PINK_SOFT),
            ("pressed", "#F3C9D8")
        ],
        foreground=[
            ("active", PINK_TITLE),
            ("pressed", PINK_TITLE)
        ]
    )

    style.configure(
        "Danger.TButton",
        font=("Segoe UI", 10, "bold"),
        padding=(10, 8),
        background=PINK_ACCENT,
        foreground=WHITE,
        borderwidth=0
    )
    style.map(
        "Danger.TButton",
        background=[
            ("active", "#D97D9A"),
            ("pressed", "#D97D9A")
        ]
    )

    style.configure(
        "TEntry",
        fieldbackground=WHITE,
        background=WHITE,
        foreground=TEXT_MAIN,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER,
        insertcolor=TEXT_MAIN,
        padding=6
    )

    style.configure(
        "TCombobox",
        fieldbackground=WHITE,
        background=WHITE,
        foreground=TEXT_MAIN,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER,
        padding=6
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", WHITE)],
        selectbackground=[("readonly", ACCENT_LIGHT)],
        selectforeground=[("readonly", TEXT_MAIN)]
    )

    style.configure(
        "Treeview",
        background=WHITE,
        fieldbackground=WHITE,
        foreground=TEXT_MAIN,
        rowheight=30,
        bordercolor=BORDER,
        font=("Segoe UI", 10)
    )

    style.configure(
        "Treeview.Heading",
        background=TREE_HEADING,
        foreground=PINK_TITLE,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        padding=8
    )

    style.map(
        "Treeview",
        background=[("selected", "#F4DCE7")],
        foreground=[("selected", TEXT_MAIN)]
    )

    style.map(
        "Treeview.Heading",
        background=[("active", "#AFE7E7")]
    )


#стили кончились

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Виртуальный деканат")
        self.root.geometry("460x500")
        self.root.resizable(False, False)
        setup_styles(self.root)
        self.build_ui()

    def build_ui(self):
        outer = ttk.Frame(self.root, padding=12)
        outer.pack(fill="both", expand=True)

        card = ttk.Frame(outer, style="Card.TFrame", padding=14)
        card.pack(fill="both", expand=True, padx=6, pady=6)

        self.logo_img = tk.PhotoImage(file="logo.png")
        self.logo_img_small = self.logo_img.subsample(7, 7)
        tk.Label(card, image=self.logo_img_small, bg=BG_PANEL, bd=0).pack(pady=(2, 6))

        ttk.Label(card, text="Виртуальный деканат", style="Title.TLabel").pack(pady=(2, 6))
        ttk.Label(card, text="Авторизация пользователя", style="Subtitle.TLabel").pack(pady=(0, 14))

        ttk.Label(card, text="Логин").pack(anchor="w")
        self.username_entry = ttk.Entry(card)
        self.username_entry.pack(fill="x", pady=(6, 10), ipady=3)

        ttk.Label(card, text="Пароль").pack(anchor="w")
        self.password_entry = ttk.Entry(card, show="*")
        self.password_entry.pack(fill="x", pady=(6, 14), ipady=3)

        ttk.Button(card, text="Войти", command=self.login).pack(fill="x", pady=(2, 4))

        self.username_entry.focus()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Внимание", "Введите логин и пароль")
            return

        try:
            user = authenticate(username, password)
        except Exception as e:
            messagebox.showerror("Ошибка БД", str(e))
            return

        if not user:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
            return

        self.root.destroy()
        new_root = tk.Tk()
        MainWindow(new_root, user)
        new_root.mainloop()



class MainWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Виртуальный деканат")
        self.root.geometry("1200x720")
        self.root.minsize(1000, 620)
        setup_styles(self.root)
        self.build_ui()

    def build_ui(self):
        main = ttk.Frame(self.root, padding=16)
        main.pack(fill="both", expand=True)

        header = ttk.Frame(main, style="Card.TFrame", padding=16)
        header.pack(fill="x", pady=(0, 14))

        ttk.Label(
            header,
            text="Виртуальный деканат",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            header,
            text=(
                f"Пользователь: {self.user['full_name']}   |   "
                f"Логин: {self.user['username']}   |   "
                f"Роль: {self.user['role']}"
            ),
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(6, 0))

        body = ttk.Frame(main)
        body.pack(fill="both", expand=True)

        self.menu_frame = ttk.Frame(body, style="Card.TFrame", padding=14)
        self.menu_frame.pack(side="left", fill="y", padx=(0, 12))

        self.content_frame = ttk.Frame(body, style="Card.TFrame", padding=16)
        self.content_frame.pack(side="left", fill="both", expand=True)

        role = self.user["role"]

        if role == "admin":
            ttk.Button(self.menu_frame, text="Пользователи", style="Menu.TButton", command=self.show_users).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Студенты", style="Menu.TButton", command=self.show_students).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Преподаватели", style="Menu.TButton", command=self.show_teachers).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Абитуриенты", style="Menu.TButton", command=self.show_applicants).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Группы", style="Menu.TButton", command=self.show_groups).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Дисциплины", style="Menu.TButton", command=self.show_disciplines).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Пары", style="Menu.TButton", command=self.show_classes).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Оценки", style="Menu.TButton", command=self.show_grades).pack(fill="x", pady=5)

        elif role == "dean":
            ttk.Button(self.menu_frame, text="Студенты", style="Menu.TButton", command=self.show_students).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Преподаватели", style="Menu.TButton", command=self.show_teachers).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Абитуриенты", style="Menu.TButton", command=self.show_applicants).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Направления", style="Menu.TButton", command=self.show_directions).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Группы", style="Menu.TButton", command=self.show_groups).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Оценки", style="Menu.TButton", command=self.show_grades).pack(fill="x", pady=5)

        elif role == "teacher":
            ttk.Button(self.menu_frame, text="Мои пары", style="Menu.TButton", command=self.show_teacher_classes).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Оценки", style="Menu.TButton", command=self.show_grades).pack(fill="x", pady=5)

        elif role == "student":
            ttk.Button(self.menu_frame, text="Мой профиль", style="Menu.TButton", command=self.show_student_profile).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Мои оценки", style="Menu.TButton", command=self.show_student_grades).pack(fill="x", pady=5)

        elif role == "applicant":
            ttk.Button(self.menu_frame, text="Мой профиль", style="Menu.TButton", command=self.show_applicant_profile).pack(fill="x", pady=5)
            ttk.Button(self.menu_frame, text="Мои направления", style="Menu.TButton", command=self.show_applicant_directions).pack(fill="x", pady=5)

        ttk.Separator(self.menu_frame, orient="horizontal").pack(fill="x", pady=14)
        ttk.Button(self.menu_frame, text="Выход", style="Danger.TButton", command=self.root.destroy).pack(fill="x", pady=(4, 10))

        brand = ttk.Frame(self.menu_frame)
        brand.pack(side="bottom", fill="x", pady=(10, 0))
        ttk.Separator(brand, orient="horizontal").pack(fill="x", pady=(0, 10))

        brand_row = ttk.Frame(brand)
        brand_row.pack(anchor="center")

        ttk.Label(brand_row, text="◈", style="BrandIcon.TLabel").pack(side="left", padx=(0, 6))
        ttk.Label(brand_row, text="Станкин", style="BrandText.TLabel").pack(side="left")

        self.show_welcome()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def make_tree(self, columns, headers):
        wrapper = ttk.Frame(self.content_frame)
        wrapper.pack(fill="both", expand=True, pady=(8, 0))

        tree = ttk.Treeview(wrapper, columns=columns, show="headings")
        vsb = ttk.Scrollbar(wrapper, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(wrapper, orient="horizontal", command=tree.xview)

        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        for col, header in zip(columns, headers):
            tree.heading(col, text=header)
            tree.column(col, width=150, anchor="center")

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        wrapper.rowconfigure(0, weight=1)
        wrapper.columnconfigure(0, weight=1)

        return tree

    def show_welcome(self):
        self.clear_content()
        ttk.Label(
            self.content_frame,
            text="Добро пожаловать в виртуальный деканат",
            style="Title.TLabel"
        ).pack(pady=(30, 10))

        ttk.Label(
            self.content_frame,
            text="Выберите нужный раздел в левом меню",
            style="Subtitle.TLabel"
        ).pack()

    def show_users(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Пользователи", style="Section.TLabel").pack(anchor="w", pady=(0, 10))

        rows = fetch_users()
        tree = self.make_tree(("id", "username", "full_name", "role"), ("ID", "Username", "Full name", "Role"))
        for row in rows:
            tree.insert("", "end", values=(row["id"], row["username"], row["full_name"], row["role"]))

    def show_students(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Студенты", style="Section.TLabel").pack(anchor="w", pady=(0, 10))

        if self.user["role"] == "admin":
            ttk.Button(self.content_frame, text="Добавить студента", command=self.open_add_student_window).pack(anchor="w", pady=(0, 10))

        rows = fetch_students()
        tree = self.make_tree(
            ("id", "card", "fio", "status", "enrollment", "group"),
            ("ID", "Card", "FIO", "Status", "Enrollment", "Group")
        )
        for row in rows:
            fio = f"{row['last_name']} {row['first_name']} {row.get('middle_name') or ''}".strip()
            tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["student_card_number"],
                    fio,
                    row["status"],
                    row["enrollment_date"],
                    row["group_name"]
                )
            )

    def show_teachers(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Преподаватели", style="Section.TLabel").pack(anchor="w", pady=(0, 10))

        if self.user["role"] == "admin":
            ttk.Button(self.content_frame, text="Добавить преподавателя", command=self.open_add_teacher_window).pack(anchor="w", pady=(0, 10))

        rows = fetch_teachers()
        tree = self.make_tree(("id", "fio", "department", "email"), ("ID", "FIO", "Department", "Email"))
        for row in rows:
            fio = f"{row['last_name']} {row['first_name']} {row.get('middle_name') or ''}".strip()
            tree.insert("", "end", values=(row["id"], fio, row["department"], row["email"]))

    def show_applicants(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Абитуриенты", style="Section.TLabel").pack(anchor="w", pady=(0, 10))

        if self.user["role"] == "admin":
            ttk.Button(self.content_frame, text="Добавить абитуриента", command=self.open_add_applicant_window).pack(anchor="w", pady=(0, 10))

        rows = fetch_applicants()
        tree = self.make_tree(
            ("id", "fio", "birth_date", "phone", "email", "reg_date", "status"),
            ("ID", "FIO", "Birth date", "Phone", "Email", "Registration", "Status")
        )
        for row in rows:
            fio = f"{row['last_name']} {row['first_name']} {row.get('middle_name') or ''}".strip()
            tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    fio,
                    row["birth_date"],
                    row["phone"],
                    row["email"],
                    row["registration_date"],
                    row["status"]
                )
            )

    def show_groups(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Группы", style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        rows = fetch_groups()
        tree = self.make_tree(("id", "name", "year", "course", "active"), ("ID", "Name", "Year", "Course", "Active"))
        for row in rows:
            tree.insert("", "end", values=(row["id"], row["name"], row["year_of_admission"], row["course"], row["active"]))

    def show_disciplines(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Дисциплины", style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        rows = fetch_disciplines()
        tree = self.make_tree(("id", "name", "credits", "description"), ("ID", "Name", "Credits", "Description"))
        for row in rows:
            tree.insert("", "end", values=(row["id"], row["name"], row["credits"], row["description"]))

    def show_classes(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Пары", style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        rows = fetch_classes()
        tree = self.make_tree(
            ("id", "discipline", "group", "teacher", "date", "start", "end", "type"),
            ("ID", "Discipline", "Group", "Teacher", "Date", "Start", "End", "Type")
        )
        for row in rows:
            tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["discipline"],
                    row["group_name"],
                    row["teacher_name"],
                    row["class_date"],
                    row["time_start"],
                    row["time_end"],
                    row["class_type"]
                )
            )

    def show_teacher_classes(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Мои пары", style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        rows = fetch_classes_for_teacher(self.user["teacher_id"])
        tree = self.make_tree(
            ("id", "discipline", "group", "date", "start", "end", "type"),
            ("ID", "Discipline", "Group", "Date", "Start", "End", "Type")
        )
        for row in rows:
            tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["discipline"],
                    row["group_name"],
                    row["class_date"],
                    row["time_start"],
                    row["time_end"],
                    row["class_type"]
                )
            )

    def show_grades(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Оценки", style="Section.TLabel").pack(anchor="w", pady=(0, 10))

        if self.user["role"] in ("teacher", "admin"):
            ttk.Button(self.content_frame, text="Добавить оценку", command=self.open_add_grade_window).pack(anchor="w", pady=(0, 10))

        rows = fetch_grades()
        tree = self.make_tree(
            ("id", "student", "discipline", "teacher", "grade", "date", "comment"),
            ("ID", "Student", "Discipline", "Teacher", "Grade", "Date", "Comment")
        )
        for row in rows:
            tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["student_name"],
                    row["discipline"],
                    row["teacher_name"],
                    row["grade"],
                    row["grade_date"],
                    row["comment"]
                )
            )

    def show_student_profile(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Мой профиль", style="Section.TLabel").pack(anchor="w", pady=(0, 10))

        row = fetch_student_profile(self.user["student_id"])
        if not row:
            ttk.Label(self.content_frame, text="Профиль студента не найден", style="Subtitle.TLabel").pack(anchor="w")
            return

        fio = f"{row['last_name']} {row['first_name']} {row.get('middle_name') or ''}".strip()
        text = (
            f"ID: {row['id']}\n\n"
            f"FIO: {fio}\n\n"
            f"Card: {row['student_card_number']}\n\n"
            f"Status: {row['status']}\n\n"
            f"Enrollment date: {row['enrollment_date']}\n\n"
            f"Group: {row['group_name']}"
        )

        card = ttk.Frame(self.content_frame, style="Card.TFrame", padding=20)
        card.pack(fill="x", pady=(8, 0))
        ttk.Label(card, text=text, style="Info.TLabel", justify="left").pack(anchor="w")

    def show_student_grades(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Мои оценки", style="Section.TLabel").pack(anchor="w", pady=(0, 10))

        rows = fetch_grades_for_student(self.user["student_id"])
        tree = self.make_tree(("discipline", "grade", "date", "comment"), ("Discipline", "Grade", "Date", "Comment"))
        for row in rows:
            tree.insert("", "end", values=(row["discipline"], row["grade"], row["grade_date"], row["comment"]))

    def show_applicant_profile(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Мой профиль абитуриента", style="Section.TLabel").pack(anchor="w", pady=(0, 10))

        row = fetch_applicant_profile(self.user["applicant_id"])
        if not row:
            ttk.Label(self.content_frame, text="Профиль абитуриента не найден", style="Subtitle.TLabel").pack(anchor="w")
            return

        fio = f"{row['last_name']} {row['first_name']} {row.get('middle_name') or ''}".strip()
        text = (
            f"ID: {row['id']}\n\n"
            f"FIO: {fio}\n\n"
            f"Birth date: {row['birth_date']}\n\n"
            f"Phone: {row['phone']}\n\n"
            f"Email: {row['email']}\n\n"
            f"Registration date: {row['registration_date']}\n\n"
            f"Status: {row['status']}"
        )

        card = ttk.Frame(self.content_frame, style="Card.TFrame", padding=20)
        card.pack(fill="x", pady=(8, 0))
        ttk.Label(card, text=text, style="Info.TLabel", justify="left").pack(anchor="w")

    def show_applicant_directions(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Мои направления", style="Section.TLabel").pack(anchor="w", pady=(0, 10))

        rows = fetch_directions_for_applicant(self.user["applicant_id"])
        tree = self.make_tree(
            ("code", "name", "level", "form", "status", "date"),
            ("Code", "Direction", "Level", "Study form", "Application status", "Application date")
        )
        for row in rows:
            tree.insert(
                "",
                "end",
                values=(
                    row["code"],
                    row["name"],
                    row["education_level"],
                    row["study_form"],
                    row["application_status"],
                    row["application_date"]
                )
            )

    def show_directions(self):
        self.clear_content()
        ttk.Label(self.content_frame, text="Направления", style="Section.TLabel").pack(anchor="w", pady=(0, 10))

        rows = fetch_directions()
        tree = self.make_tree(
            ("id", "code", "name", "level", "form", "active"),
            ("ID", "Code", "Name", "Level", "Study form", "Active")
        )
        for row in rows:
            tree.insert(
                "",
                "end",
                values=(
                    row["id"],
                    row["code"],
                    row["name"],
                    row["education_level"],
                    row["study_form"],
                    row["active"]
                )
            )

    def open_add_grade_window(self):
        window = tk.Toplevel(self.root)
        window.title("Add Grade")
        window.geometry("540x520")
        window.minsize(540, 520)
        window.resizable(True, True)
        setup_styles(window)

        container = ttk.Frame(window, style="Card.TFrame", padding=18)
        container.pack(fill="both", expand=True, padx=12, pady=12)

        form_frame = ttk.Frame(container)
        form_frame.pack(fill="both", expand=True)

        students = fetch_student_choices()
        disciplines = fetch_discipline_choices()
        teachers = fetch_teacher_choices()

        ttk.Label(form_frame, text="Студент").pack(anchor="w")
        student_cb = ttk.Combobox(form_frame, state="readonly", values=[f"{x['id']} - {x['full_name']}" for x in students])
        student_cb.pack(fill="x", pady=(5, 12))

        ttk.Label(form_frame, text="Дисциплина").pack(anchor="w")
        discipline_cb = ttk.Combobox(form_frame, state="readonly", values=[f"{x['id']} - {x['name']}" for x in disciplines])
        discipline_cb.pack(fill="x", pady=(5, 12))

        ttk.Label(form_frame, text="Преподаватель").pack(anchor="w")
        teacher_cb = ttk.Combobox(form_frame, state="readonly", values=[f"{x['id']} - {x['full_name']}" for x in teachers])
        teacher_cb.pack(fill="x", pady=(5, 12))

        if self.user["role"] == "teacher" and self.user["teacher_id"]:
            for i, value in enumerate(teacher_cb["values"]):
                if value.startswith(f"{self.user['teacher_id']} - "):
                    teacher_cb.current(i)
                    teacher_cb.configure(state="disabled")
                    break

        ttk.Label(form_frame, text="Оценка").pack(anchor="w")
        grade_entry = ttk.Entry(form_frame)
        grade_entry.pack(fill="x", pady=(5, 12), ipady=3)

        ttk.Label(form_frame, text="Комментарий").pack(anchor="w")
        comment_entry = ttk.Entry(form_frame)
        comment_entry.pack(fill="x", pady=(5, 12), ipady=3)

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

        ttk.Button(container, text="Сохранить", command=save).pack(fill="x", side="bottom", pady=(12, 0))

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

        base_height = 220
        per_field_height = 68
        window_height = base_height + len(fields) * per_field_height

        window.geometry(f"540x{window_height}")
        window.minsize(540, window_height)
        window.resizable(True, True)
        setup_styles(window)

        container = ttk.Frame(window, style="Card.TFrame", padding=18)
        container.pack(fill="both", expand=True, padx=12, pady=12)

        ttk.Label(container, text=title, style="Section.TLabel").pack(anchor="w", pady=(0, 12))

        form_frame = ttk.Frame(container)
        form_frame.pack(fill="both", expand=True)

        entries = []
        for field in fields:
            ttk.Label(form_frame, text=field).pack(anchor="w")
            entry = ttk.Entry(form_frame)
            entry.pack(fill="x", pady=(5, 12), ipady=3)
            entries.append(entry)

        def save():
            try:
                values = [e.get().strip() or None for e in entries]
                save_callback(values)
                messagebox.showinfo("Успешно", f"{title} сохранен")
                window.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

        ttk.Button(container, text="Сохранить", command=save).pack(fill="x", side="bottom", pady=(12, 0))