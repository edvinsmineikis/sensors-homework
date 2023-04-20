from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
import json
import os

app = Flask('sensorApp')
app.config['JSON_AS_ASCII'] = False
CORS(app)
api = Api(app)


class Metrics(Resource):
    def get(self):
        with open('data/metrics.json', encoding='utf-8') as file:
            json_data = json.load(file)
        return json_data, 200

class Sensors(Resource):
    def get(self):
        with open('data/sensors.json', encoding='utf-8') as file:
            json_data = json.load(file)
        return json_data, 200

class SensorTypes(Resource):
    def get(self):
        with open('data/sensorTypes.json', encoding='utf-8') as file:
            json_data = json.load(file)
        return json_data, 200

api.add_resource(Metrics, '/metrics.json')
api.add_resource(Sensors, '/sensors.json')
api.add_resource(SensorTypes, '/sensorTypes.json')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 
