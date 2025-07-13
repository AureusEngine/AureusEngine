import streamlit as st
from modules.ui_controls import display_ui
from modules.session_manager import initialize_session
from modules.utils.firebase_utils import initialize_firebase

# Set Streamlit page config
st.set_page_config(page_title="Aureus Engine", layout="centered")

# Initialize Firebase and session
initialize_firebase()
initialize_session()

# Display the user interface
display_ui()
