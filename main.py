from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Каталог фильмов API",
    description="REST API для управления каталогом фильмов с фильтрацией и сортировкой",
    version="1.0.0"
)

@app.post("/movies/", response_model=schemas.MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    db_movie = models.Movie(**movie.model_dump())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.get("/movies/", response_model=List[schemas.MovieResponse])
def get_movies(
    genre: Optional[str] = Query(None, description="Фильтрация по жанру"),
    year: Optional[int] = Query(None, description="Фильтрация по году выпуска"),
    min_rating: Optional[float] = Query(None, ge=0.0, le=10.0, description="Минимальный рейтинг"),
    sort_by: Optional[str] = Query("id", description="Поле для сортировки: year, rating, title, id"),
    order: Optional[str] = Query("asc", description="Порядок сортировки: asc или desc"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Movie)

    if genre:
        query = query.filter(models.Movie.genre.ilike(f"%{genre}%"))
    if year:
        query = query.filter(models.Movie.release_year == year)
    if min_rating is not None:
        query = query.filter(models.Movie.rating >= min_rating)

    sort_fields = {
        "year": models.Movie.release_year,
        "rating": models.Movie.rating,
        "title": models.Movie.title,
        "id": models.Movie.id
    }
    
    sort_column = sort_fields.get(sort_by, models.Movie.id)
    if order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    return query.all()

@app.get("/movies/{movie_id}", response_model=schemas.MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    return movie

@app.put("/movies/{movie_id}", response_model=schemas.MovieResponse)
def update_movie(movie_id: int, movie_data: schemas.MovieUpdate, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")

    for key, value in movie_data.model_dump(exclude_unset=True).items():
        setattr(movie, key, value)

    db.commit()
    db.refresh(movie)
    return movie

@app.delete("/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")

    db.delete(movie)
    db.commit()
    return None