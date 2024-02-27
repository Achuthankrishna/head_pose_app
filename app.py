import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time
from utils import record_response,save_video,record_video
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

def prompt_question(questionInd,container):
    question = questions[questionInd]
    container.markdown(f"<h3>{question}</h3>", unsafe_allow_html=True)
#Function for creating a countdown when user presses answer question, which opens camera after 5 seconds
def countdown_and_answer(cap, stframe, question_index, question):
    print(question_index+1)
    #Print Question in H2
    question_text = f"<h2 style='color: white;font-weight: bold;'>Question {question_index+1}: {questions[question_index]}</h2>"
    #Container in streamlit is easy to manage elements instead of st.write()
    question_text_container = st.empty()  # Container for question text
    question_text_container.write(question_text, unsafe_allow_html=True)