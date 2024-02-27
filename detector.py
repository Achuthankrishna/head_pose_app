import cv2
import mediapipe as mp
import time
import torch

#FaceMesh Detction
f_mesh=mp.solutions.face_mesh
drawing=mp.solutions.drawing_utils
drawspec=drawing.DrawingSpec(thickness=0,circle_radius=1)

#Creating function for detection 

def detect_face_movement(frames, question, stframe):
    cap=cv2.VideoCapture(0)
    with f_mesh.FaceMesh(min_detection_confidence=0.75,min_tracking_confidence=0.75)as f_mesh:
        while cap.isOpened():
            succ,img=cap.read()
            img=cv2.cvtColor(cv2.flip(img,1),cv2.COLOR_BGR2RGB)
            start=time.time()
            im_flag=False
            res=f_mesh.process(img)
            im_flag=True
            img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
            im_h,im_w,im_c=img.shape
            if res.multi_face_landmarks:
                for f in res.multi_face_landmarks:

                    # print(f)
                    
                    # fps = 1 / totalTime
            # print("FPS: ", fps)

                    # cv2.putText(image, f'FPS: {int(fps)}', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

                    drawing.draw_landmarks(
                        image=img,
                        landmark_list=f,
                        # connections=f_mesh.FACE_CONNECTIONS,
                        landmark_drawing_spec=drawspec,
                        connection_drawing_spec=drawspec)

            cv2.imshow('Head Pose Estimation', img)

            if cv2.waitKey(5) & 0xFF == 27:
                    break

    cap.release()




