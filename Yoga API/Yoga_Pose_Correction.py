from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import cv2
import json
import numpy as np
from Pose_Detection import Pose_Detection

class Yoga_Pose_Correction(Resource):
    def get(self):
        return jsonify({'message': 'hello world'})
    
    def post(self):          
        data = request.get_json()  
        self.image=np.array(data["Image"], dtype=np.uint8)
        self.pose=data["Yoga_Pose"]
        print(type(self.image))
        print(self.image.shape)
        f = open('Asan Posture Data.json')
        posture_angles = json.load(f)
        mean=posture_angles[self.pose]["mean angle"]
        std=posture_angles[self.pose]["std angle"]
        obj=Pose_Detection(self.image,mean,std)
        obj.driver()
        f.close()
        #print( obj.output_image)
        return jsonify({'Output_message':obj.output_message, 'Output_Image': obj.output_image.tolist(), 'status': 201})