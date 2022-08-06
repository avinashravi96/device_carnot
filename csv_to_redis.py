import pandas as pd
import requests

read_file = pd.read_csv("data/raw_data.csv")

read_file['sts'] = pd.to_datetime(read_file['sts'])

df = read_file.to_dict('records')

for item in df:
    sts = item["sts"].strftime("%d-%m-%Y %H:%M:%S.%f")
    item['sts'] = sts 

    r = requests.post('http://127.0.0.1:5000/device/new', json = item)