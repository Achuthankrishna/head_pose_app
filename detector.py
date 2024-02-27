import cv2
import mediapipe as mp
import time
import torch
import numpy as np
#FaceMesh Detction
mp_f_mesh=mp.solutions.face_mesh
drawing=mp.solutions.drawing_utils
drawspec=drawing.DrawingSpec(thickness=1,circle_radius=1)

# Creating function for detection 

def detect_face_movement(frames, question, stframe):
    motion_history=[]
    start_time=time.time()
    with mp_f_mesh.FaceMesh(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
        # Iterate over each frame in the list
        for frame in frames:  
            img_h, img_w, img_c = frame.shape
            face_3d = []
            face_2d = []
            results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    for idx, lm in enumerate(face_landmarks.landmark):
                         #CHoosing landmakrs - Nose (official mediapipe documentation :https://storage.googleapis.com/mediapipe-assets/Model%20Card%20Blendshape%20V2.pdf )
                          if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                            if idx == 1:
                                nose_2d = (lm.x * img_w, lm.y * img_h)
                                nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                            x, y = int(lm.x * img_w), int(lm.y * img_h)

                           
                            face_2d.append([x, y])
                            face_3d.append([x, y, lm.z])
                            #get as np array
                    if not face_2d or not face_3d:
                        continue
                    face_2d = np.array(face_2d, dtype=np.float64)
                    face_3d = np.array(face_3d, dtype=np.float64)
                    flen=1 * img_w
                    #generate camera matrix
                    cam_matrix = np.array([[flen, 0, img_h / 2],
                                [0, flen, img_w / 2],
                                [0, 0, 1]])
                    dist_mat=np.zeros((4,1),dtype=np.float64)
                    #From the points obtained we are using pnp solver to ger respective pose
                    suc,rot,trans=cv2.solvePnP(face_3d,face_2d,cam_matrix,dist_mat)
                    #using rot mat
                    rot_mat,j=cv2.Rodrigues(rot)
                    #getting angles from rot mat
                    angles,mtxR, mtxQ, Qx, Qy, Qz=cv2.RQDecomp3x3(rot_mat)
                    x = angles[0] * 360
                    y = angles[1] * 360
                    z = angles[2] * 360
                    #Pose estimation using angles 
                    if y < -7.5:
                        motion_history.append("Looking Left")
                    elif y > 7.5:
                        motion_history.append("Looking Right")
                    elif x < -6.5:
                        motion_history.append("Looking Down")
                    elif x > 6.5:
                        motion_history.append("Looking Up")
                    else:
                        motion_history.append("Forward")
    if not motion_history:
        return "Restart"
    #get predominant motion out of all the motion happening 
    motion_counts = {motion: motion_history.count(motion) for motion in set(motion_history)}
    predominant_motion = max(motion_counts, key=motion_counts.get)
    if predominant_motion == "Looking Up" or predominant_motion == " Looking Down":
        return "Yes"
    elif predominant_motion == "Looking Left" or predominant_motion == "Looking Right":
        return "No"
    else:
        return "Undetermined"



       #assuming camera is opened
        # while cap.isOpened():
        #     succ,img=cap.read()
        #     img=cv2.cvtColor(cv2.flip(img,1),cv2.COLOR_BGR2RGB)
        #     start=time.time()
        #     im_flag=False
        #     res=f_mesh.process(img)
        #     im_flag=True
        #     img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        #     im_h,im_w,im_c=img.shape
        #     if res.multi_face_landmarks:
        #         for f in res.multi_face_landmarks:

                    # print(f)
                    
                    # fps = 1 / totalTime
            # print("FPS: ", fps)

                    # cv2.putText(image, f'FPS: {int(fps)}', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

    #                 drawing.draw_landmarks(
    #                     image=img,
    #                     landmark_list=f,
    #                     # connections=f_mesh.FACE_CONNECTIONS,
    #                     landmark_drawing_spec=drawspec,
    #                     connection_drawing_spec=drawspec)

    #         cv2.imshow('Head Pose Estimation', img)

    #         if cv2.waitKey(5) & 0xFF == 27:
    #                 break

    # cap.release()




