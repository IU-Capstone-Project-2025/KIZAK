from db.roadmap import create_roadmap, create_node
from models.roadmap import RoadmapCreate, NodeCreate
from uuid import UUID


class RoadmapFenerator():
    def genearte(required_skills: list[str]):


async def geterate_roadmap(
    required_skills: list[str],
    user_id: UUID
) -> int:
    roadmap = create_roadmap(
        RoadmapCreate(
            user_id=user_id
        )
    )
    create_node(
        NodeCreate(
            roadmap_id=roadmap['roadmap_id']
        )
    )
    return 1
