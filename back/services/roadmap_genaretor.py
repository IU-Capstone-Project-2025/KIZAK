from typing import List
from uuid import UUID

from db.roadmap import create_roadmap, create_node, create_link

from models.roadmap import RoadmapInfo, RoadmapCreate
from models.roadmap import NodeResponse, NodeCreate
from models.roadmap import LinkResponse, LinkCreate

from app import analyzer, search_engine, ranker

import dotenv

dotenv.load_dotenv()

def _get_missing_skills(user_skills, user_role):
    gap_results = analyzer.compute_gap(user_skills, user_role)
    return gap_results['missing_skills']

def _get_best_courses(user_role, user_skills, user_query):
    return search_engine.get_courses(user_role, user_query, user_skills)

def _rank_courses(best_courses, user_skills, user_role):
    return ranker.rank_courses(best_courses, user_skills, user_role)

async def generate_roadmap(user_id: UUID, user_role: str, user_skills: List[str], user_query: str) -> RoadmapInfo:
    missing_skills = _get_missing_skills(user_skills, user_role)
    best_courses = _get_best_courses(user_role, user_skills, user_query)
    ranked_courses = _rank_courses(best_courses, missing_skills, user_role)

    print("Top 5 Recommended Courses:\n")
    for i, course_entry in enumerate(ranked_courses[:5], 1):
        title = course_entry["course"]["details"]["title"]
        uuid = course_entry["course"]["details"]["id"]
        print(f"{i}. {title} (UUID: {uuid})")

    roadmap = await create_roadmap(
        RoadmapCreate(user_id=user_id)
    )

    nodes = []
    for course_entry in ranked_courses[:5]:
        details = course_entry["course"]["details"]
        node = await create_node(
            NodeCreate(
                roadmap_id=roadmap.roadmap_id,
                title=details["title"],
                summary=details["original_point"].get("summary", ""),
                resource_id=UUID(details["id"]),
                progress=0
            )
        )
        nodes.append(node)

    links = []
    for i in range(len(nodes) - 1):
        link = await create_link(
            LinkCreate(
                roadmap_id=roadmap.roadmap_id,
                from_node=nodes[i].node_id,
                to_node=nodes[i + 1].node_id
            )
        )
        links.append(link)

    return RoadmapInfo(
        roadmap_id=roadmap.roadmap_id,
        nodes=nodes,
        links=links
    )
