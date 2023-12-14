import requests
import streamlit as st

# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000"

# Streamlit app
st.title("Netflix Shows CRUD App")

# Sidebar for user input
st.sidebar.header("User Input")

# Input for show_id
show_id_input = st.sidebar.text_input("Enter show_id for specific show:")

# Display all shows
if st.button("Get All Shows"):
    try:
        # Set a timeout (e.g., 5 seconds)
        response = requests.get(f"{FASTAPI_URL}/shows/", timeout=5)
        shows = response.json()
        st.write("All Shows:")
        st.write(shows)
    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")


# Display specific show by show_id
if show_id_input and st.button("Get Show by ID"):
    try:
        response = requests.get(f"{FASTAPI_URL}/shows/{show_id_input}", timeout=5)
        show = response.json()
        st.write(f"Show with show_id {show_id_input}:")
        st.write(show)
    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
# Create a new show
st.sidebar.header("Create New Show")
new_show = {
    "show_id": st.sidebar.text_input("Show ID:"),
    "type": st.sidebar.text_input("Type:"),
    "title": st.sidebar.text_input("Title:"),
    # "director": st.sidebar.text_input("Director:"),
    # "cast": st.sidebar.text_input("Cast:"),
    # "country": st.sidebar.text_input("Country:"),
    "release_year": st.sidebar.text_input("Released year:"),
    # "rating": st.sidebar.text_input("Rating:"),
}
if st.sidebar.button("Create Show"):
    try:
        response = requests.post(f"{FASTAPI_URL}/shows/", json=new_show, timeout=5)
        created_show = response.json()
        st.write("Created Show:")
        st.write(created_show)
    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")

# Update a show by show_id
st.sidebar.header("Update Show by ID")
updated_show = {
    "type": st.sidebar.text_input("Updated Type:"),
    "title": st.sidebar.text_input("Updated Title:"),
    # ... Add more input fields for other attributes
}
if show_id_input and st.sidebar.button("Update Show"):
    try:
        response = requests.put(
            f"{FASTAPI_URL}/shows/{show_id_input}", json=updated_show, timeout=5
        )
        updated_show_response = response.json()
        st.write("Updated Show:")
        st.write(updated_show_response)
    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")

# Delete a show by show_id
if show_id_input and st.sidebar.button("Delete Show"):
    try:
        response = requests.delete(f"{FASTAPI_URL}/shows/{show_id_input}", timeout=5)
        deleted_show = response.json()
        st.write("Deleted Show:")
        st.write(deleted_show)
    except requests.exceptions.Timeout:
        st.error("The request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
