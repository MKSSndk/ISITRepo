from db import get_connection

def has_permission(role_name: str, object_name: str, action_name: str) -> bool:
    query = """
        SELECT 1
        FROM role_permissions rp
        JOIN roles r ON r.id = rp.role_id
        WHERE r.name = %s
          AND rp.object_name = %s
          AND rp.action_name = %s
        LIMIT 1
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (role_name, object_name, action_name))
            return cur.fetchone() is not None