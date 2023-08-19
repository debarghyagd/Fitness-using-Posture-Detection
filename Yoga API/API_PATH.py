from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from Yoga_Pose_Correction import Yoga_Pose_Correction

app = Flask(__name__)

api = Api(app)
    
api.add_resource(Yoga_Pose_Correction, '/')

if __name__ == '__main__':
  app.run(debug = True)