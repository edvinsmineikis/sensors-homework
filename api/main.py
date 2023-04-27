from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
import json
import os

app = Flask('sensorApp')
app.config['JSON_AS_ASCII'] = False
CORS(app)
api = Api(app)

# Converts the default data to one with already selected unit, for example:
# {
#   id: 5,
#   name: 'Voltage',
#   unit: 'V'
# }
def get_metrics():
        with open('data/metrics.json', encoding='utf-8') as file:
            json_data = json.load(file)
        items = json_data['data']['items']
        for item in items:
            for unit in item['units']:
                if 'selected' in unit and unit['selected'] is True:
                    item['unit'] = unit['name']
                    item.pop('units')
        json_data = json_data['data']['items']
        return json_data

# Converts metricId shown for each sensor to actual unit name
def get_metric_name(metricId):
    metrics = get_metrics()
    for metric in metrics:
        if metric['id'] == metricId:
            return metric['name']
    else:
        raise Exception('No metrics found')

# This is mostly useful for defining headers of the table
class Metrics(Resource):
    def get(self):
        json_data = get_metrics()
        return json_data, 200

# Sensor data has flaws in it, wrong data gets removed
# Measurement type number is replaced with measurement type name to simplify frontend work
class Sensors(Resource):
    def get(self):
        with open('data/sensors.json', encoding='utf-8') as file:
            json_data = json.load(file)
        response = self.add_sensor_types(json_data)
        response = self.remove_corrupt_items(json_data)
        response = self.update_measurement_keys(json_data)
        return response, 200
    
    def add_sensor_types(self, sensors_json):
        sensors_to_remove = []
        with open('data/sensorTypes.json', encoding='utf-8') as file:
            sensorTypes_json = json.load(file)
        for sensor in sensors_json:
            try:
                s_type = str(sensors_json[sensor]['type'])
                s_variant = str(sensors_json[sensor]['variant'])
                sensors_json[sensor]['typeName'] = sensorTypes_json[s_type][s_variant]['name']
                sensors_json[sensor].pop('type')
                sensors_json[sensor].pop('variant')
            except:
                sensors_to_remove.append(sensor)
        for sensor in sensors_to_remove:
            sensors_json.pop(sensor)
        return sensors_json

    def remove_corrupt_items(self, json_data):
        items_to_remove = []
        for item in json_data:
            try:
                if not json_data[item]['metrics'] or not json_data[item]['name']:
                    items_to_remove.append(item)
            except:
                items_to_remove.append(item)
        for item in items_to_remove:
            json_data.pop(item)
        return json_data

    def update_measurement_keys(self, json_data):
        for sensor in json_data:
            metrics = json_data[sensor]['metrics']
            new_metrics = {}
            for metric in metrics:
                unitName = get_metric_name(metric)
                new_metrics[unitName] = metrics[metric]['v']
            json_data[sensor]['metrics'] = new_metrics
        return json_data
        
api.add_resource(Metrics, '/metrics.json')
api.add_resource(Sensors, '/sensors.json')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 
