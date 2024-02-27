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
    # save_video(frames, f"question_{question_index + 1}_response.avi")
    while response=="Undetermined":
        #Need to restart loop
        warn_text = st.empty()
        warn_text.warning("Response is undetermined. Please try again.")
        time.sleep(0.5)
        warn_text.empty()
        info_text.info("Recording 3-second video clip...")
        frames = record_video(cap, stframe, duration=3)
        info_text.info("Video clip recorded successfully.")
        info_text.empty()  # Clear the info message

        response = detect_face_movement(frames, question, stframe)
        save_video(frames, f"question_{question_index + 1}_response.avi")
    while response=="Restart":
        warn_text = st.empty()
        warn_text.warning("Face is not visible clearly! Please come close to the camera")
        time.sleep(1)
        warn_text.empty()
        info_text.info("Recording 3-second video clip...")
        frames = record_video(cap, stframe, duration=3)
        info_text.info("Video clip recorded successfully.")
        info_text.empty()  # Clear the info message

        response = detect_face_movement(frames, question, stframe)
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
##Function to terminate program
def terminate():
    st.empty()

    st.title("Please close the browser window to quit the app.")
    time.sleep(4)
    keyboard.press_and_release('ctrl+w')
    # Terminate streamlit python process
    pid = os.getpid()
    p = psutil.Process(pid)
    p.terminate()
    st.stop()

#Handle end of list : To prompt user to quit app or use again
def handle_eol(nextQueInd):
    if nextQueInd == len(questions):
        print("This loop")
        st.markdown("<h2 style='color: white;> All Questions Have been Answered </h2> ",unsafe_allow_html=True)
        st.markdown("<h2 style='color: white;>Do you want to Quit or Restart? </h2> ",unsafe_allow_html=True)
        col3,col4=st.columns(2)
        with col3:
            if st.button("Quit"):
                terminate()
        with col4:
            if st.button("Restart"):
                nextQueInd=0
                st.session_state.current_question_index = 0
                print("lauda", st.session_state.current_question_index)
                st.session_state.show_next_step_button = False
                st.empty()
                # Re-run the main function to restart the application
                main()
    return st.session_state.current_question_index
#To hide texts and turn reanswe state true 
def show_hide():
    st.empty()
    st.session_state.reanswer = True
    st.session_state.show_next_step_button = False

def contd_handle():
    nextQueInd = st.session_state.current_question_index+1
    if nextQueInd >= len(questions):
        st.markdown("<h2 style='color: white;> All Questions Have been Answered </h2> ",unsafe_allow_html=True)
        st.markdown("<h2 style='color: white;>Do you want to Quit or Restart? </h2> ",unsafe_allow_html=True)
        col3,col4=st.columns(2)
        with col3:
            if st.button("Quit"):
                terminate()
        with col4:
            if st.button("Restart"):
                nextQueInd=0
    nextQueInd = st.session_state.current_question_index+1
    st.session_state.current_question_index = nextQueInd
    st.session_state.show_next_step_button = False

def main():
    st.title('VSTBalance - Daily Checkup')
    st.markdown(f"<h5 style='text-align: left;'>Empower your nods, unlock answers. 🤖💡</h5>",unsafe_allow_html=True)
    text_body=st.empty()
    reanswer_info_text=st.empty()
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
    
    reanswer_info = f"<h4 style='color : White;'>If you want to reanswer, press 'Reanswer'. Else, press continue to the next question.</h4>"
    text_body.markdown(instructions)
    reanswer_info_text.markdown(reanswer_info,unsafe_allow_html=True)
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
    #Create Logo in Sidebar
    st.session_state.title="VSTBalance - Daily Checkup"
    st.session_state.img=f'<img src = "https://www.virtusense.ai/hubfs/Site%20content/Imported_Blog_Media/Logo-bar-black-768x127.png"  style="position: absolute; top: 55px; left: 10px; width: 400px;">'
    st.session_state.license="""
        <div style="position: fixed; bottom: 10px; left: 15%; align: center; transform: translateX(-50%); background-color: #333; padding: 10px; border-top: 1px solid #555; text-align: center;">
            <p style="margin: 0; color: #fff;">© 2024 AchuthanKrishna. All rights reserved.</p>
        </div>
        """
    

    ######SESSION STATES #########
    if 'start' not in st.session_state:
        st.session_state.start = False
    if 'quit' not in st.session_state: #For quit
        st.session_state.quit = False
    if 'current_question' not in st.session_state: #current ques is first
        st.session_state.current_question = questions[0]
    if 'current_question_index' not in st.session_state: #start from 0
        st.session_state.current_question_index = 0
    if "change_ques"not in st.session_state:
        st.session_state.change_que = False
    if 'reanswer' not in st.session_state:
        st.session_state.reanswer = False
    if 'show_next_step_button' not in st.session_state:
        st.session_state.show_next_step_button = False
    ########################################
    col1, col2, col3 = st.sidebar.columns([1,2,1])
    with col1:
        if StartBtnContainer.button("Start",type="primary",use_container_width=True):
                st.session_state.start = True
    #Quit to exit app
    with col2:

        if qtnbtncontainer.button("Quit App",type="primary",use_container_width=True):
                    st.session_state.quit=True
    if st.session_state.quit:
        StartBtnContainer.empty()
        qtnbtncontainer.empty()
        text_body.empty()
        st.empty()

        st.title("Please close the browser window to quit the app.")
        time.sleep(4)
        keyboard.press_and_release('ctrl+w')
        # Terminate streamlit python process
        pid = os.getpid()
        p = psutil.Process(pid)
        p.terminate()
        st.stop()
    
    #If pressed Start
    if st.session_state.start:
        text_body.empty()
        StartBtnContainer.empty()
        st.session_state.img = " "

        st.session_state.title="Questions"
        cap = cv2.VideoCapture(0)
        st.sidebar.empty()
        container = st.sidebar.container() #Check status of sidebar
        ans_que = st.sidebar.button(f"Answer Question",key="ans_que") #answer Question button 
      
        change_que = st.sidebar.button(f"Change Question") #Change Ques
        if change_que : 
            nextQueInd = (st.session_state.current_question_index+1)
            print(len(questions))
            print(nextQueInd)
            st.session_state.current_question_index = nextQueInd
            if nextQueInd==len(questions):
                reanswer_info_text.empty()
                nextQueInda=handle_eol(nextQueInd)
                st.session_state.current_question_index=0
            
            print(st.session_state.current_question_index)
            container.empty()
        else :
            container.empty()
        if ans_que:
            text_body.empty()
            countdown_and_answer(cap, stframe, st.session_state.current_question_index, st.session_state.current_question)
            st.session_state.show_next_step_button = True
        

        #If user wants to reanswer
        if st.session_state.reanswer :
            text_body.empty()
            countdown_and_answer(cap, stframe, st.session_state.current_question_index, st.session_state.current_question)
            st.session_state.reanswer = False
            st.session_state.show_next_step_button = True

        if st.session_state.show_next_step_button:
            
            reans_question = ReanswerBtnContainer.button("Reanswer",on_click=show_hide)
        
        if st.session_state.show_next_step_button:
            continue_question = ContinueBtnContainer.button("Continue",on_click=contd_handle)


        prompt_question(st.session_state.current_question_index,container)




    TitleContainer.title(st.session_state.title)
    ImgContainer.markdown(st.session_state.img, unsafe_allow_html=True,)
    LicenseContainer.markdown(st.session_state.license, unsafe_allow_html=True,)

    img_b1,img_b2 = st.columns(2)
    with img_b1:
       
        st.markdown(nod_yes_text)
        st.image(nod_yes_gif,width=200)
        
        
    with img_b2:
        st.markdown(nod_no_text)
        st.image(nod_no_gif,width=200)

    ##Primary Button Styling
    st.markdown("""
    <style>
    button[kind="primary"] {
    background: orange;
    position: absolute;
    top: 300px; left: 0px;
    text-decoration: none;
    cursor: pointer;
    border: none !important;

    }
                
    </style>""", unsafe_allow_html=True)

if __name__ == '__main__':
    main()