import streamlit as st
from modules.prediction_engine import predict_next_outcome
from modules.output_handler import display_prediction
from modules.material_data import get_material_input_fields
from modules.session_manager import handle_result_submission
from modules.utils.firebase_utils import upload_user_pattern

def display_ui():
    st.title("Aureus Engine Pattern Predictor")

    # Use dummy prediction call for now (replace with actual logic later)
    prediction, confidence = "W", 0.87
    display_prediction(prediction, confidence)

    # Crafted Result Input
    st.subheader("Enter Crafted Result")
    cols = st.columns([1, 1, 1])
    with cols[0]:
        if st.button("✅ W", key="win"):
            handle_result_submission("W")
    with cols[1]:
        if st.button("❌ L", key="loss"):
            handle_result_submission("L")
    with cols[2]:
        if st.button("➖ M", key="mid"):
            st.session_state["awaiting_mid_input"] = True

    if st.session_state.get("awaiting_mid_input", False):
        quality = st.selectbox("Select Crafted Quality", ["P", "C", "R", "X", "E", "Y"], key="mid_quality")
        if st.button("Submit Quality", key="submit_quality"):
            handle_result_submission(quality)
            st.session_state["awaiting_mid_input"] = False

    st.subheader("Crafting Materials")
    get_material_input_fields()

    st.subheader("Submit Known Pattern")
    user_pattern = st.text_input("Enter pattern (e.g. WLWML)")
    if st.button("Submit Pattern"):
        upload_user_pattern(user_pattern)
        st.success("Pattern submitted!")