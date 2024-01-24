import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

stop_parameters = {
    "api_key": os.environ['API_KEY'],
    "operator_id" : 'BA',
    "stop_id": '16TH',
    "format": 'json'
}

parameters = {
    "api_key": os.environ['API_KEY'],
    "agency" : 'BA',
    "stopcode": '16TH',
    "format": 'json'
}

aimed_arrival_times = []
expected_arrival_times = []

stops = requests.get('http://api.511.org/transit/stopplaces', params=stop_parameters)
#print(stops.status_code)

response = requests.get('http://api.511.org/transit/StopMonitoring', params=parameters)
#print(response.status_code)


def create_datetime_object(string):
    datetime_version = datetime.fromisoformat(string [:-1])
    return datetime_version


stop_content = stops.content.decode('utf-8-sig')
# converting JSON string to Python Dict
stop_data = json.loads(stop_content)

# understanding info in json file
# stop_json_format = json.dumps(stop_data, indent=4) 

# querying stop id and stop name from the JSON data
stop_id = stop_data['Siri']['ServiceDelivery']['DataObjectDelivery']['dataObjects']['SiteFrame']['stopPlaces']['StopPlace']['@id']
stop_name = stop_data['Siri']['ServiceDelivery']['DataObjectDelivery']['dataObjects']['SiteFrame']['stopPlaces']['StopPlace']['Name']

content = response.content.decode('utf-8-sig') 
# converting JSON string to Python Dict
data = json.loads(content)
#print = json.dumps(data, indent=4) 

monitoredStopVisits = data['ServiceDelivery']['StopMonitoringDelivery']['MonitoredStopVisit']

# sometimes MonitoredStopVisit can be empty depending on the time querying
if monitoredStopVisits:
    for i in monitoredStopVisits:
        aimed_arrival = i['MonitoredVehicleJourney']['MonitoredCall']['AimedArrivalTime']
        aimed_datetime_version = create_datetime_object(aimed_arrival)
        aimed_arrival_times.append(aimed_datetime_version)

        expected_arrival = i['MonitoredVehicleJourney']['MonitoredCall']['ExpectedArrivalTime']
        if isinstance(expected_arrival, str):
            expected_datetime_version = create_datetime_object(expected_arrival)
            expected_arrival_times.append(expected_datetime_version)
        
        else :
            expected_arrival_times.append(expected_arrival)


def get_stopId():
    return stop_id

def get_stopName():
    return stop_name

def get_aimed_arrival_times():
    return aimed_arrival_times

def get_expected_arrival_times():
    return expected_arrival_times

def soonest_bus():
    if aimed_arrival_times:
        wait_time = aimed_arrival_times[0] - datetime.now()
        seconds = wait_time.total_seconds()
        minutes = divmod(seconds, 60)[0]
        return wait_time
    else:
        return "No more buses"
    

print("Current Time: ", datetime.now())
print("Stop Id: ", get_stopId())
print("Stop Name: ", get_stopName())
print(get_aimed_arrival_times())
print(get_expected_arrival_times())
print(soonest_bus())