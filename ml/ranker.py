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

    def __init__(self, priorities_by_role: Dict[str, Dict[str, int]], rating_max: float = 5.0):
        self.priorities_by_role = priorities_by_role
        self.rating_max = rating_max

    def _filter_low_quality_courses(self, courses: List[Dict]) -> List[Dict]:
        # еthrow out courses without any skills or with bad rating
        return [
            c for c in courses
            if c.get("skills") and (c.get("rating", 0) or 0) >= 2.5
        ]

    def rank_courses(self, courses: List[Dict], # from cosine similarity search
                     skill_gap: List[str], #from skillgap
                     target_role: str, # from user onboarding info
                     weights: Dict[str, float] = None, # alpha beta for ranking
                     strategy: str = "v1" # to recalculate if offline metrics are bad
                     ) -> List[Dict]:
        if weights is None:
            if strategy == "v1":
                weights = {"coverage": 0.45, "priority": 0.45, "rating": 0.1}
            elif strategy == "v2":
                weights = {"coverage": 0.7, "priority": 0.2, "rating": 0.1}
                courses = self._filter_low_quality_courses(courses)

        # get priorities from job-skills mapping
        priorities = self.priorities_by_role.get(target_role, {})
        ranked = []
        for course in courses:
            course_skills = course.get("skills", [])

            covered_skills = set(course_skills).intersection(set(skill_gap))

            # how many skills are covered by this course, the more the >>
            coverage_score = len(covered_skills) / len(skill_gap) if skill_gap else 0

            #how large is priority of skills for that course
            priority_score_sum = sum(priorities.get(skill, 0.0) for skill in covered_skills)
            mean_priority_score = priority_score_sum / len(covered_skills) if covered_skills else 0

            # todo: count non starred courses as also good and not just 0
            rating = course.get("rating", 0) or 0 #course stars
            rating_score = rating / self.rating_max

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

    # todo: update, add diversity etc
    def evaluate_ranking(self,
                         ranked_courses: List[Dict], #init ranking
                         skill_gap: List[str],
                         target_role: str,
                         k: int = 10 # top-k
                         ) -> Dict[str, float]:
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

    def rank_with_fallback(self,
                           courses: List[Dict],
                           skill_gap: List[str],
                           target_role: str,
                           max_attempts: int = 3 #attenpt to improve 3 times
                           ) -> List[Dict]:
        """Cyclic ranks with different strategies until offline metrics are better"""

        strategies = ["v1", "v2"]
        for i in range(min(max_attempts, len(strategies))):
            strategy = strategies[i]
            logger.info(f"Ranking attempt {i + 1} with strategy '{strategy}'")
            ranked = self.rank_courses(courses, skill_gap, target_role, strategy=strategy)
            metrics = self.evaluate_ranking(ranked, skill_gap, target_role)
            logger.info(f"Evaluation metrics: {metrics}")

            # threshold
            if metrics.get("NDCG@k", 0) > 0.3:
                return ranked

        # if no improvement - return last variant
        return ranked

    def update_ranking(self,
                       ranked_courses: List[Dict],
                       feedback_type: str,  # - "too_easy"
                                            # - "wrong_skills"
                                            # - "too_hard"
                                            # - "bad_author"
                                            # - "unavailable"
                       feedback_data: None # course id or mb something else
                       ) -> List[Dict]:
        """
        Re-ranking based on user feedback (human metric)
        """
        updated_courses = ranked_courses.copy()

        if feedback_type == "too_easy":
            # todo: update known skills and re-rank with new skill gap
            logger.info(f"Feedback type is 'too_easy'")
        elif feedback_type == "wrong_skills":
            # throw out this course and similar ones
            logger.info('Feedback type is "wrong_skills"')
            course_id = feedback_data.get("course_id")
            updated_courses = [c for c in updated_courses if c["course"].get("id") != course_id]
            # TODO: implement logic of deleting similar courses
        elif feedback_type == "too_hard":
            # make course further in roadmap
            logger.info('Feedback type is "too_hard"')
            course_id = feedback_data.get("course_id")
            for i, c in enumerate(updated_courses):
                if c["course"].get("id") == course_id and i < len(updated_courses) - 1:
                    updated_courses[i], updated_courses[i + 1] = updated_courses[i + 1], updated_courses[i]
                    break
        elif feedback_type == "bad_author":
            # throw out courses with that author
            logger.info('Feedback type is "bad_author"')
            author = feedback_data.get("author")
            updated_courses = [c for c in updated_courses if c["course"].get("author") != author]
        elif feedback_type == "unavailable":
            # TODO: implement alg to delete course from db
            logger.info('Feedback type is "unavailable"')
            course_id = feedback_data.get("course_id")
            updated_courses = [c for c in updated_courses if c["course"].get("id") != course_id]
        else:
            logger.info('Unknown feedback type')
        return updated_courses
