import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from skill_extractor import load_skill_dictionary, extract_skills
from text_cleaner import clean_text
from job_matcher import load_roles, analyze_roles
from roadmap_generator import generate_roadmap

def test_cleaner_preserves_technical_terms():
    text = clean_text("Experienced in C++, C# and .NET")
    assert "c++" in text
    assert "c#" in text
    assert ".net" in text

def test_skill_aliases_and_detection():
    df = load_skill_dictionary("data/skill_dictionary.csv")
    found = extract_skills("I used python, sklearn, sql and power bi.", df)
    assert "Python" in found
    assert "scikit-learn" in found
    assert "SQL" in found
    assert "Power BI" in found

def test_at_least_five_roles_and_sorted_scores():
    roles = load_roles("data/job_roles.csv")
    result = analyze_roles("python sql pandas excel power bi", ["Python", "SQL", "Pandas", "Excel", "Power BI"], roles)
    assert len(result) >= 5
    assert result["match_score"].is_monotonic_decreasing

def test_roadmap_returns_missing_skill_actions():
    plan = generate_roadmap(["Docker"])
    assert plan and plan[0]["Skill to learn"] == "Docker"
    assert plan[0]["Suggested activity"]
