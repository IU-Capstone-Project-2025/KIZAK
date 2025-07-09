from db.db_connector import db

from models.feedback import FeedbackCreate, FeedbackResponse

async def create_feedback(feedback: FeedbackCreate) -> FeedbackResponse:
    try:
        feedback_row = await db.fetchrow("""
            INSERT INTO roadmap_feedback(
                user_id,
                roadmap_id,
                resource_id,
                is_liked,
                reason
            ) VALUES ($1, $2, $3, $4, $5)
            RETURNING *
            """,
            feedback.user_id,
            feedback.roadmap_id,
            feedback.resource_id,
            feedback.is_liked,
            feedback.reason
        )
        
        return FeedbackResponse(**feedback_row)
    except:
        raise