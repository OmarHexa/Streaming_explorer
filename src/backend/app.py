from typing import Dict, List, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator

# initialize the fastapi handler
app = FastAPI()

# Load initial data
global data
data = pd.read_csv("./Data/processed/netflix.csv")


# Define Pydantic model for the dataset
class ShowData(BaseModel):
    show_id: str
    type: str
    title: str
    director: Optional[str] = None
    cast: Optional[str] = None
    country: Optional[str] = None
    date_added: Optional[str] = None
    release_year: Optional[int] = None
    rating: str
    duration: Optional[str] = None
    listed_in: Optional[str] = None
    description: Optional[str] = None


# CRUD operations


@app.get("/", response_model=Dict)
def index():
    """Welcome message for the API.

    It does nothing just to avoid starting error in the server.
    """
    return {"message": "Welcome to the app"}


# Update the FastAPI endpoint to accept an index parameter
@app.get("/shows/", response_model=List[ShowData])
def get_shows(index: int = 0, limit: int = 10):
    """Retrieve the shows from the dataset based on the provided index and limit."""
    start_index = index
    end_index = start_index + limit
    return data.iloc[start_index:end_index].to_dict(orient="records")


# Get a specific row by show_id
@app.get("/shows/{show_id}", response_model=ShowData)
def get_show_by_id(show_id: str):
    """Retrieve a specific row by show_id."""
    show_data = data[data["show_id"] == show_id].to_dict(orient="records")
    if not show_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")
    return show_data[0]  # Wrapped around list [], so [0] indexing to only return the dict


# Create a new show
@app.post("/shows/", response_model=ShowData, status_code=status.HTTP_201_CREATED)
def create_show(show: ShowData):
    """Create a new show in the dataset."""
    if show.show_id in data["show_id"].values:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Show ID already exists"
        )

    new_show = show.dict()
    data.loc[len(data)] = new_show
    return show


# Update a show by show_id
@app.put("/shows/{show_id}", response_model=ShowData)
def update_show(show_id: str, updated_show: ShowData):
    """Update a show in the dataset by show_id."""
    show_index = data[data["show_id"] == show_id].index
    if show_index.empty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")

    show_index = show_index[0]  # Extract the index value
    for key, value in updated_show.dict().items():
        data.at[show_index, key] = value

    return updated_show


# Delete a show by show_id
@app.delete("/shows/{show_id}", response_model=ShowData)
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
