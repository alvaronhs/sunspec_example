from datetime import datetime

def check_model(model, value):
    if (model == 'VTABLE6_TB' or model == 'VTABLE2_TenB' or model == 'VTABLE2_CorrB' 
    or model == 'VTABLE4_FreqS' or model == 'VTABLE4_TS1'):
        return value / 10
    else:
        return value

def write_json(measurement, value, model):
    if str(value) == 'None':
        value = 0
    value = check_model(model, value)
    json_body = [
        {
            "measurement": measurement,
            "tags": {
                "server": "NHS"
            },
            "time": get_time(),
            "fields": {
                model: value
            }
        }
    ]
    return json_body

def extract_attr_values (data):
    model = []
    model = data.points
    values = []
    attributes = []
    for points in model:
        values.append(getattr(data,str(points)))
        attributes.append(points)
    return attributes, values

def read_values(data):
    data.read()

def get_time():
    now = datetime.utcnow()
    dt_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return dt_string