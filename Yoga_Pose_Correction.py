import os
import json
import cv2
import mediapipe as mp
import numpy as np
from Pose_Detection import Pose_Detection
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class Yoga_Pose_Correction():
    def driver(self, pose_name):
        f = open('Asan Posture Data.json')
        data = json.load(f)
        cap = cv2.VideoCapture(1)
        # Setup mediapipe instance
        with mp_pose.Pose(min_detection_confidence=0, min_tracking_confidence=0) as pose:
            while cap.isOpened():
                ret, frame = cap.read()
                # Make detection

                mean = data[pose_name]["mean angle"]
                std = data[pose_name]["std angle"]

                obj = Pose_Detection(frame, mean, std)
                obj.driver()

                cv2.imshow('Mediapipe Feed', obj.output_image)
                print(type(obj.output_image))
                print(obj.output_message + "    "+str(obj.accuracy))

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()
            return True


obj=Yoga_Pose_Correction()
obj.driver('Cobra Pose or Bhujangasana')
