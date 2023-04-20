from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
import json

app = Flask('sensorApp')
app.config['JSON_AS_ASCII'] = False
CORS(app)
api = Api(app)


class Metrics(Resource):
    def get(self):
        with open('api/data/metrics.json', encoding='utf-8') as file:
            json_data = json.load(file)
        return json_data, 200

class Sensors(Resource):
    def get(self):
        with open('api/data/sensors.json', encoding='utf-8') as file:
            json_data = json.load(file)
        return json_data, 200

class SensorTypes(Resource):
    def get(self):
        with open('api/data/sensorTypes.json', encoding='utf-8') as file:
            json_data = json.load(file)
        return json_data, 200

api.add_resource(Metrics, '/metrics.json')
api.add_resource(Sensors, '/sensors.json')
api.add_resource(SensorTypes, '/sensorTypes.json')

if __name__ == '__main__':
    app.run()