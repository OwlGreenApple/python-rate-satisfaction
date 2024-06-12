from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas, models
from ..database import get_db

router = APIRouter()

@router.post("/feedback/", response_model=schemas.Feedback)
async def create_feedback(feedback: schemas.FeedbackCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_feedback(db, feedback)

@router.get("/feedback/{feedback_id}", response_model=schemas.Feedback)
async def read_feedback(feedback_id: int, db: AsyncSession = Depends(get_db)):
    db_feedback = await crud.get_feedback(db, feedback_id)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return db_feedback
