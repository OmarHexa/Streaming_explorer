from typing import Optional

from pydantic import BaseModel


# Define Pydantic model for the dataset
class ShowSchema(BaseModel):
    """Schema for all tables in the database.

    Used for Pydantic validation
    """

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
