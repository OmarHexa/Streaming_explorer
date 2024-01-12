from typing import Dict, List

import rootutils
from fastapi import Body, Depends, FastAPI, HTTPException, Query, status
from fastapi.routing import Annotated
from sqlalchemy.orm import Session

rootutils.setup_root(__file__, indicator="pyproject.toml", pythonpath=True, cwd=True)

from backend.recommender import recommend_similar_shows
from src.backend.database.mysql.config import engine
from src.backend.database.mysql.model import Base
from src.backend.routes.amazon import amazon_router
from src.backend.routes.disney import disney_router
from src.backend.routes.netflix import netflix_router
from src.backend.schema import ShowSchema

Base.metadata.create_all(bind=engine)
# FastAPI setup
app = FastAPI()

app.include_router(amazon_router)
app.include_router(disney_router)
app.include_router(netflix_router)


@app.get("/", response_model=Dict)
def index():
    """Welcome message for the API.

    It does nothing just to avoid starting error in the server.
    """
    return {"message": "Welcome to the app"}


@app.post("/recommend")
def recommend(title: Dict):
    """This function recommends similar shows from different platform."""
    show = recommend_similar_shows(title["title"])
    return show


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
