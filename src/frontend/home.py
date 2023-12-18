import rootutils

rootutils.setup_root(__file__, indicator="pyproject.toml", pythonpath=True, cwd=True)

import streamlit as st

from src.frontend.common.Widget import CRUDSidebarWidget, fetch_and_display_shows

# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000"

# Streamlit app
st.title(":red[Netflix Shows CRUD App]")

fetch_and_display_shows(FASTAPI_URL)


# Creates the sidebar widget
CRUDSidebarWidget(FASTAPI_URL)
