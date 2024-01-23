import requests
import json
from datetime import datetime, timezone

stop_parameters = {
    "api_key": '',
    "operator_id" : 'SC',
    "stop_id": '62943',
    "format": 'json'
}

parameters = {
    "api_key": '',
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
stop_data = json.loads(stop_content)
stop_json_format = json.dumps(stop_data, indent=4)  


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