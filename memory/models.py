from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: str
    name: str

@dataclass
class Goal:
    user_id: str
    goal_text: str
    target_date: Optional[str] = None
    id: Optional[int] = None

@dataclass
class Preference:
    user_id: str
    pref_key: str
    pref_value: str

@dataclass
class Decision:
    user_id: str
    query: str
    recommendation: str
    confidence: int
    rationale: str
    created_at: Optional[str] = None
    id: Optional[int] = None

@dataclass
class Task:
    user_id: str
    task_description: str
    status: str = "pending"
    id: Optional[int] = None

@dataclass
class SkillProgress:
    user_id: str
    skill_name: str
    progress_level: str
