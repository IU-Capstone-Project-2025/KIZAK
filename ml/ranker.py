import ast
from typing import List, Dict, Any
from sklearn.metrics import ndcg_score
import numpy as np
import re

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

class CourseRanker:
    '''
    priorities_by_role = skill_priorities = {
        "fullstack developer": [
        {
          "skill": "angular",
          "priority": 0.95
        },
        {
          "skill": "aws",
          "priority": 0.9
        },
        {
          "skill": "azure",
          "priority": 0.85
        },
        ...
    rating_max = max course rank(5 stars)
    '''
    def __init__(self, priorities_by_role: Dict[str, Dict[str, int]], rating_max: float = 5.0):
        self.priorities_by_role = priorities_by_role
        self.rating_max = rating_max

    def normalize_skill(self, skill: str) -> str:
        skill = skill.lower()
        skill = re.sub(r"[^a-z0-9\s]", "", skill)
        return skill.strip()

    def get_skill_words(self, skills: list[str]) -> set[str]:
        words = set()
        for skill in skills:
            normalized = self.normalize_skill(skill)
            splitted = normalized.split()
            words.update(splitted)
        return words

    def rank_courses(self, courses: List[Dict], # from cosine similarity serach
                     skill_gap: List[str], #from skillgap
                     target_role: str, # from user onboarding info
                     weights: Dict[str, float] = None) -> List[Dict]: # alpha beta for ranking
        if weights is None:
            weights = {
                "coverage": 0.45,
                "priority": 0.45,
                "rating": 0.1
            }
        # get priorities only for needed role
        priorities = self.priorities_by_role.get(target_role, {})
        ranked = []
        for course in courses:
            raw_course_skills = course.get("skills", [])
            if isinstance(raw_course_skills, str):
                try:
                    import ast
                    raw_course_skills = ast.literal_eval(raw_course_skills)
                except Exception:
                    raw_course_skills = []

            course_skills = self.get_skill_words(raw_course_skills)

            logger.info(
                f"Course ID: {course.get('id')}, "
                f"skills type: {type(course_skills)}, "
                f"value: {course_skills}")

            # normalized_gap = set(self.normalize_skill(s) for s in skill_gap)
            covered_skills = course_skills.intersection(skill_gap)


            # how many skills are covered by this course, the more the >>
            coverage_score = len(covered_skills) / len(skill_gap) if skill_gap else 0

            #how large is priority of skills for that course
            priority_score_sum = sum(priorities.get(skill, 0.0) for skill in covered_skills)
            mean_priority_score = priority_score_sum / len(covered_skills) if covered_skills else 0

            rating = course.get("rating", 0) or 0 #course stars
            rating_score = rating / self.rating_max

            # # bcs everybody love halyava :)
            # price_score = 1 if course.get("price", 0) == 0 else 0

            score = (
                    weights["coverage"] * coverage_score +
                    weights["priority"] * mean_priority_score +
                    weights["rating"] * rating_score
            )

            ranked.append({
                "course": course,
                "ranking_score": round(score, 4),
                "covered_skills": list(covered_skills)
            })
        # dict course - how cool it is
        return sorted(ranked, key=lambda x: x["ranking_score"], reverse=True)

    def evaluate_ranking(self, ranked_courses: List[Dict],
                         skill_gap: List[str],
                         target_role: str,
                         k: int = 10 # top-k
                         ) -> Dict[
        str, float]:
        priorities = self.priorities_by_role.get(target_role, {})

        predicted_relevances = []

        for item in ranked_courses[:k]:
            covered_skills = item["covered_skills"]
            rel = sum(1 / priorities.get(skill, 5) for skill in covered_skills)
            predicted_relevances.append(rel)

        ideal_relevances = sorted(predicted_relevances, reverse=True)

        if not any(predicted_relevances):
            return {"NDCG@k": 0.0}

        ndcg = ndcg_score([ideal_relevances], [predicted_relevances])
        return {"NDCG@k": round(ndcg, 4)}
