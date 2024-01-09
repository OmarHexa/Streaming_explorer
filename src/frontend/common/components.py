from typing import Dict, List

import streamlit as st

from src.backend.schema import ShowSchema
from src.frontend.common.utils import request_with_error_handling

# Alias for session state
ss = st.session_state


class ShowsViewHandler:
    def __init__(self, container, fastapi_url: str = "http://localhost:8000", num_shows: int = 10):
        """Initializes a ShowsViewHandler instance.

        Parameters:
        - container (streamlit.container.Container): The container to display shows and buttons.
        - fastapi_url (str): The URL of the FastAPI server. Default is "http://localhost:8000".
        - num_shows (int): The number of shows to display. Default is 10.

        Example:
            # Create a Streamlit container
            my_container = st.container()

            # Initialize ShowsViewHandler
            shows_handler = ShowsViewHandler(container=my_container, fastapi_url="http://example.com/api", num_shows=10)

            # Render shows
            shows_handler.render_shows()
        """
        self.fastapi_url = fastapi_url
        if "current_showId" not in st.session_state:
            ss.current_showId = 0
        self.container = container
        self.num_shows = num_shows

    def render_shows(self):
        """Renders shows in the specified container along with next and previous buttons."""
        start_index = max(0, ss.current_showId)
        # Get shows from the API
        shows = request_with_error_handling(
            self.fastapi_url, f"shows/?index={start_index}&limit={self.num_shows}", method="get"
        )

        # Display the shows in Streamlit
        self.container.write(
            f":gray[Shows]: {ss.current_showId + 1} - {ss.current_showId + self.num_shows}"
        )
        self.container.dataframe(shows)
        self._render_buttons()

    def next_shows(self):
        """Updates the current show index to show the next set of shows."""
        ss.current_showId += self.num_shows

    def previous_shows(self):
        """Updates the current show index to show the previous set of shows."""
        if ss.current_showId > 0:
            ss.current_showId -= self.num_shows

    def _render_buttons(self):
        """Renders next and previous buttons inside the container."""
        # Display next and previous buttons inside the container
        col1, col2 = self.container.columns((7, 1), gap="small")

        with col1:
            # "Previous" button
            if st.button("⏮️ Previous", on_click=self.previous_shows):
                pass

        with col2:
            # "Next" button
            if st.button("Next ⏭️", on_click=self.next_shows):
                pass


class ShowEditorHandler:
    """A class for handling the creation and updating of shows using Streamlit forms.

    Args:
        options (List[str]): List of field options.
        url (str): URL of the FastAPI server. Default is "http://localhost:8000".

    Examples:

        # Initialize ShowEditorHandler
        options = ["title", "director", "cast", "country", "release_year"]
        show_editor_handler = ShowEditorHandler(options)

        # Display buttons for Create Show and Edit Show
        show_editor_handler.create_show()
        show_editor_handler.edit_show()
    """

    def __init__(self, options: List[str], url: str = "http://localhost:8000"):
        self.options = options
        self.url = url
        if any(key not in ss for key in ["show_create_form", "show_update_form"]):
            self._reset_session_state()

    def render_create_form(self):
        """Form to create a new show."""
        with st.form("create_form"):
            new_show = {
                f"{field}": st.text_input(f"{field.capitalize()}", placeholder="unknown")
                for field in self.options
            }
            new_show.update(
                {f"{field}": "unknown" for field in self.options if new_show[f"{field}"] == ""}
            )
            submitted = st.form_submit_button("Submit")

        if submitted:
            created_show = request_with_error_handling(
                self.url, "shows/", method="post", data=new_show
            )
            if created_show:
                st.write("New Show Created:")
                st.dataframe(created_show)

    def render_update_form(self, show_id):
        """Generates a Streamlit widget for updating a show with dynamic fields."""

        if any(key not in ss for key in ["field_count", "update_dict"]):
            ss.field_count = 1
            ss.update_dict = {}

        def increase_count():
            if ss.field_count < len(self.options):
                ss.field_count += 1

        def remove_row(field_value):
            del ss.update_dict[field_value]
            ss.field_count -= 1

        for i in range(ss.field_count):
            col_A, col_B, col_C = st.columns((2, 6, 1))
            field_value = col_A.selectbox("Field", options=self.options, key=f"Field_{i}")
            input_value = col_B.text_input("Input", key=f"Input_{i}")
            if i > 0:
                col_C.button("🗑️", on_click=remove_row, args=[field_value], key=f"remove_{i}")
            ss.update_dict[field_value] = input_value

        col1, col2, col3 = st.columns([1, 2, 1])
        if ss.field_count < len(self.options):
            col3.button("Add Field :heavy_plus_sign:", on_click=increase_count)

        if col1.button(":blue[Submit]"):
            # st.dataframe(ss.update_dict)
            updated_show = request_with_error_handling(
                self.url, f"shows/{show_id}", "put", data=ss.update_dict
            )
            if updated_show:
                st.write("Update show:")
                st.dataframe(updated_show)
        if col2.button(":red[Cancel]", on_click=self._reset_session_state):
            pass

    def create_show(self):
        """Create a new show using a form."""
        if (
            st.button("Create Show", on_click=self._select_create, use_container_width=True)
            or ss.show_create_form
        ):
            self.render_create_form()

    def edit_show(self):
        """Edit a existing show."""
        # NOTE: for design purpose we didn't initialize "edit_show". that's why we used dict get function with default
        # value as False. As soon as button is clicked it will initialize "edit_show" to true.
        if st.button("Edit Show", on_click=self._select_edit, use_container_width=True) or ss.get(
            "edit_show", False
        ):
            left, center, _ = st.columns((1, 1, 1))
            left.markdown("### Which show you would like to edit")
            text = center.empty()
            if hasattr(ss, "delete_msg"):
                show_id = text.text_input("Show ID", placeholder="s??", key="2")
                delattr(ss, "delete_msg")
                st.write(":red[Successfully deleted]")
            else:
                show_id = text.text_input("Show ID", placeholder="s??", key="1")
            if show_id:
                self.check_show_exist(show_id)
                self.update_show(show_id)
                self.delete_show(show_id)

    def check_show_exist(self, show_id):
        """Check if the show exist in database server."""
        show = request_with_error_handling(self.url, f"shows/{show_id}")
        if show:
            _, center, _ = st.columns((1, 1, 1))
            center.write(f"Current Details of the Show: :grey[{show_id.capitalize()}]:")
            center.dataframe(show)

    def update_show(self, show_id):
        """Update a show using a form."""
        _, center, _ = st.columns([1, 3, 1])

        if (
            center.button("Update Show", on_click=self._select_update, use_container_width=True)
            or ss.show_update_form
        ):
            self.render_update_form(show_id)

    def delete_show(self, show_id):
        """Delete a new show using a form."""
        _, center, _ = st.columns([1, 3, 1])

        if center.button(
            "Delete Show", on_click=self._reset_session_state, use_container_width=True
        ) or ss.get("delete_show", False):
            left, center, right = st.columns(3)
            ss.delete_show = True
            # empty space to fill in messages
            container = center.empty()

            input = container.text_input(
                "Are you sure you want to delete the item? Write delete in the box and press enter.",
                placeholder="delete",
            )
            if input == "delete":
                # st.write("show deleted")
                deleted_show = request_with_error_handling(self.url, f"shows/{show_id}", "delete")
                if deleted_show:
                    self._delete_msg()
                    st.rerun()

    def _reset_session_state(self):
        """Initialize the form state."""
        ss.show_create_form = False
        ss.show_update_form = False

        self._remove_update_form()

    def _remove_update_form(self):
        """Remove update form state."""
        if hasattr(ss, "update_dict"):
            delattr(ss, "update_dict")
        if hasattr(ss, "field_count"):
            delattr(ss, "field_count")

    def _delete_msg(self):
        ss.edit_show = True
        ss.delete_msg = True

    def _select_edit(self):
        """Select the edit show."""
        ss.show_create_form = False
        ss.show_update_form = False
        ss.delete_show = False

        self._remove_update_form()
        # only show edit panel
        ss.edit_show = True

    def _select_update(self):
        """Select the update form."""
        ss.show_create_form = False
        ss.show_update_form = True
        ss.delete_show = False

    def _select_create(self):
        """Select the create form."""
        ss.show_create_form = True
        ss.edit_show = False
        self._remove_update_form()
