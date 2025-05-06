from typing import Dict

import rootutils
from fastapi import FastAPI


from database.config import engine 
from database.model import Base 
from recommender import recommend_similar_shows
from routes.amazon import amazon_router 
from routes.disney import disney_router 
from routes.netflix import netflix_router 

rootutils.setup_root(__file__, indicator="pyproject.toml", pythonpath=True, cwd=True)
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
