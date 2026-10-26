from sqlalchemy import Column, Integer, String, Float, CheckConstraint
from database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(String, nullable=True)
    release_year = Column(Integer, nullable=False)
    genre = Column(String(100), nullable=False, index=True)
    rating = Column(Float, default=0.0)

    __table_args__ = (
        CheckConstraint('release_year >= 1888', name='check_release_year_min'),
        CheckConstraint('rating >= 0.0 AND rating <= 10.0', name='check_rating_range'),
    )