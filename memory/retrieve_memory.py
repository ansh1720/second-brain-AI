from typing import List, Dict, Any
from memory.db import get_db_connection

def retrieve_user_goals(user_id: str) -> List[Dict[str, Any]]:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, goal_text, target_date FROM goals WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error retrieving goals: {e}")
        return []

def retrieve_user_preferences(user_id: str) -> Dict[str, str]:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT pref_key, pref_value FROM preferences WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return {row["pref_key"]: row["pref_value"] for row in rows}
    except Exception as e:
        print(f"Error retrieving preferences: {e}")
        return {}

def retrieve_user_decisions(user_id: str) -> List[Dict[str, Any]]:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, query, recommendation, confidence, rationale, created_at FROM decisions WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error retrieving decisions: {e}")
        return []

def retrieve_user_tasks(user_id: str) -> List[Dict[str, Any]]:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, task_description, status FROM tasks WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error retrieving tasks: {e}")
        return []

def retrieve_skill_progress(user_id: str) -> Dict[str, str]:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT skill_name, progress_level FROM skills_progress WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return {row["skill_name"]: row["progress_level"] for row in rows}
    except Exception as e:
        print(f"Error retrieving skill progress: {e}")
        return {}
