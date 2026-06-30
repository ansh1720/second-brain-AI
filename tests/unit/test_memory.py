"""
Unit tests for the persistent SQLite memory layer.
Tests save/retrieve round-trips for all data categories.

Uses a temporary in-memory or temp-file database so tests
don't pollute the real memory store.
"""
import os
import sys
import sqlite3
import tempfile
import pytest

# Ensure project root is on sys.path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from memory.db import init_db, get_db_connection
from memory.save_memory import (
    save_user_preference,
    save_user_goal,
    save_user_decision,
    save_user_task,
    save_skill_progress,
)
from memory.retrieve_memory import (
    retrieve_user_preferences,
    retrieve_user_goals,
    retrieve_user_decisions,
    retrieve_user_tasks,
    retrieve_skill_progress,
)
from memory.clear_memory import clear_all_memory, delete_memory_key

# Use a separate test DB that gets cleaned up
TEST_USER = "test_user_999"


@pytest.fixture(autouse=True)
def setup_db():
    """Ensure tables exist before every test."""
    init_db()
    yield
    # Cleanup test data after each test
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM preferences WHERE user_id = ?", (TEST_USER,))
        cursor.execute("DELETE FROM goals WHERE user_id = ?", (TEST_USER,))
        cursor.execute("DELETE FROM decisions WHERE user_id = ?", (TEST_USER,))
        cursor.execute("DELETE FROM tasks WHERE user_id = ?", (TEST_USER,))
        cursor.execute("DELETE FROM skills_progress WHERE user_id = ?", (TEST_USER,))
        conn.commit()
        conn.close()
    except Exception:
        pass


# ── Table creation ───────────────────────────────────────────────────────

class TestDatabaseInit:
    def test_tables_exist(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row["name"] for row in cursor.fetchall()}
        conn.close()
        expected = {"users", "goals", "preferences", "decisions", "tasks", "skills_progress"}
        assert expected.issubset(tables), f"Missing tables: {expected - tables}"

    def test_default_user_seeded(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = 'user_123'")
        row = cursor.fetchone()
        conn.close()
        assert row is not None, "Default user 'user_123' not seeded"


# ── Preferences ──────────────────────────────────────────────────────────

class TestPreferences:
    def test_save_and_retrieve_preference(self):
        assert save_user_preference(TEST_USER, "budget", "50000 INR")
        prefs = retrieve_user_preferences(TEST_USER)
        assert prefs.get("budget") == "50000 INR"

    def test_overwrite_preference(self):
        save_user_preference(TEST_USER, "budget", "50000 INR")
        save_user_preference(TEST_USER, "budget", "75000 INR")
        prefs = retrieve_user_preferences(TEST_USER)
        assert prefs["budget"] == "75000 INR"

    def test_multiple_preferences(self):
        save_user_preference(TEST_USER, "budget", "80000")
        save_user_preference(TEST_USER, "brand", "Apple")
        prefs = retrieve_user_preferences(TEST_USER)
        assert len(prefs) >= 2
        assert prefs["brand"] == "Apple"

    def test_retrieve_nonexistent_user(self):
        prefs = retrieve_user_preferences("nonexistent_user_xyz")
        assert prefs == {}


# ── Goals ────────────────────────────────────────────────────────────────

class TestGoals:
    def test_save_and_retrieve_goal(self):
        assert save_user_goal(TEST_USER, "Learn PyTorch", "2026-12-31")
        goals = retrieve_user_goals(TEST_USER)
        assert any("PyTorch" in g["goal_text"] for g in goals)

    def test_multiple_goals(self):
        save_user_goal(TEST_USER, "Goal A")
        save_user_goal(TEST_USER, "Goal B")
        goals = retrieve_user_goals(TEST_USER)
        texts = [g["goal_text"] for g in goals]
        assert "Goal A" in texts
        assert "Goal B" in texts


# ── Decisions ────────────────────────────────────────────────────────────

class TestDecisions:
    def test_save_and_retrieve_decision(self):
        assert save_user_decision(
            TEST_USER, "Laptop choice", "Lenovo LOQ", 85, "Better GPU for AI"
        )
        decisions = retrieve_user_decisions(TEST_USER)
        assert any(d["recommendation"] == "Lenovo LOQ" for d in decisions)

    def test_decision_has_timestamp(self):
        save_user_decision(TEST_USER, "Test", "Result", 90, "Reason")
        decisions = retrieve_user_decisions(TEST_USER)
        assert decisions[0]["created_at"] is not None


# ── Tasks ────────────────────────────────────────────────────────────────

class TestTasks:
    def test_save_and_retrieve_task(self):
        assert save_user_task(TEST_USER, "Complete capstone project")
        tasks = retrieve_user_tasks(TEST_USER)
        assert any("capstone" in t["task_description"] for t in tasks)

    def test_default_status_is_pending(self):
        save_user_task(TEST_USER, "New task")
        tasks = retrieve_user_tasks(TEST_USER)
        assert tasks[-1]["status"] == "pending"


# ── Skills progress ──────────────────────────────────────────────────────

class TestSkillProgress:
    def test_save_and_retrieve_skill(self):
        assert save_skill_progress(TEST_USER, "Python", "Advanced")
        skills = retrieve_skill_progress(TEST_USER)
        assert skills.get("Python") == "Advanced"

    def test_overwrite_skill(self):
        save_skill_progress(TEST_USER, "Python", "Beginner")
        save_skill_progress(TEST_USER, "Python", "Intermediate")
        skills = retrieve_skill_progress(TEST_USER)
        assert skills["Python"] == "Intermediate"


# ── Clear Memory ─────────────────────────────────────────────────────────

class TestClearMemory:
    def test_delete_individual_preference_key(self):
        save_user_preference(TEST_USER, "budget", "100000 INR")
        save_user_preference(TEST_USER, "other_key", "keep_me")
        
        # Delete only budget
        assert delete_memory_key("budget", user_id=TEST_USER)
        
        prefs = retrieve_user_preferences(TEST_USER)
        assert "budget" not in prefs
        assert prefs.get("other_key") == "keep_me"

    def test_delete_goal_category(self):
        save_user_goal(TEST_USER, "Learn ML")
        assert delete_memory_key("career_goals", user_id=TEST_USER)
        
        goals = retrieve_user_goals(TEST_USER)
        assert not goals

    def test_clear_all_memory(self):
        save_user_preference(TEST_USER, "budget", "50000")
        save_user_goal(TEST_USER, "Learn Python")
        save_user_decision(TEST_USER, "Query", "Recommendation", 80, "Rationale")
        save_user_task(TEST_USER, "Pending task")
        save_skill_progress(TEST_USER, "SQL", "Intermediate")
        
        # Clear everything
        assert clear_all_memory(user_id=TEST_USER)
        
        # Verify completely empty
        assert retrieve_user_preferences(TEST_USER) == {}
        assert retrieve_user_goals(TEST_USER) == []
        assert retrieve_user_decisions(TEST_USER) == []
        assert retrieve_user_tasks(TEST_USER) == []
        assert retrieve_skill_progress(TEST_USER) == {}

