from typing import Dict, List

import rootutils
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.routing import Annotated
from sqlalchemy.orm import Session

rootutils.setup_root(__file__, indicator="pyproject.toml", pythonpath=True, cwd=True)

from src.backend.database.mysql.model import NetflixModel
from src.backend.dependencies import get_db
from src.backend.schema import ShowSchema

netflix_router = APIRouter(prefix="/netflix", tags=["Netflix"])


@netflix_router.get("/unique", response_model=Dict[str, List])
async def get_unique(db: Session = Depends(get_db)):
    unique_years = (
        db.query(NetflixModel.release_year)
        .distinct()
        .order_by(NetflixModel.release_year.desc())
        .all()
    )

    # unique_actors = db.query(NetflixModel.cast).distinct().all()
    # unique_directors = db.query(NetflixModel.director).distinct().all()
    unique_ratings = db.query(NetflixModel.rating).distinct().all()

    if not unique_years:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")

    return {
        "years": [year[0] for year in unique_years],
        # "actors": [actor[0] for actor in unique_actors],
        # "directors": [director[0] for director in unique_directors],
        "ratings": [rating[0] for rating in unique_ratings],
    }


@netflix_router.get("/shows", response_model=List[ShowSchema], status_code=status.HTTP_200_OK)
def get_shows(
    db: Annotated[Session, Depends(get_db)],
    index: int = Query(0, description="Index to start retrieving shows", ge=0),
    limit: int = Query(10, description="Number of shows to retrieve", ge=1, le=50),
    filters: dict = Body(None, description="Filter shows based on column name and value"),
):
    """Retrieve the shows from the dataset based on the provided index, limit, and filters.

    Currently request body on get function has undefined behavior. So it doesn't work with FastAPI-
    Swagger but works fine from python request. We will change this behavior on our next version.
    """
    query = db.query(NetflixModel)
    # netflix_routerly filters if provided
    if filters:
        for column, value in filters.items():
            query = query.filter(getattr(NetflixModel, column) == value)

    # netflix_routerly offset and limit
    shows = query.offset(index).limit(limit).all()

    # Use jsonable_encoder to convert SQLAlchemy models to dictionaries
    shows_dict = jsonable_encoder(shows)

    return shows_dict


@netflix_router.get("/{show_id}", response_model=ShowSchema, status_code=status.HTTP_200_OK)
def get_show_by_id(show_id: str, db: Annotated[Session, Depends(get_db)]):
    """Retrieve a specific row by show_id."""
    show = db.query(NetflixModel).filter(NetflixModel.show_id == show_id).first()
    if not show:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")
    return show


@netflix_router.post("/shows", response_model=ShowSchema, status_code=status.HTTP_201_CREATED)
def create_show(show: ShowSchema, db: Annotated[Session, Depends(get_db)]):
    """Create a new show in the dataset."""
    db_show = NetflixModel(**show.model_dump())
    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return db_show


@netflix_router.put("/{show_id}", response_model=ShowSchema)
def update_show(show_id: str, updated_show: Dict, db: Annotated[Session, Depends(get_db)]):
    """Update a show in the dataset by show_id."""
    db_show = db.query(NetflixModel).filter(NetflixModel.show_id == show_id).first()
    if not db_show:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")

    for key, value in updated_show.items():
        setattr(db_show, key, value)

    db.commit()
    db.refresh(db_show)
    return db_show


@netflix_router.delete("/{show_id}", response_model=ShowSchema)
def delete_show(show_id: str, db: Annotated[Session, Depends(get_db)]):
    """Delete a show from the dataset by show_id."""
    db_show = db.query(NetflixModel).filter(NetflixModel.show_id == show_id).first()
    if not db_show:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")

    db.delete(db_show)
    db.commit()
    return db_show
