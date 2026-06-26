import os
from typing import List
from google.adk.skills import load_skill_from_dir
from google.adk.skills.models import Skill

def get_skills_dir() -> str:
    return os.path.dirname(os.path.abspath(__file__))

def load_skill_by_name(skill_name: str) -> Skill:
    base_dir = get_skills_dir()
    skill_dir = os.path.join(base_dir, skill_name)
    return load_skill_from_dir(skill_dir)

def list_all_skills() -> List[str]:
    base_dir = get_skills_dir()
    skills = []
    if os.path.exists(base_dir):
        for item in os.listdir(base_dir):
            sub = os.path.join(base_dir, item)
            if os.path.isdir(sub) and not item.startswith("__") and not item.startswith("."):
                skills.append(item)
    return skills

def match_and_load_skills(query: str) -> List[Skill]:
    """Matches keywords in the user query to dynamically load specialized skills."""
    query_lower = query.lower()
    matched_skills = []
    
    # Map domains to request keyword patterns
    mappings = {
        "career": ["career", "job", "internship", "engineer", "cv", "resume"],
        "shopping": ["buy", "purchase", "shopping", "laptop", "compare", "price", "macbook", "lenovo"],
        "learning": ["learn", "roadmap", "syllabus", "course", "study", "tutor"],
        "finance": ["budget", "finance", "cost", "roi", "price", "expensive", "cheaper"],
        "planning": ["plan", "schedule", "task", "milestone", "timeline"]
    }
    
    all_available = list_all_skills()
    for skill_name in all_available:
        keywords = mappings.get(skill_name, [skill_name])
        if any(keyword in query_lower for keyword in keywords):
            try:
                skill = load_skill_by_name(skill_name)
                matched_skills.append(skill)
            except Exception as e:
                print(f"Error loading skill {skill_name}: {e}")
                
    return matched_skills
