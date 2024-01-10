from typing import Dict, List

import rootutils
from fastapi import Body, Depends, FastAPI, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.routing import Annotated
from sqlalchemy.orm import Session

rootutils.setup_root(__file__, indicator="pyproject.toml", pythonpath=True, cwd=True)

from src.backend.database.mysql.config import SessionLocal, engine
from src.backend.database.mysql.model import Base, ShowModel
from src.backend.schema import ShowSchema

Base.metadata.create_all(bind=engine)


# Dependency for getting a database session
# see the following link to more about dependencies with yield
# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# FastAPI setup
app = FastAPI()

# CRUD operations on MySQL database using SQLAlchemy ORM #


@app.get("/", response_model=Dict)
def index():
    """Welcome message for the API.

    It does nothing just to avoid starting error in the server.
    """
    return {"message": "Welcome to the app"}


@app.get("/unique", response_model=Dict[str, List])
async def get_unique(db: Session = Depends(get_db)):
    unique_years = (
        db.query(ShowModel.release_year).distinct().order_by(ShowModel.release_year.desc()).all()
    )

    # unique_actors = db.query(ShowModel.cast).distinct().all()
    # unique_directors = db.query(ShowModel.director).distinct().all()
    unique_ratings = db.query(ShowModel.rating).distinct().all()

    if not unique_years:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")

    return {
        "years": [year[0] for year in unique_years],
        # "actors": [actor[0] for actor in unique_actors],
        # "directors": [director[0] for director in unique_directors],
        "ratings": [rating[0] for rating in unique_ratings],
    }


# @app.get("/shows/", response_model=List[ShowSchema], status_code=status.HTTP_200_OK)
# def get_shows(db: Annotated[Session, Depends(get_db)], index: int = 0, limit: int = 10):
#     """Retrieve the shows from the dataset based on the provided index and limit."""
#     shows = db.query(ShowModel).offset(index).limit(limit).all()

#     # Use jsonable_encoder to convert SQLAlchemy models to dictionaries
#     shows_dict = jsonable_encoder(shows)

#     return shows_dict


@app.get("/shows/", response_model=List[ShowSchema], status_code=status.HTTP_200_OK)
def get_shows(
    db: Annotated[Session, Depends(get_db)],
    index: int = Query(0, description="Index to start retrieving shows", ge=0),
    limit: int = Query(10, description="Number of shows to retrieve", ge=1, le=50),
    filters: dict = Body(None, description="Filter shows based on column name and value"),
):
    """Retrieve the shows from the dataset based on the provided index, limit, and filters."""
    query = db.query(ShowModel)
    # Apply filters if provided
    if filters:
        for column, value in filters.items():
            query = query.filter(getattr(ShowModel, column) == value)

    # Apply offset and limit
    shows = query.offset(index).limit(limit).all()

    # Use jsonable_encoder to convert SQLAlchemy models to dictionaries
    shows_dict = jsonable_encoder(shows)

    return shows_dict


@app.get("/shows/{show_id}", response_model=ShowSchema, status_code=status.HTTP_200_OK)
def get_show_by_id(show_id: str, db: Annotated[Session, Depends(get_db)]):
    """Retrieve a specific row by show_id."""
    show = db.query(ShowModel).filter(ShowModel.show_id == show_id).first()
    if not show:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")
    return show


@app.post("/shows/", response_model=ShowSchema, status_code=status.HTTP_201_CREATED)
def create_show(show: ShowSchema, db: Annotated[Session, Depends(get_db)]):
    """Create a new show in the dataset."""
    db_show = ShowModel(**show.dict())
    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return db_show


@app.put("/shows/{show_id}", response_model=ShowSchema)
def update_show(show_id: str, updated_show: Dict, db: Annotated[Session, Depends(get_db)]):
    """Update a show in the dataset by show_id."""
    db_show = db.query(ShowModel).filter(ShowModel.show_id == show_id).first()
    if not db_show:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")

    for key, value in updated_show.items():
        setattr(db_show, key, value)

    db.commit()
    db.refresh(db_show)
    return db_show


@app.delete("/shows/{show_id}", response_model=ShowSchema)
def delete_show(show_id: str, db: Annotated[Session, Depends(get_db)]):
    """Delete a show from the dataset by show_id."""
    db_show = db.query(ShowModel).filter(ShowModel.show_id == show_id).first()
    if not db_show:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")

    db.delete(db_show)
    db.commit()
    return db_show


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
