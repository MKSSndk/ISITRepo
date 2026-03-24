from db import get_connection

def fetch_students():
    query = """
        SELECT
            s.id,
            s.student_card_number,
            s.last_name,
            s.first_name,
            s.middle_name,
            s.status,
            s.enrollment_date,
            g.name AS group_name
        FROM students s
        LEFT JOIN student_groups sg
            ON sg.student_id = s.id AND sg.end_date IS NULL
        LEFT JOIN groups_tbl g
            ON g.id = sg.group_id
        ORDER BY s.id
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def fetch_teachers():
    query = """
        SELECT id, last_name, first_name, middle_name, department, email
        FROM teachers
        ORDER BY id
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def fetch_groups():
    query = """
        SELECT id, name, year_of_admission, course, active
        FROM groups_tbl
        ORDER BY id
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def fetch_disciplines():
    query = """
        SELECT id, name, credits, description
        FROM disciplines
        ORDER BY id
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def fetch_classes():
    query = """
        SELECT
            c.id,
            d.name AS discipline,
            g.name AS group_name,
            CONCAT(t.last_name, ' ', t.first_name, ' ', COALESCE(t.middle_name, '')) AS teacher_name,
            c.class_date,
            c.time_start,
            c.time_end,
            c.class_type
        FROM classes c
        JOIN disciplines d ON d.id = c.discipline_id
        JOIN groups_tbl g ON g.id = c.group_id
        JOIN teachers t ON t.id = c.teacher_id
        ORDER BY c.class_date, c.time_start
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def fetch_classes_for_teacher(teacher_id: int):
    query = """
        SELECT
            c.id,
            d.name AS discipline,
            g.name AS group_name,
            c.class_date,
            c.time_start,
            c.time_end,
            c.class_type
        FROM classes c
        JOIN disciplines d ON d.id = c.discipline_id
        JOIN groups_tbl g ON g.id = c.group_id
        WHERE c.teacher_id = %s
        ORDER BY c.class_date, c.time_start
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (teacher_id,))
            return cur.fetchall()

def fetch_grades():
    query = """
        SELECT
            gr.id,
            CONCAT(s.last_name, ' ', s.first_name, ' ', COALESCE(s.middle_name, '')) AS student_name,
            d.name AS discipline,
            CONCAT(t.last_name, ' ', t.first_name, ' ', COALESCE(t.middle_name, '')) AS teacher_name,
            gr.grade,
            gr.grade_date,
            gr.comment
        FROM grades gr
        JOIN students s ON s.id = gr.student_id
        JOIN disciplines d ON d.id = gr.discipline_id
        JOIN teachers t ON t.id = gr.teacher_id
        ORDER BY gr.grade_date DESC, gr.id DESC
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def fetch_grades_for_student(student_id: int):
    query = """
        SELECT
            d.name AS discipline,
            gr.grade,
            gr.grade_date,
            gr.comment
        FROM grades gr
        JOIN disciplines d ON d.id = gr.discipline_id
        WHERE gr.student_id = %s
        ORDER BY gr.grade_date DESC, gr.id DESC
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (student_id,))
            return cur.fetchall()

def fetch_student_profile(student_id: int):
    query = """
        SELECT
            s.id,
            s.student_card_number,
            s.last_name,
            s.first_name,
            s.middle_name,
            s.status,
            s.enrollment_date,
            g.name AS group_name
        FROM students s
        LEFT JOIN student_groups sg
            ON sg.student_id = s.id AND sg.end_date IS NULL
        LEFT JOIN groups_tbl g
            ON g.id = sg.group_id
        WHERE s.id = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (student_id,))
            return cur.fetchone()

def fetch_applicants():
    query = """
        SELECT
            id,
            last_name,
            first_name,
            middle_name,
            birth_date,
            phone,
            email,
            registration_date,
            status
        FROM applicants
        ORDER BY id
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def fetch_applicant_profile(applicant_id: int):
    query = """
        SELECT
            id,
            last_name,
            first_name,
            middle_name,
            birth_date,
            phone,
            email,
            registration_date,
            status
        FROM applicants
        WHERE id = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (applicant_id,))
            return cur.fetchone()

def fetch_directions():
    query = """
        SELECT id, code, name, education_level, study_form, active
        FROM directions
        ORDER BY code
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def fetch_directions_for_applicant(applicant_id: int):
    query = """
        SELECT
            d.code,
            d.name,
            d.education_level,
            d.study_form,
            aa.application_status,
            aa.application_date
        FROM applicant_applications aa
        JOIN directions d ON d.id = aa.direction_id
        WHERE aa.applicant_id = %s
        ORDER BY aa.id
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (applicant_id,))
            return cur.fetchall()

def add_grade(student_id: int, discipline_id: int, teacher_id: int, grade: float, comment: str):
    query = """
        INSERT INTO grades (student_id, discipline_id, teacher_id, grade, grade_date, comment)
        VALUES (%s, %s, %s, %s, CURRENT_DATE, %s)
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (student_id, discipline_id, teacher_id, grade, comment))
        conn.commit()

def fetch_student_choices():
    query = """
        SELECT id, CONCAT(last_name, ' ', first_name, ' ', COALESCE(middle_name, '')) AS full_name
        FROM students
        ORDER BY last_name, first_name
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def fetch_teacher_choices():
    query = """
        SELECT id, CONCAT(last_name, ' ', first_name, ' ', COALESCE(middle_name, '')) AS full_name
        FROM teachers
        ORDER BY last_name, first_name
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def fetch_discipline_choices():
    query = """
        SELECT id, name
        FROM disciplines
        ORDER BY name
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def add_student(card_number: str, last_name: str, first_name: str, middle_name: str, status: str, enrollment_date):
    query = """
        INSERT INTO students (student_card_number, last_name, first_name, middle_name, status, enrollment_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (card_number, last_name, first_name, middle_name, status, enrollment_date))
        conn.commit()

def add_teacher(last_name: str, first_name: str, middle_name: str, department: str, email: str):
    query = """
        INSERT INTO teachers (last_name, first_name, middle_name, department, email)
        VALUES (%s, %s, %s, %s, %s)
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (last_name, first_name, middle_name, department, email))
        conn.commit()

def add_applicant(last_name: str, first_name: str, middle_name: str, birth_date, phone: str, email: str, registration_date, status: str):
    query = """
        INSERT INTO applicants (last_name, first_name, middle_name, birth_date, phone, email, registration_date, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (last_name, first_name, middle_name, birth_date, phone, email, registration_date, status))
        conn.commit()

def fetch_users():
    query = """
        SELECT u.id, u.username, u.full_name, r.name AS role
        FROM users u
        JOIN roles r ON r.id = u.role_id
        ORDER BY u.id
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()