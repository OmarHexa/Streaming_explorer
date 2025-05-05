import rootutils
import streamlit as st

from src.frontend.common.utils import ShowSchema

from src.frontend.common.components import (
    PlotlyPlotDisplayer,
    ShowEditorHandler,
    ShowsViewHandler,
)
rootutils.setup_root(__file__, indicator="pyproject.toml", pythonpath=True, cwd=True)

st.set_page_config(
    page_title="Disney+",
    page_icon="🏰",
)
# This removes the default menu button on the top right of the screen
st.markdown("<style>#MainMenu{visibility:hidden;}</style>", unsafe_allow_html=True)

# Streamlit app
st.title(
    "Disney+",
)

# Create a container for shows
shows_container = st.container()

# Display shows
shows_viewer = ShowsViewHandler(container=shows_container, channel="disney")
options = list(ShowSchema.__annotations__.keys())
show_editor = ShowEditorHandler(options, channel="disney")
shows_viewer.render_shows()
# # Display buttons for Create Show and Edit Show
show_editor.create_show()
show_editor.edit_show()


plot_object = PlotlyPlotDisplayer("disney")

plot_object.display_plot("yearlyShowPlot")
plot_object.display_plot("ratingPlot")
plot_object.display_plot("genresPlot")
plot_object.display_plot("countryProdPlot")
