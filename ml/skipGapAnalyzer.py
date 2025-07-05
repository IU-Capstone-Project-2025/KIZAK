import json


class SkillGapAnalyzer:
    def __init__(self, role_to_skills: dict[str: list[str]]):
        '''
        Initialize the SkillGapAnalyzer with a mapping of roles
        to required skills.
        '''
        self.__role_map__ = role_to_skills

    def required_skils(self, role: str) -> list[str]:
        '''
        Get the required skills for a given role
        '''
        return self.__role_map__.get(role, [])

    def compute_gap(
            self, user_skills: list[str], role: str
    ) -> dict[str, list[str]]:
        '''
        Compute the gap between the user's skills and the required skills
        for a given role.
        '''
        required = self.required_skils(role)
        return {
            "missing_skills": list(set(required) - set(user_skills)),
            "matched_skills": list(set(user_skills) & set(required)),
            "extra_skills": list(set(user_skills) - set(required)),
        }
        
# testing part

# with open('job_skill.json', 'r', encoding='utf-8') as f:
#     ROLE_TO_SKILLS = json.load(f)
#
# # TODO: add real user skills from backend
# # probably extract from all user info
# USER_SKILLS = ["python", "sql", "aws", "docker", "kubernetes"]
#
# # TODO: add real role from backend
# USER_ROLE = "data_engineer"
#
# analyzer = SkillGapAnalyzer(ROLE_TO_SKILLS)
# result = analyzer.compute_gap(USER_SKILLS, USER_ROLE)
# print(result)


with open('job_skill.json', 'r', encoding='utf-8') as f:
    ROLE_TO_SKILLS = json.load(f)

analyzer = SkillGapAnalyzer(ROLE_TO_SKILLS)
