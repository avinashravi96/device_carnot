from asyncio import exceptions
from datetime import datetime
import json
from time import strftime
from urllib import response
from xml.dom import NotFoundErr
from flask import Flask, request, Response
from pydantic import ValidationError
from device import DeviceLog
from redis_om import Migrator
from redis_om.model import NotFoundError
from datetime import datetime
import pandas as pd

app = Flask(__name__)


def build_results_device(device):
    response = []
    for device in device:
        response.append(device.dict())

    return { "results": response }

@app.route("/device/new", methods=["POST"])
def create_device_log():
    try:
        print(request.json)
        new_device_log = DeviceLog(**request.json)
        new_device_log.save()
        return new_device_log.pk

    except ValidationError as e:
        print(e)
        return "Bad request.", 400

@app.route("/device/<int:id>", methods=["GET"])
def find_by_device_id(id):
    try:
        device = DeviceLog.find(
            (DeviceLog.device_fk_id == id) 
        ).all()

        if device:
            return build_results_device(device)
    except Exception as e:
        return {"error" : e}


@app.route("/device/latest_log/<int:id>", methods=["GET"])
def find_latest_log_by_device_id(id):
    try:
        res = {}
        device = DeviceLog.find(
            (DeviceLog.device_fk_id == id) 
        ).sort_by('sts').all()

        if device:
            latest_log = device[-1]
            res['device_fk_id'] = latest_log.dict()['device_fk_id']
            res['latitude'] = latest_log.dict()['latitude']
            res['longitude'] = latest_log.dict()['latitude']
            res['time_stamp'] = latest_log.dict()['time_stamp']
            res['sts'] = latest_log.dict()['sts']
            return res
        else:
            return {"No Data Available"}
    except Exception as e:
        return {"error" : e}

@app.route("/device/location/<int:id>", methods=["GET"])
def find_device_location_by_id(id):
    try:
        res = {}
        device = DeviceLog.find(
            (DeviceLog.device_fk_id == id) 
        ).sort_by('sts').all()

        if device:
            res['device_fk_id'] = device[0].dict()['device_fk_id']
            res['start_location'] = (device[0].dict()['latitude'], device[0].dict()['longitude'])
            res['end_location'] =  (device[-1].dict()['latitude'], device[-1].dict()['longitude'])
    
            return res
        else:
            return {"No Data Available"}
    except Exception as e:
        return {'error': e }
    

@app.route("/device/location/time_range/<int:id>", methods=["GET"])
def find_device_location_on_range(id):
    try:
        page = request.args.get('page',default=1,type=int)
        per_page = 50
        req_start_time = request.args.get('start_time',type=str)
        req_end_time = request.args.get('end_time', type=str)
        start_time = datetime.strptime(req_start_time,"%Y-%m-%dT%H:%M:%SZ")
        end_time = datetime.strptime(req_end_time,"%Y-%m-%dT%H:%M:%SZ")

        device = DeviceLog.find(DeviceLog.device_fk_id == id ).sort_by('sts').all()

        if device:
            out = []
            for device in device:
                item = {}
                item['device_fk_id'] = device.dict()['device_fk_id']
                item['latitude'] = device.dict()['latitude']
                item['longitude'] = device.dict()['longitude']
                item['time_stamp'] = datetime.strptime(device.dict()['time_stamp'], "%Y-%m-%dT%H:%M:%SZ")
                out.append(item)

            process_data = pd.DataFrame(out)

            filter_data = (process_data['time_stamp'] > start_time) & (process_data['time_stamp'] <= end_time)

            process_data =  process_data.loc[filter_data]

            process_data['time_stamp'] = process_data['time_stamp'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')

            end_res = process_data.to_dict('records')

            return Response(json.dumps(end_res))
        else:
            return {"No Data Available"}
    except Exception as e:
        return {'error': e }




# Create a RediSearch index for instances of the Person model.
Migrator().run()
