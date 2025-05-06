from typing import Dict, List

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import Annotated
from sqlalchemy.orm import Session

from database.model import NetflixModel
from routes.dependencies import get_db
from eda.eda_pandas import (
    country_prod_plot,
    genres_plot,
    rating_plot,
    yearly_show_plot,
)
from schema import ShowSchema


netflix_router = APIRouter(prefix="/netflix", tags=["Netflix"])


@netflix_router.get("/yearlyShowPlot", response_model=None)
def get_yearly_plot():
    """Endpoint to get the yearly show plot for Netflix.

    Returns:
        JSONResponse: Plot data in JSON format.
    """
    try:
        plot = yearly_show_plot("netflix")
        return JSONResponse(content=plot, media_type="application/json")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@netflix_router.get("/ratingPlot", response_model=None)
def get_rating_plot():
    """Endpoint to get the rating plot for Netflix.

    Returns:
        JSONResponse: Plot data in JSON format.
    """
    try:
        plot = rating_plot("netflix")
        return JSONResponse(content=plot, media_type="application/json")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@netflix_router.get("/genresPlot", response_model=None)
def get_geners_plot():
    """Endpoint to get the genres plot for Netflix.

    Returns:
        JSONResponse: Plot data in JSON format.
    """
    try:
        plot = genres_plot("netflix")
        return JSONResponse(content=plot, media_type="application/json")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@netflix_router.get("/countryProdPlot", response_model=None)
def get_country_plot():
    """Endpoint to get the country production plot for Netflix.

    Returns:
        JSONResponse: Plot data in JSON format.
    """
    try:
        plot = country_prod_plot("netflix")
        return JSONResponse(content=plot, media_type="application/json")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@netflix_router.get("/unique", response_model=Dict[str, List])
def get_unique(db: Session = Depends(get_db)):
    """Endpoint to get unique release years, ratings, actors, and directors for Netflix shows.

    Args:
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Returns:
        Dict[str, List]: Dictionary containing unique years, ratings, actors, and directors.
    """
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
