import hashlib
from db import get_connection

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def authenticate(username: str, password: str):
    password_hash = hash_password(password)

    query = """
        SELECT
            u.id,
            u.username,
            u.full_name,
            u.student_id,
            u.teacher_id,
            u.applicant_id,
            r.name AS role
        FROM users u
        JOIN roles r ON r.id = u.role_id
        WHERE u.username = %s AND u.password_hash = %s
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (username, password_hash))
            return cur.fetchone()