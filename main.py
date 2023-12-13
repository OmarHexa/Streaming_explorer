import json
import logging
from typing import List, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator

# initialize the fastapi handler
app = FastAPI()

# Load initial data
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
    release_year: int
    rating: Optional[str] = None
    duration: str
    listed_in: str
    description: str

    # class Config:
    #     validate_assignment = True  # Enable validation for optional fields

    # @validator("show_id", pre=True, always=True)
    # def validate_show_id(cls, value):
    #     # Validate show_id uniqueness here, e.g., using a database query
    #     # For simplicity, assuming show_id is unique in this example
    #     return value


# CRUD operations


@app.get("/", response_model=str)
def index():
    """Welcome message for the API."""
    return {"message": "Welcome to the app"}


# Get the first 5 rows
@app.get("/shows/", response_model=List[ShowData])
def get_first_five_rows():
    """Retrieve the first 5 rows from the dataset."""
    return data.head(5).to_dict(orient="records")


# Get a specific row by show_id
@app.get("/shows/{show_id}", response_model=ShowData)
def get_show_by_id(show_id: str):
    """Retrieve a specific row by show_id."""
    show_data = data[data["show_id"] == show_id].to_dict(orient="records")
    if not show_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")
    return show_data[0]


# Create a new show
@app.post("/shows/", response_model=ShowData, status_code=status.HTTP_201_CREATED)
def create_show(show: ShowData):
    """Create a new show in the dataset."""
    global data
    if show.show_id in data["show_id"].values:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Show ID already exists"
        )

    new_show = show.dict()
    data = data.append(new_show, ignore_index=True)
    return show


# Update a show by show_id
@app.put("/shows/{show_id}", response_model=ShowData)
def update_show(show_id: str, updated_show: ShowData):
    """Update a show in the dataset by show_id."""
    show_data = data[data["show_id"] == show_id]
    if show_data.empty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Show not found")

    data.loc[data["show_id"] == show_id] = updated_show.dict()
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
