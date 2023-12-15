import requests
import streamlit as st

from main import ShowData


def updateFormWidget(options):
    """Generates a Streamlit sidebar widget for updating a show with dynamic fields.

    Parameters:
    - options (list): List of field options.

    Returns:
    dict: Dictionary containing updated field values.
    """
    if "count" not in st.session_state:
        st.session_state.count = 1

    def increase_count():
        if st.session_state.count < len(options):
            st.session_state.count += 1

    def remove_row(field_value):
        del st.session_state.input_dict[field_value]
        st.session_state.count -= 1

    if "input_dict" not in st.session_state:
        st.session_state.input_dict = {}
    with st.sidebar:
        for i in range(st.session_state.count):
            col_A, col_B, col_C = st.columns((2, 3, 1))
            field_value = col_A.selectbox("Field", options=options, key=f"Field_{i}")
            input_value = col_B.text_input("Input", key=f"Input_{i}")
            remove_button = col_C.button(
                "🗑️", on_click=remove_row, args=[field_value], key=f"remove_{i}"
            )
            st.session_state.input_dict[field_value] = input_value

        if st.session_state.count < len(options):
            st.button("Add Field :heavy_plus_sign:", on_click=increase_count)

    return st.session_state.input_dict


def request_with_error_handling(api_url, route, method="get", data=None):
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
        if method.lower() == "get":
            response = requests.get(f"{api_url}/{route}", timeout=5)
        elif method.lower() == "post":
            response = requests.post(f"{api_url}/{route}", json=data, timeout=5)
        # Add more methods (put, delete, etc.) as needed
        elif method.lower() == "put":
            response = requests.put(f"{api_url}/{route}", json=data, timeout=5)
        elif method.lower() == "delete":
            response = requests.delete(f"{api_url}/{route}", timeout=5)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")


def CRUDSidebarWidget(CRUDAPI_URL):
    """Streamlit sidebar widget for CRUD operations on a show database.

    Parameters:
    - CRUDAPI_URL (str): Base URL of the CRUD API.

    Returns:
    None
    """
    show_id_input = st.sidebar.text_input("Enter show_id for specific show:")

    # Display specific show by show_id
    if show_id_input and st.button("Get Show by ID"):
        show = request_with_error_handling(CRUDAPI_URL, f"shows/{show_id_input}")
        if show:
            st.write(f"Show with show_id {show_id_input}:")
            st.dataframe(show)

    # Create a new show
    st.sidebar.header("Create New Show")
    new_show = {
        "show_id": st.sidebar.text_input("Show ID:"),
        "type": st.sidebar.text_input("Type:"),
        "title": st.sidebar.text_input("Title:"),
        "release_year": st.sidebar.text_input("Released year:"),
    }
    if st.sidebar.button("Create Show", use_container_width=True):
        created_show = request_with_error_handling(
            CRUDAPI_URL, "shows/", method="post", data=new_show
        )
        if created_show:
            st.write("Created Show:")
            st.dataframe(created_show)

    # Update a show by id
    options = list(ShowData.__annotations__.keys())
    st.sidebar.header("Update Show by ID")
    updated_show = updateFormWidget(options=options)

    if show_id_input and st.sidebar.button("Update Show", use_container_width=True):
        updated_show = request_with_error_handling(
            CRUDAPI_URL, f"shows/{show_id_input}", "put", data=updated_show
        )
        if updated_show:
            st.write("Update show:")
            st.dataframe(updated_show)

    # Delete a show by show_id
    if show_id_input and st.sidebar.button("Delete Show", use_container_width=True):
        deleted_show = request_with_error_handling(CRUDAPI_URL, f"shows/{show_id_input}", "delete")
        if deleted_show:
            st.write("Deleted Show:")
            st.dataframe(deleted_show)
