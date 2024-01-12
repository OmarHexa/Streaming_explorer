import rootutils

rootutils.setup_root(__file__, indicator="pyproject.toml", pythonpath=True, cwd=True)

import streamlit as st

from src.frontend.common.components import get_show_recommendations

st.set_page_config(
    page_title="Home",
    page_icon="🎥",
)
#    menu_items={"About": "something"})

# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000"
# This removes the default menu button on the top right of the screen
st.markdown("<style>#MainMenu{visibility:hidden;}</style>", unsafe_allow_html=True)
A, B, C = st.columns((1, 2, 1))
# Streamlit app
B.title(
    ":red[Streaming Explorer]",
)
st.header("Welcome to the home page")
st.write(
    "This web app presents a comprehensive exploration of shows available on popular streaming platforms - Netflix, Amazon Prime, and Disney+.\
          Users can effortlessly navigate through a vast collection of shows, applying filters based on release year and age ratings. \
         Get insights into the dataset with our Exploratory Data Analysis results. Understand trends, distributions, and key statistics about the shows available on these platforms."
)

st.markdown(":blue[Get Show recommendation from all platform]")


get_show_recommendations(FASTAPI_URL)
