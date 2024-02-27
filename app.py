import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time
questions = [
    "Can technology solve all of humanity’s problems?",
    "Is climate change a significant threat to the planet?",
    "Should genetically modified organisms (GMOs) be banned?",
    "Is social media harmful to society?",
    "Should recreational marijuana be legalized?",
    "Is online learning as effective as in-person learning?",
    "Should the minimum wage be raised?",
    "Is space exploration worth the cost?",
    "Should voting be made mandatory?",
    "Is artificial intelligence dangerous?"
]
def set_default_dark_theme():
    theme = """
    <style>
    [data-testid="stHorizontalBlock"] .stDataFrame {
        color: black;
    }
    </style>
    """
    st.markdown(theme, unsafe_allow_html=True)

set_default_dark_theme()
