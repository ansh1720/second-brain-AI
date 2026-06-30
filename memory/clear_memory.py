"""
clear_memory.py — Wipe user memory from the database.
Provides full clear and per-key delete operations.
"""
from memory.db import get_db_connection

USER_ID = "user_123"


def clear_all_memory(user_id: str = USER_ID) -> bool:
    """Delete all stored preferences, goals, decisions, tasks and skill progress for the user."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM preferences WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM goals WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM decisions WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM tasks WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM skills_progress WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def delete_memory_key(key: str, user_id: str = USER_ID) -> bool:
    """Delete a single preference key or clear specific categories from memory."""
    key_lower = key.lower().strip()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if "goal" in key_lower:
            cursor.execute("DELETE FROM goals WHERE user_id = ?", (user_id,))
        elif "decision" in key_lower:
            cursor.execute("DELETE FROM decisions WHERE user_id = ?", (user_id,))
        elif "task" in key_lower:
            cursor.execute("DELETE FROM tasks WHERE user_id = ?", (user_id,))
        elif "skill" in key_lower:
            cursor.execute("DELETE FROM skills_progress WHERE user_id = ?", (user_id,))
        else:
            cursor.execute(
                "DELETE FROM preferences WHERE user_id = ? AND pref_key = ?",
                (user_id, key.strip())
            )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False
