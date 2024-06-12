from sqlalchemy import Column, Integer
from app.database import Base

class Feedback(Base):
    __tablename__ = 'feedback'
    
    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)
