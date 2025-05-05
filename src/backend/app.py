from typing import Dict

import rootutils
from fastapi import FastAPI

rootutils.setup_root(__file__, indicator="pyproject.toml", pythonpath=True, cwd=True)

from backend.database.config import engine # noqa: E402
from backend.database.model import Base # noqa: E402
from src.backend.recommender import recommend_similar_shows # noqa: E402
from src.backend.routes.amazon import amazon_router # noqa: E402
from src.backend.routes.disney import disney_router  # noqa: E402
from src.backend.routes.netflix import netflix_router  # noqa: E402

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
