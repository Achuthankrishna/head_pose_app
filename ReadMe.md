# VirtuSense Head-Nod Assistant - 🤖

## Project Overview
Countless of elderly people need constant attention to their needs. It is mighty challenging for them to engage in day to day conversations, and
call for help. The VirtuSense Head-Nod Assistant is an AI powered personal assistant that keeps patients in check of their needs and necessities and also offer a peice of entertainment. An AI-powered web app , designed to interact with users through a single thought-provoking question that expects a "Yes" or "No" head-nod..

##  Tools Used
<img src="./images/image.png" alt="Image 1" width="200" height="200"/> <img src="./images/image-1.png" alt="Image 2" width="200"/> <img src="./images/image-2.png" alt="Image 3" width="200" height="200"/> <img src="./images/image-3.png" alt="Image 4" width="200"/>

## Package Structure

The head-nod application is structured into following components: 
- `images/` : Folder containing deployment use cases
- `app.py`: The main Streamlit application.
- `Dockerfile`: Instructions for Docker to build the application image.
- `detetctor.py`:  The main detector algorithm using mediapipe and OpenCV.
- `utils.py` : File consisting record and save video utlity for the application.
- `interaction.txt`: File for interaction storage with time stamp.
- `video_logs/`: Folder containing video_log files.
- `open_browser.sh`: The bash file for opening web browswer.
- `open_cam.sh`: The bash file for opening camera.

## Dependencies 
For the application, you are required to have docker installed. To install docker, follow the instructions given on the link [!Install](https://docs.docker.com/desktop/install/linux-install/)