import requests
import json
from geopy import distance


def get_nearby_stations(lat,lon,radius,max_length):
	url = 'https://gbfs.citibikenyc.com/gbfs/en/station_information.json'
	resp = requests.get(url=url)
	feed = resp.json()

	user_coord = (lat,lon)


	station_list=[]


	for station in feed['data']['stations']:
		station_coord = (station['lat'],station['lon'])
		station_distance = distance.distance(user_coord, station_coord).m
		# print(station_distance)
		if station_distance<radius:
			place = 0
			for s in range(len(station_list)):
				if station_list[s][1]<station_distance:
					place=s
			station_list.insert(place,[station['station_id'],station_distance])
		# print(station_list)
	return station_list[:max_length]



def get_station_availability(station_list):
	url = 'https://gbfs.citibikenyc.com/gbfs/es/station_status.json'
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

	#ISSUE: "bikes" and "docks" add up to number of docks, but valet stations don't always have all docks available to use so "docks" may be  overestimated. 		
	for station,info in stations.items():
		print("Station "+station+": "+str(info["bikes"])+" bikes out of "+str(info["bikes"]+info["docks"])+" available.")

	return stations




print(get_nearby_stations(40.727258, -73.983639,1000,5))


