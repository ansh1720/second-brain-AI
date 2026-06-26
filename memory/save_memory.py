from memory.db import get_db_connection

def save_user_goal(user_id: str, goal_text: str, target_date: str = None) -> bool:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO goals (user_id, goal_text, target_date) VALUES (?, ?, ?)",
            (user_id, goal_text, target_date)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving goal: {e}")
        return False

def save_user_preference(user_id: str, pref_key: str, pref_value: str) -> bool:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO preferences (user_id, pref_key, pref_value) VALUES (?, ?, ?)",
            (user_id, pref_key, pref_value)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving preference: {e}")
        return False

def save_user_decision(user_id: str, query: str, recommendation: str, confidence: int, rationale: str) -> bool:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO decisions (user_id, query, recommendation, confidence, rationale) VALUES (?, ?, ?, ?, ?)",
            (user_id, query, recommendation, confidence, rationale)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving decision: {e}")
        return False

def save_user_task(user_id: str, task_description: str, status: str = "pending") -> bool:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (user_id, task_description, status) VALUES (?, ?, ?)",
            (user_id, task_description, status)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving task: {e}")
        return False

def save_skill_progress(user_id: str, skill_name: str, progress_level: str) -> bool:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO skills_progress (user_id, skill_name, progress_level) VALUES (?, ?, ?)",
            (user_id, skill_name, progress_level)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving skill progress: {e}")
        return False
