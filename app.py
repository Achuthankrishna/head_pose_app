import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time
from utils import record_response,save_video,record_video
from detector import detect_face_movement
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

    countdown=st.empty()
    success_text = st.empty()
    info_text = st.empty()

    #countdown for 5 seconds
    for i in range(5, 0, -1):
        countdown.markdown(f"<h1 style='text-align: center; color: yellow;'>{i}</h1>",
                                unsafe_allow_html=True)
        time.sleep(1)
    #Clear once done
    countdown.empty()
    success_text.success('You can start answering')
    time.sleep(0.5)
    #Clear
    success_text.empty()
    info_text.info("Recording 3-second video clip...")
    #Record and detect logic : We record First
    frames = record_video(cap, stframe, duration=3)
    info_text.info("Video clip recorded successfully.")
    info_text.empty()
    response = detect_face_movement(frames, question, stframe)
    question_text_container.empty()
    save_video(frames, f"question_{question_index + 1}_response.avi")

    record_response(question, response)
    if response == "Yes":
        st.sidebar.write(f"<h3 style='text-align: center; color: white;'>Your response: </h3>"
                         f"<h3 style='text-align: center; color: green;'>{response}</h3>",
                         unsafe_allow_html=True)
    else:
        st.sidebar.write(f"<h3 style='text-align: center; color: white;'>Your response: </h3>"
                         f"<h3 style='text-align: center; color: red;'>{response}</h3>",
                         unsafe_allow_html=True)