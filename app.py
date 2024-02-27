import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time
from utils import record_response,save_video,record_video
from detector import detect_face_movement
import keyboard
import os
import psutil
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
        
def main():
    st.title('VSTBalance - Daily Checkup')
    st.markdown(f"<h5 style='text-align: left;'>Empower your nods, unlock answers. 🤖💡</h5>",unsafe_allow_html=True)
    text_body=st.empty()
    instructions = """
    ### Instructions
    - Click start to start the application.
    - When the question pops up, press "Answer" to answer the question or "Continue" to skip.
    - When the screen pops up, follow the below GIFs to understand how to nod.
    """

    nod_yes_text = "## To nod yes, do this"
    nod_yes_gif = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbjI0ZDA3emc5eWNjczluMm8wNHB6ODZnYmwwc3RmOHZkcjQ1eXFvcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/WoaeuzCFZ1TRsmwf1t/giphy.gif"
    
    nod_no_text = "## To nod no, do this"
    nod_no_gif = "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdDk5MXBjeTI1N2FtdDZyZThzb2phMm9majRlcmtmb3E5aHhybzhkZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QuhgjzQ3PaWE8NiiMJ/giphy-downsized-large.gif"
    
    reanswer_info = f"<h4 style='color : red;'>If you want to reanswer, press 'Reanswer'; else, press continue to the next question.</h4>"
    text_body.markdown(instructions)
    st.markdown(reanswer_info,unsafe_allow_html=True)
    #Column for the Gifs
    
    stframe = st.empty()
    #creating sidebar to start the app using container and creating a session to track user input

    ####BUtton Containers ######
    StartBtnContainer = st.sidebar.empty()
    AnswerBtnContainer = st.sidebar.empty() # To press answer ques
    changeBtnContainer = st.sidebar.empty() #To press change ques
    ContinueBtnContainer = st.empty() #To press continue
    EndBtnContainer = st.sidebar.empty() # To press End
    ReanswerBtnContainer = st.empty() #To press reanswer

    #####################################
    #Setting deefault sidebar size
    st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 500px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
    )

    ##### Im creating text containers since there's no animation in streaamlit
    TitleContainer = st.sidebar.empty()
    ImgContainer=st.sidebar.empty()
    LicenseContainer=st.sidebar.empty()
    textContainer=st.sidebar.empty()
    qtnbtncontainer=st.sidebar.empty()
    ##########################################################################

    if 'start' not in st.session_state:
        st.session_state.start = False
    
    col1, col2, col3 = st.sidebar.columns([1,2,1])
    with col1:
        if StartBtnContainer.button("Start",type="primary",use_container_width=True):
                st.session_state.start = True



    img_b1,img_b2 = st.columns(2)
    with img_b1:
       
        st.markdown(nod_yes_text)
        st.image(nod_yes_gif,width=200)
        
        
    with img_b2:
        st.markdown(nod_no_text)
        st.image(nod_no_gif,width=200)

if __name__ == '__main__':
    main()