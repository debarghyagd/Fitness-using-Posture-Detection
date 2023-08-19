import os
import json
import cv2
import mediapipe as mp
import numpy as np


class Pose_Detection:
    def __init__(self, img, mean, std):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.yoga_pose = img
        self.co_ordinates = []
        self.angles_mapping = dict()
        self.results = None
        self.mean = mean
        self.std = std
        self.heads = [
            'Head Angle',
            'Left-Elbow Angle',
            'Right-Elbow Angle',
            'Left-Shoulder Angle',
            'Right-Shoulder Angle',
            'Left-Hip Angle',
            'Right-Hip Angle',
            'Left-Knee Angle',
            'Right-Knee Angle',
            'Left-Ankle Angle',
            'Right-Ankle Angle'
        ]

    def estimate_position(self):
        with self.mp_pose.Pose(min_detection_confidence=0.0, min_tracking_confidence=0.0, model_complexity=1) as pose:
            image = cv2.cvtColor(self.yoga_pose, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            # Make detection
            self.results = pose.process(image)

    def fill_coordinates(self):
        for lndmrk, i in zip(self.mp_pose.PoseLandmark, list(self.results.pose_landmarks.landmark)):
            ind = str(lndmrk).index('.')
            points = {
                "feature": str(lndmrk)[ind+1:],
                "x": i.x,
                "y": i.y,
                "z": i.z,
                "As-Tuple": [i.x, i.y, i.z]
            }
            self.co_ordinates.append(points)

    def calculate_angle(self, a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
            np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)

        if angle > 180.0:
            angle = 360-angle

        return angle

    def determine_angles(self):
        neck_point = [(self.co_ordinates[12]["x"]+self.co_ordinates[11]["x"])/2, (self.co_ordinates[12]
                                                                                  ["y"]+self.co_ordinates[11]["y"])/2, (self.co_ordinates[12]["z"]+self.co_ordinates[11]["z"])/2]
        self.angles_mapping = {'Head': self.calculate_angle(self.co_ordinates[0]["As-Tuple"], neck_point, self.co_ordinates[11]["As-Tuple"]),
                               'Left-Elbow': self.calculate_angle(self.co_ordinates[16]["As-Tuple"], self.co_ordinates[14]["As-Tuple"], self.co_ordinates[12]["As-Tuple"]),
                               'Right-Elbow': self.calculate_angle(self.co_ordinates[15]["As-Tuple"], self.co_ordinates[13]["As-Tuple"], self.co_ordinates[11]["As-Tuple"]),
                               'Left-Shoulder': self.calculate_angle(self.co_ordinates[24]["As-Tuple"], self.co_ordinates[12]["As-Tuple"], self.co_ordinates[14]["As-Tuple"]),
                               'Right-Shoulder': self.calculate_angle(self.co_ordinates[23]["As-Tuple"], self.co_ordinates[11]["As-Tuple"], self.co_ordinates[13]["As-Tuple"]),
                               'Left-Hip': self.calculate_angle(self.co_ordinates[12]["As-Tuple"], self.co_ordinates[24]["As-Tuple"], self.co_ordinates[26]["As-Tuple"]),
                               'Right-Hip': self.calculate_angle(self.co_ordinates[11]["As-Tuple"], self.co_ordinates[23]["As-Tuple"], self.co_ordinates[25]["As-Tuple"]),
                               'Left-Knee': self.calculate_angle(self.co_ordinates[24]["As-Tuple"], self.co_ordinates[26]["As-Tuple"], self.co_ordinates[28]["As-Tuple"]),
                               'Right-Knee': self.calculate_angle(self.co_ordinates[23]["As-Tuple"], self.co_ordinates[25]["As-Tuple"], self.co_ordinates[27]["As-Tuple"]),
                               'Left-Ankle': self.calculate_angle(self.co_ordinates[26]["As-Tuple"], self.co_ordinates[28]["As-Tuple"], self.co_ordinates[32]["As-Tuple"]),
                               'Right-Ankle': self.calculate_angle(self.co_ordinates[25]["As-Tuple"], self.co_ordinates[27]["As-Tuple"], self.co_ordinates[31]["As-Tuple"])}

    def driver(self):
        self.estimate_position()
        self.fill_coordinates()
        self.determine_angles()
        self.compare()
        self.display()

    def compare(self):
        message = "Perfect!"
        self.accuracy = 0
        aggregate = []
        self.heads.reverse()
        for i in self.heads:
            acc_ratio = None
            if self.angles_mapping[i[:-6]] < self.mean[i]-self.std[i]:
                message = "Increase your "+i+"."
                acc_ratio = 2 * \
                    self.angles_mapping[i[:-6]]/(2*self.mean[i]-self.std[i])
            elif self.angles_mapping[i[:-6]] > self.mean[i]+self.std[i]:
                message = "Decrease your "+i+"."
                acc_ratio = 2 * \
                    self.angles_mapping[i[:-6]]/(2*self.mean[i]+self.std[i])
            else:
                acc_ratio = self.angles_mapping[i[:-6]]/self.mean[i]
            if acc_ratio > 1:
                acc_ratio = 1-(acc_ratio-1)
            aggregate.append(acc_ratio)
        self.accuracy = 100*sum(aggregate)/len(self.heads)
        self.output_message = message

    def display(self):
        image = self.yoga_pose
        colourR = (0, 0, 245)
        colourG = (0, 245, 0)
        colour = None
        if self.accuracy < 80:
            colour = colourR
        else:
            colour = colourG
        self.mp_drawing.draw_landmarks(image, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                       self.mp_drawing.DrawingSpec(
                                           color=(245, 0, 0), thickness=3, circle_radius=3),
                                       self.mp_drawing.DrawingSpec(
                                           color=colour, thickness=3, circle_radius=3)
                                       )
        self.output_image = image
