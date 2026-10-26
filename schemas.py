from pydantic import BaseModel, Field
from typing import Optional

class MovieBase(BaseModel):
    title: str = Field(..., max_length=255, description="Название фильма")
    description: Optional[str] = Field(None, description="Описание фильма")
    release_year: int = Field(..., ge=1888, description="Год выпуска (не ранее 1888)")
    genre: str = Field(..., max_length=100, description="Жанр фильма")
    rating: float = Field(0.0, ge=0.0, le=10.0, description="Рейтинг от 0.0 до 10.0")

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    release_year: Optional[int] = Field(None, ge=1888)
    genre: Optional[str] = Field(None, max_length=100)
    rating: Optional[float] = Field(None, ge=0.0, le=10.0)

class MovieResponse(MovieBase):
    id: int

    class Config:
        from_attributes = True