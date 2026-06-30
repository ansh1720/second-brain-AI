"""
Unit tests for the dynamic skills loader.
Tests skill discovery, keyword matching, and loading.
"""
import os
import sys
import pytest

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from skills.loader import list_all_skills, match_and_load_skills


# ── Skill discovery ─────────────────────────────────────────────────────

class TestSkillDiscovery:
    def test_all_skills_found(self):
        skills = list_all_skills()
        expected = {"career", "shopping", "learning", "finance", "planning"}
        assert set(skills) == expected, f"Expected {expected}, got {set(skills)}"

    def test_returns_list(self):
        skills = list_all_skills()
        assert isinstance(skills, list)

    def test_no_hidden_dirs(self):
        skills = list_all_skills()
        assert all(not s.startswith("__") for s in skills)
        assert all(not s.startswith(".") for s in skills)


# ── Keyword matching ─────────────────────────────────────────────────────

class TestSkillMatching:
    def test_shopping_keyword_buy(self):
        matched = match_and_load_skills("I want to buy a laptop")
        names = [s.name for s in matched]
        assert "shopping" in names

    def test_shopping_keyword_macbook(self):
        matched = match_and_load_skills("Compare MacBook Air vs Lenovo LOQ")
        names = [s.name for s in matched]
        assert "shopping" in names

    def test_career_keyword(self):
        matched = match_and_load_skills("How do I get a job in AI?")
        names = [s.name for s in matched]
        assert "career" in names

    def test_learning_keyword(self):
        matched = match_and_load_skills("I want to learn machine learning")
        names = [s.name for s in matched]
        assert "learning" in names

    def test_finance_keyword(self):
        matched = match_and_load_skills("What is the ROI of this purchase?")
        names = [s.name for s in matched]
        assert "finance" in names

    def test_planning_keyword(self):
        matched = match_and_load_skills("Help me plan my next 3 months")
        names = [s.name for s in matched]
        assert "planning" in names

    def test_no_match_returns_empty(self):
        matched = match_and_load_skills("Tell me a joke")
        assert matched == []

    def test_multiple_skills_can_match(self):
        """A query about buying and budget should match both shopping and finance."""
        matched = match_and_load_skills("What is the best budget laptop to buy?")
        names = [s.name for s in matched]
        assert "shopping" in names
        assert "finance" in names

    def test_case_insensitive(self):
        matched = match_and_load_skills("CAREER in AI Engineering")
        names = [s.name for s in matched]
        assert "career" in names

    def test_loaded_skills_have_name_and_instructions(self):
        matched = match_and_load_skills("I want to buy a laptop")
        for skill in matched:
            assert hasattr(skill, "name")
            assert hasattr(skill, "instructions")
            assert len(skill.instructions) > 0
