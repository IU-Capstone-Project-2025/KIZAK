from typing import List, Dict, Any
from sklearn.metrics import ndcg_score
import numpy as np


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

    def rank_courses(self, courses: List[Dict], # from cosine similarity serach
                     skill_gap: List[str], #from skillgap
                     target_role: str, # from user onboarding info
                     weights: Dict[str, float] = None) -> List[Dict]: # alpha beta for ranking
        if weights is None:
            weights = {
                "coverage": 0.4,
                "priority": 0.4,
                "rating": 0.2,
                # "free": 0.1
            }
        # get priorities only for needed role
        priorities = self.priorities_by_role.get(target_role, {})
        ranked = []

        for course in courses:
            course_skills = set(course.get("skills", []))
            # todo: check how to get this from skill_gap_anal
            covered_skills = course_skills.intersection(skill_gap)

            # how many skills are covered by this course, the more the >>
            coverage_score = len(covered_skills) / len(skill_gap) if skill_gap else 0

            #how large is priority of skills for that course
            priority_score_sum = sum(priorities.get(skill, 0.0) for skill in covered_skills)
            mean_priority_score = priority_score_sum / len(covered_skills) if covered_skills else 0

            rating = course.get("rating", 0) or 0 #course stars
            rating_score = rating / self.rating_max

            # bcs everybody love halyava :)
            price_score = 1 if course.get("price", 0) == 0 else 0

            score = (
                    weights["coverage"] * coverage_score +
                    weights["priority"] * mean_priority_score +
                    weights["rating"] * rating_score
                    # +
                    # weights["free"] * price_score
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
