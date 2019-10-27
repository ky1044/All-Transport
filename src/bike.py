import requests
import json
from geopy import distance
import geocoder


def get_user_location():
	g = geocoder.ip('me')
	return g.latlng


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
				if station_list[s][2]<station_distance:
					place=s
			station_list.insert(place,[station['station_id'],station['name'],station_distance])
		# print(station_list)
	return station_list[:max_length]


def get_station_availability(station_list):
	url = 'https://gbfs.citibikenyc.com/gbfs/es/station_status.json'
	resp = requests.get(url=url)
	feed = resp.json()

	station_statuses = {}
	for station_number in station_list:
		station_statuses[station_number[0]]={
		"name":station_number[1],
		"distance":station_number[2],
		"bikes":0,
		"docks":0
		}

	for station in feed['data']['stations']:
		if station["station_id"] in station_statuses:
			#ISSUE: "bikes" and "docks" add up to number of docks, but valet stations don't always have all docks available to use so "docks" may be  overestimated.
			station_statuses[station["station_id"]]["bikes"] = station["num_bikes_available"]
			station_statuses[station["station_id"]]["docks"]=station["num_docks_available"]

	return station_statuses

def main_function():
	user_latitude, user_longitude = get_user_location()
	nearby_station_list = get_nearby_stations(user_latitude, user_longitude,1000,5)
	nearby_station_status = get_station_availability(nearby_station_list)
	for station,info in nearby_station_status.items():
			print("Station "+info["name"]+" "+str(round(info["distance"],2))+" meters away"+": "+str(info["bikes"])+" bikes out of "+str(info["bikes"]+info["docks"])+" available.")

if __name__ == "__main__":
	
	main_function()


