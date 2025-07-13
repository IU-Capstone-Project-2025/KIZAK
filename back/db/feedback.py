from db.db_connector import db

from models.feedback import FeedbackCreate, FeedbackResponse


async def create_feedback(feedback: FeedbackCreate) -> FeedbackResponse:
    try:
        feedback_row = await db.fetchrow("""
            INSERT INTO roadmap_feedback(
                "user_id",
                "node_id",
                "reason"
            ) VALUES ($1, $2, $3)
            RETURNING *
            """,
            feedback.user_id,
            feedback.node_id,
            feedback.reason
        )

        return FeedbackResponse(**feedback_row)
    except:
        raise
