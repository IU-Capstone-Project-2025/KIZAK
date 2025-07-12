from typing import List
from uuid import UUID

from db.roadmap import create_roadmap, create_node, create_link
from db.db_connector import db

from models.roadmap import RoadmapInfo, RoadmapCreate
from models.roadmap import NodeResponse, NodeCreate
from models.roadmap import LinkResponse, LinkCreate

from models.user import UserSkill

import requests

async def generate_roadmap(
    user_id: UUID,
    user_role: str,
    user_skills: List[UserSkill],
    user_query: str
) -> RoadmapInfo:
    try:
        data = {
            "user_role": user_role,
            "user_skills": [skill.skill for skill in user_skills],
            "user_query": user_query
        }
        response = requests.post("http://ml:8001/generate_roadmap/", json=data)
        response.raise_for_status()
        roadmap_info = response.json()
        
        roadmap = await create_roadmap(
            RoadmapCreate(user_id=user_id)
        )
        
        nodes = []
        for course in roadmap_info["nodes"]:
            resource_details = await db.fetchrow(
                """
                SELECT
                    resource_id,
                    title,
                    summary
                FROM
                    resource
                WHERE
                    resource_id = $1
            """,
                course["resource_id"],
            )
            node = await create_node(
                NodeCreate(
                    roadmap_id=roadmap.roadmap_id,
                    title=resource_details["title"],
                    summary=resource_details["summary"],
                    resource_id=resource_details["resource_id"],
                    progress="Not started"
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
        
    except requests.exceptions.RequestException as e:
        print(f"Error calling ML service: {e}")
        return None
