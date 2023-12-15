import requests
import streamlit as st

from app.Widget import CRUDSidebarWidget, request_with_error_handling
from main import ShowData

# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000"

# Streamlit app
st.title("Netflix Shows CRUD App")

# Sidebar for user input
st.sidebar.header("User Input")


# Display all shows
if st.button("Get All Shows"):
    shows = request_with_error_handling(FASTAPI_URL, "shows/", method="get")
    if shows:
        st.write("All Shows:")
        st.dataframe(shows)
# Creates the sidebar widget
CRUDSidebarWidget(FASTAPI_URL)
