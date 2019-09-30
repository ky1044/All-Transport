import requests
import json


url = 'https://gbfs.citibikenyc.com/gbfs/es/station_status.json'

# params = dict(
#     origin='Chicago,IL',
#     destination='Los+Angeles,CA',
#     waypoints='Joplin,MO|Oklahoma+City,OK',
#     sensor='false'
# )

resp = requests.get(url=url)
feed = resp.json()

stations = {}
station_list = ["438","236","326"]
for station_number in station_list:
	stations[station_number]={
	"bikes":0,
	"docks":0
	}


for station in feed['data']['stations']:
	if station["station_id"] in stations:
		stations[station["station_id"]]["bikes"] = station["num_bikes_available"]
		stations[station["station_id"]]["docks"]=station["num_docks_available"]
		print(station)

#ISSUE: "bikes" and "docks" add up to number of docks, but valet stations don't have all docks available to use so "docks" is overestimated. 		
for station,info in stations.items():
	print("Station "+station+": "+str(info["bikes"])+" bikes out of "+str(info["bikes"]+info["docks"])+" docks available.")
