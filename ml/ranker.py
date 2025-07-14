from typing import List, Dict, Any
import numpy as np
import re
import random

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

class CourseRanker:
    STRATEGIES = {
        "basic": {
            # basic balanced rankin, no penalties
            "weights": {"coverage": 0.45, "priority": 0.45, "rating": 0.1},
            "filter_low_quality": False,  # allow low tarred courses
            "diversity_penalty": 0.0,  # allow intersection of skill coverages among courses
            "known_skills_penalty": 0.0,  # allow courses with known skills
            "position_bias_shuffle": False,  # do not shuffly similar scored courses
            "max_top_similar_courses": None,  # allow similar in skills set courses
        },

        "skill_gain_focus": {
            # More weight to coverage, do filtration and penalties for known skills
            "weights": {"coverage": 0.7, "priority": 0.2, "rating": 0.1},
            "filter_low_quality": True,  # throw out bad starred courses
            "diversity_penalty": 0.3,  # moderate penalty for intersection of skills btw courses
            "known_skills_penalty": 0.2,  # moderate penalty for teaching already known skills
            "position_bias_shuffle": True,  # shuffle similar scorred
            "max_top_similar_courses": None,
        },

        "diversity_focus": {
            # Give priority to skills variance, large penalty for similarity, small for known skills
            "weights": {"coverage": 0.4, "priority": 0.3, "rating": 0.3},
            "filter_low_quality": True,
            "diversity_penalty": 0.5,  # big penalty for skills set intersection
            "known_skills_penalty": 0.1,  # small penalty for known skills
            "position_bias_shuffle": True,
            "max_top_similar_courses": 5,  # max # similar in skills sets courses
        },

        "position_bias_control": {
            # Control concentration of good courses by shuffling and small penalties
            "weights": {"coverage": 0.5, "priority": 0.4, "rating": 0.1},
            "filter_low_quality": False,
            "diversity_penalty_weight": 0.2,
            "known_skills_penalty_weight": 0.1,
            "position_bias_shuffle": True,
            "max_top_similar_courses": 3,  # max # similar in skills sets courses
        }
    #     todo: add strategies to re-rank based on feedback (if needed)
    }

    def __init__(self, priorities_by_role: Dict[str, Dict[str, int]], skill_gap_analyzer=None, rating_max: float = 5.0):
        self.priorities_by_role = priorities_by_role
        self.rating_max = rating_max
        self.skill_gap_analyzer = skill_gap_analyzer

        # diversity, skill gain and positional bias from last ranking
        self.last_metrics = {}

        # to change dynamically
        self.skill_gain_threshold = 6.0
        self.diversity_threshold = 2.5
        self.position_bias_threshold = 4.0

        self.buffer_zone = []  # unavailable courses to delete from db

    def get_metrics(self):
        return self.last_metrics

    def _filter_low_quality_courses(self, courses: List[Dict]) -> List[Dict]:
        """throw out courses without any skills or with bad rating"""
        return [
            c for c in courses
            if c.get("skills") and (c.get("rating", 0) or 0) >= 3
        ]

    def _limit_similar_courses(self, ranked: List[Dict], max_similar: int) -> List[Dict]:
        """
        reduce number of courses with similar skills sets to max_similar.
        similarity defines as nof intersected skills >= 50% smaller set
        """
        limited = []
        skill_sets = []

        def is_similar(skills1, skills2):
            set1, set2 = set(skills1), set(skills2)
            intersection = len(set1.intersection(set2))
            threshold = min(len(set1), len(set2)) * 0.5
            return intersection >= threshold

        for item in ranked:
            skills = item["covered_skills"]
            similar_count = sum(is_similar(skills, s) for s in skill_sets)
            if similar_count < max_similar:
                limited.append(item)
                skill_sets.append(skills)
            # esle - skip course

        return limited

    def _shuffle_similar_scores(self, ranked: List[Dict], epsilon: float = 0.01) -> List[Dict]:
        """
        shuffle courses with similar scores (diff <= epsilon), to reduce position bias.
        """
        if not ranked:
            return ranked

        shuffled = []
        buffer = [ranked[0]]

        for i in range(1, len(ranked)):
            prev_score = buffer[-1]["ranking_score"]
            curr_score = ranked[i]["ranking_score"]

            if abs(curr_score - prev_score) <= epsilon:
                buffer.append(ranked[i])
            else:
                random.shuffle(buffer)
                shuffled.extend(buffer)
                buffer = [ranked[i]]

        random.shuffle(buffer)
        shuffled.extend(buffer)

        return shuffled

    def normalize_skill(self, skill: str) -> str:
        skill = skill.lower()
        skill = re.sub(r"[^a-z0-9\s]", "", skill)
        return skill.strip()

    def get_skill_words(self, skills: list[str]) -> set[str]:
        words = set()
        for skill in skills:
            normalized = self.normalize_skill(skill)
            splited = normalized.split()
            words.update(splited)
        return words

    def prepare_courses(self, search_results: List[Dict]) -> List[Dict]:
        """
        Converts raw search results to format expected by ranking logic
        while preserving all metadata for re-ranking.
        """
        courses = []
        for res in search_results:
            original = res["details"]["original_point"]
            course = {
                "id": res["details"]["id"],
                "title": original.get("title"),
                "skills": original.get("skills", []),
                "rating": original.get("rating", 0),
                "price": original.get("price", 0),
                "author": original.get("author")
            }
            courses.append(course)
        return courses

    def rank_courses(self,
                     courses: List[Dict], # from cosine similarity search
                     skill_gap: List[str], #from skillgap
                     known_skills: List[str],
                     target_role: str, # from user onboarding info
                     weights: Dict[str, float] = None, # alpha beta for ranking
                     strategy_name: str = "basic" # to recalculate if offline metrics are bad
                     ) -> List[Dict]:
        #identify startegy
        strategy = self.STRATEGIES.get(strategy_name, self.STRATEGIES["basic"])

        # choose weights of strategy
        if weights is None:
            weights = strategy["weights"]

        # get priorities from job-skills mapping
        priorities = self.priorities_by_role.get(target_role, {})

        # known_skills = set(known_skills)

        ranked = []
        for course in courses:
            # temporarily return kostyl normalizing
            raw_course_skills = course.get("skills", [])
            if isinstance(raw_course_skills, str):
                try:
                    import ast
                    raw_course_skills = ast.literal_eval(raw_course_skills)
                except Exception:
                    raw_course_skills = []

            course_skills = self.get_skill_words(raw_course_skills)

            # course_skills = course.get("skills", [])

            covered_skills = set(course_skills).intersection(set(skill_gap))

            # how many skills are covered by this course, the more the >>
            coverage_score = len(covered_skills) / len(skill_gap) if skill_gap else 0

            #how large is priority of skills for that course
            priority_score_sum = sum(priorities.get(skill, 0.0) for skill in covered_skills)
            mean_priority_score = priority_score_sum / len(covered_skills) if covered_skills else 0

            raw_rating = course.get("rating", None)
            rating = raw_rating if raw_rating is not None else 0.3 * self.rating_max
            rating_score = rating / self.rating_max

            score = (
                    weights["coverage"] * coverage_score +
                    weights["priority"] * mean_priority_score +
                    weights["rating"] * rating_score
            )

            # now penalties :(

            # diversity penalty — for intersection with already picked courses
            if strategy["diversity_penalty"] > 0 and ranked:
                overlap = 0
                for prev in ranked:
                    overlap += len(set(prev["covered_skills"]).intersection(covered_skills))
                overlap /= len(ranked)
                score -= strategy["diversity_penalty"] * overlap

            # known skills penalty — for using skills that user know
            if strategy["known_skills_penalty"] > 0:
                known_overlap = len(set(known_skills).intersection(covered_skills))
                score -= strategy["known_skills_penalty"] * known_overlap

            ranked.append({
                "course": course,
                "ranking_score": round(score, 4),
                "covered_skills": list(covered_skills)
            })

        # sort by score
        ranked = sorted(ranked, key=lambda x: x["ranking_score"], reverse=True)

        max_sim = strategy.get("max_top_similar_courses")
        if max_sim is not None:
            ranked = self._limit_similar_courses(ranked, max_sim)

        if strategy.get("position_bias_shuffle"):
            ranked = self._shuffle_similar_scores(ranked)

        return ranked


    def evaluate_ranking(self,
                         ranked_courses: List[Dict], #init ranking
                         target_role: str,
                         k: int = 10 # top-k
                         ) -> Dict[str, float]:
        priorities = self.priorities_by_role.get(target_role, {})

        # Skill Gain: priorities of covered skills in top-k courses
        top_k = ranked_courses[:k]
        skill_gain = sum(
            priorities.get(skill, 0.0)
            for item in top_k
            for skill in item["covered_skills"]
        )

        # Diversity: entropy(variety) of skills in top-k
        from collections import Counter
        all_skills = [s for item in top_k for s in item["covered_skills"]]
        skill_counts = Counter(all_skills)
        total = sum(skill_counts.values())
        diversity_score = 0.0
        if total > 0:
            diversity_score = -sum(
                (count / total) * np.log2(count / total)
                for count in skill_counts.values()
            )

        # Position bias: how necessary skills are concentrated in the upper positions
        position_bias = sum(
            priorities.get(skill, 0.0) / np.log2(idx + 2)
            for idx, item in enumerate(top_k)
            for skill in item["covered_skills"]
        )

        return {
            "skill_gain": round(skill_gain, 4),
            "diversity_score": round(diversity_score, 4),
            "position_bias": round(position_bias, 4)
        }

    def check_skill_gain(self, metrics: Dict[str, float]) -> bool:
        # todo: threshold of skill gain
        return metrics.get("skill_gain", 0) >= self.skill_gain_threshold

    def check_diversity(self, metrics: Dict[str, float]) -> bool:
        # todo: entropy threshold
        return metrics.get("diversity_score", 0) >= self.diversity_threshold

    def check_position_bias(self, metrics: Dict[str, float]) -> bool:
        # todo: threshold of pos bias
        # position_bias — the << the better (too concentrated sjills on the top is not cool)
        return metrics.get("position_bias", 0) <= self.position_bias_threshold

    def rank_with_fallback(self,
                           search_res: List[Dict],
                           skill_gap: List[str],
                           known_skills: List[str],
                           target_role: str,
                           max_attempts: int = 5 #attenpt to improve 3 times
                           ) -> List[Dict]:
        """Cyclic ranks with different strategies until offline metrics are better"""

        courses = self.prepare_courses(search_res)

        tried_strategies = set()
        strategy = "basic"  # start with basic one

        for attempt in range(max_attempts):
            if strategy in tried_strategies:
                # if tried current strategy - choose different
                strategy = "basic"

            tried_strategies.add(strategy)

            params = self.STRATEGIES[strategy]
            logger.info(f"Ranking attempt {attempt + 1} with strategy '{strategy}'")

            ranked = self.rank_courses(
                courses,
                skill_gap,
                known_skills,
                target_role,
                weights=params["weights"],
                strategy_name=strategy
            )

            metrics = self.evaluate_ranking(ranked, target_role)
            self.last_metrics = metrics
            logger.info(f"Evaluation metrics: {metrics}")

            skill_gain_ok = self.check_skill_gain(metrics)
            diversity_ok = self.check_diversity(metrics)
            position_bias_ok = self.check_position_bias(metrics)

            logger.info(
                f"Skill gain OK: {skill_gain_ok}, Diversity OK: {diversity_ok}, Position bias OK: {position_bias_ok}")

            if skill_gain_ok and diversity_ok and position_bias_ok:
                return ranked

            # choose next strategy
            if not skill_gain_ok and "skill_gain_focus" not in tried_strategies:
                strategy = "skill_gain_focus"
            elif not diversity_ok and "diversity_focus" not in tried_strategies:
                strategy = "diversity_focus"
            elif not position_bias_ok and "position_bias_control" not in tried_strategies:
                strategy = "position_bias_control"
            else:
                # all tried, return last (hopefully best)
                break

        return ranked

    def update_ranking(self,
                       ranked_courses: List[Dict],
                       feedback_dict: Dict[int, str],  # - "too_easy"
                                            # - "wrong_skills"
                                            # - "too_hard"
                                            # - "bad_author"
                                            # - "unavailable"
                       known_skills: List[str],
                       user_role: str
                       ) -> List[Dict]:
        """
        Re-ranking based on user feedback (human metric)
        """
        updated_courses = ranked_courses.copy()
        new_known_skills = set(known_skills) #to update

        for node_id, feedback_type in feedback_dict.items():
            if node_id >= len(updated_courses):
                continue

            course = updated_courses[node_id]
            details = course["course"]["details"]
            original = details.get("original_point", {})

            course_id = details.get("id")
            course_skills = set(original.get("skills", []))
            author = original.get("author")

            logger.info(f"Feedback '{feedback_type}' on course {course_id} at node {node_id}")

            if feedback_type == "too_easy":
                # update known skills
                new_known_skills.update(course_skills)
                # throw out course
                updated_courses = [
                    c for c in updated_courses
                    if c["course"]["details"]["id"] != course_id
                ]
            elif feedback_type == "wrong_skills":
                # throw out this course and similar ones
                updated_courses = [
                    c for c in updated_courses
                    if c["course"]["details"]["id"] != course_id and not (
                            course_skills & set(c["course"]["details"]["original_point"].get("skills", []))
                    )
                ]
            elif feedback_type == "too_hard":
                # make course further in roadmap
                logger.info('Feedback type is "too_hard"')
                if node_id < len(updated_courses):
                    course = updated_courses.pop(node_id)
                    new_pos = min(node_id + 3, len(updated_courses))
                    updated_courses.insert(new_pos, course)
            elif feedback_type == "bad_author":
                # throw out courses with that author
                updated_courses = [
                    c for c in updated_courses
                    if c["course"]["details"]["original_point"].get("author") != author
                ]
            elif feedback_type == "unavailable":
                # throw out course and add it to a buffer zone
                updated_courses = [
                    c for c in updated_courses
                    if c["course"]["details"]["id"] != course_id
                ]
                self.buffer_zone.append(course)
            else:
                logger.warning(f"Unknown feedback type: {feedback_type}")

        # recalculate skill gap and rerank
        if new_known_skills != set(known_skills) and self.skill_gap_analyzer:
            missing_skills = self.skill_gap_analyzer.compute_gap(list(new_known_skills), user_role)[
                "missing_skills"]
            flattened_courses = [c["course"]["details"]["original_point"] for c in updated_courses]
            for course in flattened_courses:
                course["id"] = course.get("id") or course.get("url")  # ensure ID exists
            updated_courses = self.rank_courses(flattened_courses, missing_skills, list(new_known_skills),
                                                user_role)

        return updated_courses
