from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from app.database import engine, Base, get_db
from app.models import Feedback
from pydantic import BaseModel
from sqlalchemy.future import select

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:5173",  # Assuming your frontend runs on this port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FeedbackSchema(BaseModel):
    score: int

    class Config:
        orm_mode = True

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
@app.post("/feedback", response_model=dict)
async def create_feedback(feedback: FeedbackSchema, db: AsyncSession = Depends(get_db)):
    if feedback.score < 1 or feedback.score > 5:
        raise HTTPException(status_code=422, detail="Score must be between 1 and 5")
    new_feedback = Feedback(score=feedback.score)
    db.add(new_feedback)
    await db.commit()
    await db.refresh(new_feedback)
    return {"message": "Feedback submitted successfully"}
    
@app.options("/feedback")
async def options_feedback():
    return JSONResponse({"message": "OK"})