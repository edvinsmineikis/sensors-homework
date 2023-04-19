from flask import Flask
from flask_restful import Resource, Api, reqparse
import json

app = Flask('sensorApp')
api = Api(app)

class Metrics(Resource):
    def get(self):
        with open('data/metrics.json') as file:
            json_data = json.load(file)
        return json_data, 200

class Sensors(Resource):
    def get(self):
        with open('data/sensors.json') as file:
            json_data = json.load(file)
        return json_data, 200

class SensorTypes(Resource):
    def get(self):
        with open('data/sensorTypes.json') as file:
            json_data = json.load(file)
        return json_data, 200

api.add_resource(Metrics, '/metrics.json')
api.add_resource(Sensors, '/sensors.json')
api.add_resource(SensorTypes, '/sensorTypes.json')

#with open('data/sensors.json') as file:
#    json_data = json.load(file)
#print(json_data)
#exit()

if __name__ == '__main__':
    app.run()
