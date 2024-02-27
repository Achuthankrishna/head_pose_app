import time
import cv2
def record_response(question, response):
    with open("./interaction.txt", "a") as file:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        file.write(f"Question: {question}\n")
        file.write(f"Response: {response}\n")
        file.write(f"Time: {timestamp}\n\n")

def save_video(frames, filename):


def record_video(cap, stframe, duration=3):