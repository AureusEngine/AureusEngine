import pandas as pd
import plotly.express as px
import streamlit as st

def display_prediction(prediction, confidence, show_confidence=True):
    style = "font-size: 32px; font-weight: bold;"
    if confidence >= 0.85:
        color = "green" if prediction == "W" else "red"
        style += f" border: 3px solid {color}; padding: 10px;"
    st.markdown(f"<div style='{style}'>Next Result Prediction: {prediction}</div>", unsafe_allow_html=True)
    if show_confidence:
        st.markdown(f"<div style='font-size: 16px;'>Confidence: {confidence:.2%}</div>", unsafe_allow_html=True)

def plot_distribution(history_df):
    fig = px.histogram(history_df, x='Result', title='Crafting Results Distribution')
    st.plotly_chart(fig)