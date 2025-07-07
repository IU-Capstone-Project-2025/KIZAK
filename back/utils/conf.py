import json

with open('ml/job_skill.json', 'r', encoding='utf-8') as f:
    job_skills_raw = json.load(f)

ROLE_TO_SKILLS = dict()
PRIORITIES_BY_ROLE = dict()
USER_SKILLS = set()
for role, skills in job_skills_raw.items():
    ROLE_TO_SKILLS[role] = [item["skill"] for item in skills]
    PRIORITIES_BY_ROLE[role] = {item["skill"]: item["priority"] for item in skills}
    USER_SKILLS.add(ROLE_TO_SKILLS.values())
