import pandas as pd
import requests
import streamlit as st

# Define the base URL for the FastAPI server
base_url = "http://127.0.0.1:8000"

# Streamlit app
st.title("CRUD App with FastAPI and Streamlit")


# Function to make API requests
def make_request(endpoint, data=None, method="get"):
    """Make a request to the FastAPI server.

    Args:
        endpoint (str): API endpoint.
        data (dict, optional): Data to be sent in the request. Defaults to None.
        method (str, optional): HTTP method (e.g., "get", "post", "put", "delete"). Defaults to "get".

    Returns:
        dict: JSON response from the server.
    """
    url = f"{base_url}{endpoint}"
    response = getattr(requests, method)(url, json=data)
    return response.json()


# Sidebar for user input
st.sidebar.header("User Input")
name = st.sidebar.text_input("Name:")
email = st.sidebar.text_input("Email:")

# CRUD operations buttons
if st.button("Create User"):
    """Create a new user using the provided name and email."""
    user_data = {"name": name, "email": email}
    make_request("/users/", data=user_data, method="post")

if st.button("Read User"):
    """Read user information based on the provided user ID."""
    user_id = st.sidebar.number_input("User ID:")
    user_data = make_request(f"/users/{user_id}")
    st.write("User Data:", user_data)

if st.button("Update User"):
    """Update user information based on the provided user ID, name, and email."""
    user_id = st.sidebar.number_input("User ID:")
    user_data = {"name": name, "email": email}
    make_request(f"/users/{user_id}", data=user_data, method="put")

if st.button("Delete User"):
    """Delete user based on the provided user ID."""
    user_id = st.sidebar.number_input("User ID:")
    user_data = make_request(f"/users/{user_id}", method="delete")
    st.write("Deleted User Data:", user_data)

# Display all users
st.header("All Users")
all_users = make_request("/users/")
df = pd.DataFrame(all_users)
st.dataframe(df)
