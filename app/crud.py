from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Feedback
from app.schemas import FeedbackCreate

async def create_feedback(db: AsyncSession, feedback: FeedbackCreate):
    db_feedback = Feedback(score=feedback.score)
    db.add(db_feedback)
    await db.commit()
    await db.refresh(db_feedback)
    return db_feedback
