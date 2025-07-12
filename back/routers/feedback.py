from fastapi import APIRouter
from fastapi import status

from models.feedback import FeedbackResponse

from db.feedback import create_feedback

router = APIRouter()

@router.post(
    "/feedback/",
    response_model=FeedbackResponse,
    tags=["Feedback"],
    description="Post users feedback",
    status_code=status.HTTP_201_CREATED
    )
async def post_feedback(feedback: FeedbackResponse) -> FeedbackResponse:
    return await create_feedback(feedback)
