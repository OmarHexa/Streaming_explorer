from typing import Dict

from typing import Optional

from pydantic import BaseModel
import requests
import streamlit as st


def request_with_error_handling(
    api_url: str, route: str, method: str = "get", data: Dict = None
) -> dict:
    """Makes an HTTP request to the specified API endpoint with error handling.

    Parameters:
    - api_url (str): Base URL of the API.
    - route (str): API endpoint route.
    - method (str): HTTP method (default is "get").
    - data (dict): JSON data for the request (default is None).

    Returns:
    dict: JSON response from the API.
    """

    try:
        if method.lower() not in ["get", "post", "put", "delete"]:
            raise ValueError(
                f"Invalid HTTP method '{method}'. Supported methods are 'get', 'post', 'put', and 'delete'."
            )

        response = requests.request(method.lower(), f"{api_url}/{route}", timeout=5, json=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()

    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")


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