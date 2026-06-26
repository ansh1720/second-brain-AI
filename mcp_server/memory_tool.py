from memory import (
    init_db,
    save_user_preference,
    save_user_goal,
    save_user_decision,
    save_user_task,
    save_skill_progress,
    retrieve_user_preferences,
    retrieve_user_goals,
    retrieve_user_decisions,
    retrieve_user_tasks,
    retrieve_skill_progress
)
import json

# Initialize database
init_db()

# Default user ID
USER_ID = "user_123"

def save_memory(key: str, val: str) -> str:
    """Saves a key-value memory pair to the persistent SQLite memory store.
    It automatically routes keys to appropriate database tables (preferences, goals, decisions, etc.).
    
    Args:
        key: The key or category (e.g. 'budget', 'career_goals', 'decision:laptop').
        val: The memory content to store.
        
    Returns:
        A confirmation message.
    """
    key_lower = key.lower().strip()
    
    if "goal" in key_lower:
        success = save_user_goal(USER_ID, val)
        table = "goals"
    elif "decision" in key_lower:
        try:
            data = json.loads(val)
            query = data.get("query", "Laptop Comparison")
            recommendation = data.get("recommendation", "Unknown")
            confidence = int(data.get("confidence", 90))
            rationale = data.get("rationale", val)
            success = save_user_decision(USER_ID, query, recommendation, confidence, rationale)
        except Exception:
            success = save_user_decision(USER_ID, "Stored Decision", val, 100, val)
        table = "decisions"
    elif "task" in key_lower:
        success = save_user_task(USER_ID, val)
        table = "tasks"
    elif "skill" in key_lower:
        if ":" in val:
            skill_name, progress = val.split(":", 1)
            success = save_skill_progress(USER_ID, skill_name.strip(), progress.strip())
        else:
            success = save_skill_progress(USER_ID, key, val)
        table = "skills_progress"
    else:
        success = save_user_preference(USER_ID, key.strip(), val.strip())
        table = "preferences"
        
    if success:
        return f"Successfully saved memory key '{key}' to '{table}' table."
    return f"Failed to save memory key '{key}'."

def retrieve_memory(key: str) -> str:
    """Retrieves a memory value from the persistent SQLite memory store.
    
    Args:
        key: The memory key to look up (e.g. 'budget', 'career_goals', 'decisions').
        
    Returns:
        The retrieved value or error message.
    """
    key_lower = key.lower().strip()
    
    if "goal" in key_lower:
        goals = retrieve_user_goals(USER_ID)
        if not goals:
            return "No goals found."
        return "\n".join([f"- Goal: {g['goal_text']} (Target: {g['target_date']})" for g in goals])
        
    elif "decision" in key_lower:
        decisions = retrieve_user_decisions(USER_ID)
        if not decisions:
            return "No past decisions found."
        return "\n".join([f"- Query: '{d['query']}' -> Recommendation: {d['recommendation']} (Conf: {d['confidence']}%)" for d in decisions])
        
    elif "task" in key_lower:
        tasks = retrieve_user_tasks(USER_ID)
        if not tasks:
            return "No tasks found."
        return "\n".join([f"- Task: {t['task_description']} [{t['status']}]" for t in tasks])
        
    elif "skill" in key_lower:
        skills = retrieve_skill_progress(USER_ID)
        if not skills:
            return "No skill progress found."
        return "\n".join([f"- Skill: {name} (Level: {lvl})" for name, lvl in skills.items()])
        
    else:
        prefs = retrieve_user_preferences(USER_ID)
        val = prefs.get(key.strip())
        if val:
            return val
        return f"Key '{key}' not found in preferences. Available keys: {', '.join(prefs.keys())}"
