import time
import cv2
def record_response(question, response):
    with open("./interaction.txt", "a") as file:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        file.write(f"Question: {question}\n")
        file.write(f"Response: {response}\n")
        file.write(f"Time: {timestamp}\n\n")

def save_video(frames, filename):
    if len(frames) == 0:
        print("No frames to save.")
        return
    frame_h,frame_w,_=frames.shape[0]
    output=cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'DIVX'), 30, (frame_w, frame_h))
    for frame in frames:
        output.write(frame)

    output.release()
    print(f"Video saved as {filename}")


def record_video(cap, stframe, duration=3):