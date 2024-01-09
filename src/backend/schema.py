from typing import Dict, List, Optional

from pydantic import BaseModel, validator


# Define Pydantic model for the dataset
class ShowSchema(BaseModel):
    show_id: str
    type: str
    title: str
    director: Optional[str] = None
    cast: Optional[str] = None
    country: Optional[str] = None
    date_added: Optional[str] = None
    release_year: Optional[int] = None
    rating: Optional[str] = None
    duration: Optional[str] = None
    listed_in: Optional[str] = None
    description: Optional[str] = None
