import pandas as pd
import rootutils
import streamlit as st

rootutils.setup_root(__file__, indicator="pyproject.toml", pythonpath=True, cwd=True)
from src.backend.schema import ShowSchema
from src.frontend.common.components import (
    PlotlyPlotDisplayer,
    ShowEditorHandler,
    ShowsViewHandler,
)

st.set_page_config(
    page_title="Amazon Prime",
    page_icon="📦",
)
# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000"
# This removes the default menu button on the top right of the screen
st.markdown("<style>#MainMenu{visibility:hidden;}</style>", unsafe_allow_html=True)

# Streamlit app
st.title(
    ":blue[Amazon Prime]",
)
# Create a container for shows
shows_container = st.container()

# Display shows
shows_viewer = ShowsViewHandler(container=shows_container, channel="amazon")
options = list(ShowSchema.__annotations__.keys())
show_editor = ShowEditorHandler(options, channel="amazon")
shows_viewer.render_shows()
# # Display buttons for Create Show and Edit Show
show_editor.create_show()
show_editor.edit_show()

plot_object = PlotlyPlotDisplayer("amazon")

plot_object.display_plot("yearlyShowPlot")
plot_object.display_plot("ratingPlot")
plot_object.display_plot("genresPlot")
plot_object.display_plot("countryProdPlot")
