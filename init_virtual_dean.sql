DROP TABLE IF EXISTS grades CASCADE;
DROP TABLE IF EXISTS classes CASCADE;
DROP TABLE IF EXISTS student_groups CASCADE;
DROP TABLE IF EXISTS applicant_applications CASCADE;
DROP TABLE IF EXISTS directions CASCADE;
DROP TABLE IF EXISTS applicants CASCADE;
DROP TABLE IF EXISTS disciplines CASCADE;
DROP TABLE IF EXISTS groups_tbl CASCADE;
DROP TABLE IF EXISTS teachers CASCADE;
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS role_permissions CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS roles CASCADE;

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    student_card_number VARCHAR(32) UNIQUE,
    last_name VARCHAR(64) NOT NULL,
    first_name VARCHAR(64) NOT NULL,
    middle_name VARCHAR(64),
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    enrollment_date DATE
);

CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    last_name VARCHAR(64) NOT NULL,
    first_name VARCHAR(64) NOT NULL,
    middle_name VARCHAR(64),
    department VARCHAR(128),
    email VARCHAR(128)
);

CREATE TABLE applicants (
    id SERIAL PRIMARY KEY,
    last_name VARCHAR(64) NOT NULL,
    first_name VARCHAR(64) NOT NULL,
    middle_name VARCHAR(64),
    birth_date DATE,
    passport_series VARCHAR(16),
    passport_number VARCHAR(16),
    phone VARCHAR(32),
    email VARCHAR(128),
    snils VARCHAR(16),
    registration_date DATE,
    status VARCHAR(32) NOT NULL DEFAULT 'submitted'
);

CREATE TABLE directions (
    id SERIAL PRIMARY KEY,
    code VARCHAR(32) NOT NULL UNIQUE,
    name VARCHAR(128) NOT NULL,
    education_level VARCHAR(32),
    study_form VARCHAR(32),
    active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE applicant_applications (
    id SERIAL PRIMARY KEY,
    applicant_id INT NOT NULL REFERENCES applicants(id) ON DELETE CASCADE,
    direction_id INT NOT NULL REFERENCES directions(id) ON DELETE CASCADE,
    application_status VARCHAR(32) NOT NULL DEFAULT 'submitted',
    application_date DATE NOT NULL DEFAULT CURRENT_DATE,
    UNIQUE(applicant_id, direction_id)
);

CREATE TABLE groups_tbl (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL UNIQUE,
    year_of_admission INT,
    course INT,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE disciplines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL UNIQUE,
    credits INT,
    description TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    role_id INT NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    student_id INT REFERENCES students(id) ON DELETE SET NULL,
    teacher_id INT REFERENCES teachers(id) ON DELETE SET NULL,
    applicant_id INT REFERENCES applicants(id) ON DELETE SET NULL
);

CREATE TABLE role_permissions (
    role_id INT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    object_name VARCHAR(50) NOT NULL,
    action_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (role_id, object_name, action_name)
);

CREATE TABLE student_groups (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    group_id INT NOT NULL REFERENCES groups_tbl(id) ON DELETE CASCADE,
    start_date DATE,
    end_date DATE,
    UNIQUE(student_id, group_id, start_date)
);

CREATE TABLE classes (
    id SERIAL PRIMARY KEY,
    discipline_id INT NOT NULL REFERENCES disciplines(id) ON DELETE RESTRICT,
    group_id INT NOT NULL REFERENCES groups_tbl(id) ON DELETE RESTRICT,
    teacher_id INT NOT NULL REFERENCES teachers(id) ON DELETE RESTRICT,
    class_date DATE NOT NULL,
    time_start TIME NOT NULL,
    time_end TIME NOT NULL,
    class_type VARCHAR(32) NOT NULL,
    CHECK (time_end > time_start)
);

CREATE TABLE grades (
    id SERIAL PRIMARY KEY,
    student_id INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    discipline_id INT NOT NULL REFERENCES disciplines(id) ON DELETE RESTRICT,
    teacher_id INT NOT NULL REFERENCES teachers(id) ON DELETE RESTRICT,
    grade NUMERIC(5,2) NOT NULL,
    grade_date DATE NOT NULL DEFAULT CURRENT_DATE,
    comment TEXT,
    CHECK (grade >= 0 AND grade <= 100)
);

CREATE INDEX idx_users_role_id ON users(role_id);

CREATE INDEX idx_student_groups_student_id ON student_groups(student_id);
CREATE INDEX idx_student_groups_group_id ON student_groups(group_id);

CREATE INDEX idx_classes_discipline_id ON classes(discipline_id);
CREATE INDEX idx_classes_group_id ON classes(group_id);
CREATE INDEX idx_classes_teacher_id ON classes(teacher_id);
CREATE INDEX idx_classes_class_date ON classes(class_date);

CREATE INDEX idx_grades_student_id ON grades(student_id);
CREATE INDEX idx_grades_discipline_id ON grades(discipline_id);
CREATE INDEX idx_grades_teacher_id ON grades(teacher_id);

CREATE UNIQUE INDEX idx_applicants_snils_unique
ON applicants(snils)
WHERE snils IS NOT NULL;

CREATE UNIQUE INDEX idx_applicants_passport_unique
ON applicants(passport_series, passport_number)
WHERE passport_series IS NOT NULL AND passport_number IS NOT NULL;

INSERT INTO roles (name) VALUES
('admin'),
('dean'),
('teacher'),
('student'),
('applicant');

INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'users', 'read' FROM roles WHERE name = 'admin';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'users', 'write' FROM roles WHERE name = 'admin';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'users', 'delete' FROM roles WHERE name = 'admin';

INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'students', 'read' FROM roles WHERE name = 'admin';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'students', 'write' FROM roles WHERE name = 'admin';

INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'teachers', 'read' FROM roles WHERE name = 'admin';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'teachers', 'write' FROM roles WHERE name = 'admin';

INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'applicants', 'read' FROM roles WHERE name = 'admin';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'applicants', 'write' FROM roles WHERE name = 'admin';

INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'groups', 'read' FROM roles WHERE name = 'admin';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'disciplines', 'read' FROM roles WHERE name = 'admin';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'classes', 'read' FROM roles WHERE name = 'admin';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'grades', 'read' FROM roles WHERE name = 'admin';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'grades', 'write' FROM roles WHERE name = 'admin';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'directions', 'read' FROM roles WHERE name = 'admin';

INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'students', 'read' FROM roles WHERE name = 'dean';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'teachers', 'read' FROM roles WHERE name = 'dean';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'groups', 'read' FROM roles WHERE name = 'dean';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'disciplines', 'read' FROM roles WHERE name = 'dean';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'classes', 'read' FROM roles WHERE name = 'dean';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'grades', 'read' FROM roles WHERE name = 'dean';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'applicants', 'read' FROM roles WHERE name = 'dean';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'directions', 'read' FROM roles WHERE name = 'dean';

INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'students', 'read' FROM roles WHERE name = 'teacher';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'groups', 'read' FROM roles WHERE name = 'teacher';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'disciplines', 'read' FROM roles WHERE name = 'teacher';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'classes', 'read' FROM roles WHERE name = 'teacher';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'grades', 'read' FROM roles WHERE name = 'teacher';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'grades', 'write' FROM roles WHERE name = 'teacher';

INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'students', 'read_self' FROM roles WHERE name = 'student';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'groups', 'read' FROM roles WHERE name = 'student';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'classes', 'read' FROM roles WHERE name = 'student';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'grades', 'read_self' FROM roles WHERE name = 'student';

INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'applicants', 'read_self' FROM roles WHERE name = 'applicant';
INSERT INTO role_permissions (role_id, object_name, action_name)
SELECT id, 'directions', 'read_self' FROM roles WHERE name = 'applicant';

INSERT INTO students (student_card_number, last_name, first_name, middle_name, status, enrollment_date) VALUES
('ST-001', 'Petrov', 'Ivan', 'Alekseevich', 'active', '2024-09-01'),
('ST-002', 'Sidorova', 'Anna', 'Igorevna', 'active', '2024-09-01'),
('ST-003', 'Kuznetsov', 'Maksim', 'Olegovich', 'academic_leave', '2023-09-01');

INSERT INTO teachers (last_name, first_name, middle_name, department, email) VALUES
('Ivanov', 'Sergey', 'Petrovich', 'Informatics Department', 'ivanov@university.local'),
('Smirnova', 'Elena', 'Viktorovna', 'Mathematics Department', 'smirnova@university.local');

INSERT INTO applicants (
    last_name, first_name, middle_name, birth_date,
    passport_series, passport_number, phone, email, snils,
    registration_date, status
) VALUES
('Ivanov', 'Pavel', 'Sergeevich', '2007-05-14', '4510', '123456', '+79990000001', 'ivanov.pavel@mail.com', '123-456-789 01', '2026-06-20', 'submitted'),
('Smirnova', 'Alina', 'Olegovna', '2007-09-22', '4511', '654321', '+79990000002', 'smirnova.alina@mail.com', '123-456-789 02', '2026-06-21', 'confirmed'),
('Kozlov', 'Denis', 'Igorevich', '2006-12-03', '4512', '777888', '+79990000003', 'kozlov.denis@mail.com', '123-456-789 03', '2026-06-22', 'enrolled');

INSERT INTO directions (code, name, education_level, study_form, active) VALUES
('09.03.01', 'Informatics and Computer Engineering', 'bachelor', 'full-time', TRUE),
('09.03.02', 'Information Systems and Technologies', 'bachelor', 'full-time', TRUE),
('01.03.02', 'Applied Mathematics and Informatics', 'bachelor', 'full-time', TRUE);

INSERT INTO applicant_applications (applicant_id, direction_id, application_status, application_date) VALUES
(1, 1, 'submitted', '2026-06-20'),
(1, 2, 'confirmed', '2026-06-21'),
(2, 3, 'submitted', '2026-06-21');

INSERT INTO groups_tbl (name, year_of_admission, course, active) VALUES
('PI-101', 2024, 2, TRUE),
('PI-201', 2023, 3, TRUE);

INSERT INTO student_groups (student_id, group_id, start_date, end_date) VALUES
(1, 1, '2024-09-01', NULL),
(2, 1, '2024-09-01', NULL),
(3, 2, '2023-09-01', NULL);

INSERT INTO disciplines (name, credits, description) VALUES
('Databases', 4, 'Database fundamentals'),
('Python Programming', 5, 'Python application development'),
('Mathematical Analysis', 6, 'Basic mathematics course');

INSERT INTO classes (discipline_id, group_id, teacher_id, class_date, time_start, time_end, class_type) VALUES
(1, 1, 1, '2026-03-25', '09:00', '10:30', 'Lecture'),
(2, 1, 1, '2026-03-26', '10:45', '12:15', 'Practice'),
(3, 2, 2, '2026-03-27', '12:30', '14:00', 'Lecture');

INSERT INTO grades (student_id, discipline_id, teacher_id, grade, grade_date, comment) VALUES
(1, 1, 1, 90, '2026-03-10', 'Excellent'),
(1, 2, 1, 85, '2026-03-12', 'Good'),
(2, 1, 1, 78, '2026-03-10', 'Not bad'),
(2, 2, 1, 88, '2026-03-12', 'Confident'),
(3, 3, 2, 67, '2026-03-11', 'Needs improvement');

INSERT INTO users (username, password_hash, full_name, role_id, student_id)
SELECT 'student',
       '703b0a3d6ad75b649a28adde7d83c6251da457549263bc7ff45ec709b0a8448b',
       'Student Petrov',
       id,
       1
FROM roles WHERE name = 'student';

INSERT INTO users (username, password_hash, full_name, role_id, teacher_id)
SELECT 'teacher',
       'cde383eee8ee7a4400adf7a15f716f179a2eb97646b37e089eb8d6d04e663416',
       'Teacher Ivanov',
       id,
       1
FROM roles WHERE name = 'teacher';

INSERT INTO users (username, password_hash, full_name, role_id, applicant_id)
SELECT 'applicant',
       '255f39b6bcf7c09a1cc783c0812c1ea888a257fba5072de7a9f2a76e7e8c5985',
       'Ivan Abiturientov',
       id,
       1
FROM roles WHERE name = 'applicant';

INSERT INTO users (username, password_hash, full_name, role_id)
SELECT 'admin',
       '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',
       'System Administrator',
       id
FROM roles WHERE name = 'admin';

INSERT INTO users (username, password_hash, full_name, role_id)
SELECT 'dean',
       '45ca6bc1a91a4764e6899ebdfd4a15340d18dc00a264ccee75ecfce1d2df5733',
       'Dean',
       id
FROM roles WHERE name = 'dean';