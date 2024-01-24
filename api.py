import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

stop_parameters = {
    "api_key": os.environ['API_KEY'],
    "operator_id" : 'SC',
    "stop_id": '62943',
    "format": 'json'
}

parameters = {
    "api_key": os.environ['API_KEY'],
    "agency" : 'SC',
    "stopcode": '62943',
    "format": 'json'
}

aimed_arrival_times = []
expected_arrival_times = []

stops = requests.get('http://api.511.org/transit/stopplaces', params=stop_parameters)
#print(stops.status_code)

response = requests.get('http://api.511.org/transit/StopMonitoring', params=parameters)
#print(response.status_code)

stop_content = stops.content.decode('utf-8-sig')
# converting JSON string to Python Dict
stop_data = json.loads(stop_content)

# understanding info in json file
# stop_json_format = json.dumps(stop_data, indent=4) 


stop_id = stop_data['Siri']['ServiceDelivery']['DataObjectDelivery']['dataObjects']['SiteFrame']['stopPlaces']['StopPlace']['@id']
stop_name = stop_data['Siri']['ServiceDelivery']['DataObjectDelivery']['dataObjects']['SiteFrame']['stopPlaces']['StopPlace']['Name']

content = response.content.decode('utf-8-sig') 
# converting JSON string to Python Dict
data = json.loads(content)

monitoredStopVisits = data['ServiceDelivery']['StopMonitoringDelivery']['MonitoredStopVisit']

# sometimes MonitoredStopVisit can be empty depending on the time querying
if monitoredStopVisits:
    for i in monitoredStopVisits:
        aimed_arrival = i['MonitoredVehicleJourney']['MonitoredCall']['AimedArrivalTime']
        aimed_datetime_version = datetime.fromisoformat(aimed_arrival [:-1])
        aimed_arrival_times.append(aimed_datetime_version)

        expected_arrival = i['MonitoredVehicleJourney']['MonitoredCall']['ExpectedArrivalTime']
        if isinstance(expected_arrival, str):
            expected_datetime_version = datetime.fromisoformat(expected_arrival [:-1])
            expected_arrival_times.append(expected_datetime_version)
        
        else :
            expected_arrival_times.append(expected_arrival)


print("Current Time: ", datetime.now())
print("Stop Id: ", stop_id)
print("Stop Name: ", stop_name)
print(aimed_arrival_times)
print(expected_arrival_times)


def soonest_bus():
    if aimed_arrival_times:
        wait_time = aimed_arrival_times[0] - datetime.now()
        seconds = wait_time.total_seconds()
        minutes = divmod(seconds, 60)[0]
        print(minutes)
        #return wait_time
    else:
        print("No more buses")
        return "No more buses"

