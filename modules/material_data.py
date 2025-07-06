import streamlit as st

QUALITY_LABELS = ["P", "C", "R", "X", "E", "Y"]
QUALITY_SCORES = {"P": 1, "C": 2, "R": 3, "X": 4, "E": 5, "Y": 6}

def get_material_input_fields():
    st.write("Material Quality Inputs")
    cols = st.columns(5)
    for i in range(5):
        cols[i].selectbox(f"Mat {i+1}", QUALITY_LABELS, key=f"mat_{i}")
