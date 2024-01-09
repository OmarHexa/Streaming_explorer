from typing import Dict, List

import pandas as pd
import rootutils
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

rootutils.setup_root(__file__, indicator="pyproject.toml", pythonpath=True, cwd=True)
import os

from dotenv import load_dotenv

from src.backend.schema import ShowSchema

load_dotenv()
DATA_DIR = os.getenv("DATA_DIR")
# initialize the fastapi handler
app = FastAPI()


@app.get("/", response_model=Dict)
def index():
    """Welcome message for the API.

    It does nothing just to avoid starting error in the server.
    """
    return {"message": "Welcome to the app"}


# ***CRUD operations on pandas dataframe ***

# Load initial data
global data
files = os.listdir(DATA_DIR)
data = pd.read_csv(os.path.join(DATA_DIR, files[0]))
print(data.iloc[0])


# Update the FastAPI endpoint to accept an index parameter
@app.get("/shows/", response_model=List[ShowSchema])
def get_shows(index: int = 0, limit: int = 10):
    """Retrieve the shows from the dataset based on the provided index and limit."""
    start_index = index
    end_index = start_index + limit
    return data.iloc[start_index:end_index].to_dict(orient="records")


# Get a specific row by show_id
@app.get("/shows/{show_id}", response_model=ShowSchema)
def get_show_by_id(show_id: str):
    """Retrieve a specific row by show_id."""
    show_data = data[data["show_id"] == show_id].to_dict(orient="records")
    if not show_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")
    return show_data[0]  # Wrapped around list [], so [0] indexing to only return the dict


# Create a new show
@app.post("/shows/", response_model=ShowSchema, status_code=status.HTTP_201_CREATED)
def create_show(show: ShowSchema):
    """Create a new show in the dataset."""
    if show.show_id in data["show_id"].values:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Show ID already exists"
        )

    new_show = show.dict()
    data.loc[len(data)] = new_show
    return show


# Update a show by show_id
@app.put("/shows/{show_id}", response_model=ShowSchema)
def update_show(show_id: str, updated_show: ShowSchema):
    """Update a show in the dataset by show_id."""
    show_index = data[data["show_id"] == show_id].index
    if show_index.empty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")

    show_index = show_index[0]  # Extract the index value
    for key, value in updated_show.dict().items():
        data.at[show_index, key] = value

    return updated_show


# Delete a show by show_id
@app.delete("/shows/{show_id}", response_model=ShowSchema)
def delete_show(show_id: str):
    """Delete a show from the dataset by show_id."""
    show_data = data[data["show_id"] == show_id]
    if show_data.empty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")

    deleted_show = show_data.to_dict(orient="records")[0]
    data.drop(data[data["show_id"] == show_id].index, inplace=True)
    return deleted_show


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
