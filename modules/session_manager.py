import streamlit as st
from modules.session_tracker import SessionTracker
from modules.utils.firebase_utils import upload_session_data, retrieve_session_data

DEFAULT_USER = "default"

def initialize_session(user_id=DEFAULT_USER):
    if "tracker" not in st.session_state:
        tracker = SessionTracker()
        tracker.switch_user(user_id)
        stored_data = retrieve_session_data(user_id=user_id)
        if stored_data:
            for result in stored_data:
                tracker.add_result(result)
        st.session_state.tracker = tracker
        st.session_state.user_id = user_id

def handle_result_submission(result):
    if "tracker" in st.session_state:
        tracker = st.session_state.tracker
        tracker.add_result(result)
        user_id = st.session_state.get("user_id", DEFAULT_USER)
        upload_session_data(user_id=user_id, session_data=tracker.get_session_results())