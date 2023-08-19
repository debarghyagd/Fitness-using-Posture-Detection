import os
import json
import cv2
import mediapipe as mp
import numpy as np
import pygame
import requests
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose_name="Boat Pose or Paripurna Navasana"
url="http://127.0.0.1:5000"

cap = cv2.VideoCapture(0)
## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        #print(frame.tolist())

        data={
            "Yoga_Pose": pose_name,
            "Image":frame.tolist()
        }
        response=requests.post(url, json=data).json()
        
        #print(response.json())
        
        image=np.array(response['Output_Image'], dtype=np.uint8)
        
        cv2.imshow('Mediapipe Feed', image)
        print(response['Output_message'])

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()