from fastapi import FastAPI
from models import RoadmapData, RoadmapResponse, RoadmapUpdateData

from vector_search import CourseVectorSearch
from skipGapAnalyzer import SkillGapAnalyzer
from ranker import CourseRanker

import json
import dotenv

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()

with open('./job_skill.json', 'r', encoding='utf-8') as f:
    job_skills_raw = json.load(f)

ROLE_TO_SKILLS = dict()
PRIORITIES_BY_ROLE = dict()
USER_SKILLS = set()
for role, skills in job_skills_raw.items():
    ROLE_TO_SKILLS[role] = [item["skill"] for item in skills]
    PRIORITIES_BY_ROLE[role] = {item["skill"]: item["priority"] for item in skills}
    USER_SKILLS.update(ROLE_TO_SKILLS[role])

search_engine = CourseVectorSearch()
analyzer = SkillGapAnalyzer(ROLE_TO_SKILLS)
ranker = CourseRanker(PRIORITIES_BY_ROLE, skill_gap_analyzer=analyzer)

ranks = dict()

app = FastAPI()

@app.get("/user_skills/")
async def get_user_skills() -> set:
    return USER_SKILLS

@app.post("/generate_roadmap/")
async def generate_roadmap(data: RoadmapData) -> RoadmapResponse:
    missing_skills = analyzer.compute_gap(data.user_skills, data.user_role)['missing_skills']
    # upd to search better
    best_courses = search_engine.get_courses(data.user_role, data.user_query, data.user_skills)
    # upd to improved ranking
    ranked_courses = ranker.rank_with_fallback(best_courses, missing_skills, data.user_skills, data.user_role)

    ranks[data.user_id] = ranked_courses

    logger.info(f"Ranked courses sample: {ranked_courses[:3]}")

    nodes = []
    for idx, course_entry in enumerate(ranked_courses[:10]):
        node = {
            "node_id": idx,
            "resource_id": course_entry["course"]["id"]
        }
        nodes.append(node)

    links = []
    for i in range(len(nodes) - 1):
        link = {
            "from_node": nodes[i]['node_id'],
            "to_node": nodes[i + 1]['node_id']
        }
        links.append(link)

    return RoadmapResponse(
        nodes=nodes,
        links=links
    )


@app.post("/update_roadmap/")
async def update_roadmap(data: RoadmapUpdateData) -> RoadmapResponse:
    ranked_courses = ranker.update_ranking(
        ranks[data.user_id],
        data.reasons,
        data.user_skills,
        data.user_role
    )
    ranks[data.user_id] = ranked_courses
    nodes = []
    for idx, course_entry in enumerate(ranked_courses[:10]):
        node = {
            "node_id": idx,
            "resource_id": course_entry["course"]["id"]
        }
        nodes.append(node)

    links = []
    for i in range(len(nodes) - 1):
        link = {
            "from_node": nodes[i]['node_id'],
            "to_node": nodes[i + 1]['node_id']
        }
        links.append(link)

    return RoadmapResponse(
        nodes=nodes,
        links=links
    )

# to get courses that marked by user as unavailable
# @app.get("/buffer_zone/")
# async def get_buffer_zone():
#     return ranker.buffer_zone

# todo: func to update known skills after re-ranking