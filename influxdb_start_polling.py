import time
import os
import argparse
import json
import atexit
from datetime import datetime
from influxdb import InfluxDBClient
import sunspec.core.client as client
import model_manipulation as mm

def leaving(data):
    data.close()

parser = argparse.ArgumentParser("modbus_influxdb")
parser.add_argument("ip", help="The address of the device.", type=str)
parser.add_argument("db", help="InfluxDB name.", type=str)
args = parser.parse_args()

data = client.SunSpecClientDevice(client.TCP, 1, ipaddr=args.ip, ipport=502,timeout=20000)
atexit.register(leaving,data)

db_client = InfluxDBClient('localhost',8086, 'root', 'root', args.db)
db_client.create_database(args.db)


models_array = [
    #"common",
    #"model_10",
    #"model_11",
    #"model_12",
    "inverter",
    "model_65001",
    "model_65002",
    "model_65003",
    "model_65004",
    "model_65005",
    "model_65006",
    "model_65007",
    "model_65008",
    "model_65009",
    "model_65010",
    "model_65011"
    ]

while True:
    points_array = [
        #data.common,
        #data.model_10,
        #data.model_11,
        #data.model_12,
        data.inverter,
        data.model_65001,
        data.model_65002,
        data.model_65003,
        data.model_65004,
        data.model_65005,
        data.model_65006,
        data.model_65007,
        data.model_65008,
        data.model_65009,
        data.model_65010,
        data.model_65011
    ]

    attributes = []
    values = []
    for point in range(0,len(points_array)):
        try: 
            mm.read_values(points_array[point])
            model = models_array[point]
            attributes, values = mm.extract_attr_values(points_array[point])
            for attr in range (0,len(attributes)):
                #print (mm.write_json(model,values[attr],attributes[attr]))
                db_client.write_points(mm.write_json(model,values[attr],attributes[attr]))
        except Exception as error:
            print("EXCEPTION: " + str(error))
            data.close()
            try: 
                data = client.SunSpecClientDevice(client.TCP, 1, ipaddr=args.ip, ipport=502,timeout=10000)
            except Exception as e:
                print("Sunspec could not connect to device, trying again in 10 seconds")
                time.sleep(10)
                continue
            continue

    time.sleep(20)
