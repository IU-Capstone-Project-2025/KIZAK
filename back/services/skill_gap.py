from ml.skipGapAnalyzer import analyzer


async def get_gaps(current_skills: list[str], goal_role: str) -> list[str]:
    return analyzer.compute_gap(current_skills, goal_role)
