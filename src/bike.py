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
			place = len(station_list)
			for s in range(len(station_list)):
				if station_list[s]["distance"]>station_distance:
					place=s
					break
			station_list.insert(place,{"station id": station['station_id'],"name":station['name'],"distance":station_distance})
		# print(station_list)
	return station_list[:max_length]


def get_station_availability(station_list):
	url = 'https://gbfs.citibikenyc.com/gbfs/es/station_status.json'
	resp = requests.get(url=url)
	feed = resp.json()

	for station in station_list:
		station["bikes"]=0
		station["docks"]=0

	for station in feed['data']['stations']:
		#ISSUE: "bikes" and "docks" add up to number of docks, but valet stations don't always have all docks available to use so "docks" may be  overestimated.
		try:
			station_index = [i["station id"] for i in station_list].index(station["station_id"])
			station_list[station_index]["bikes"]=station["num_bikes_available"]
			station_list[station_index]["docks"]=station["num_docks_available"]
		except:
			pass
			
	return station_list

def main_function():
	user_latitude, user_longitude = get_user_location()
	nearby_station_list = get_nearby_stations(user_latitude, user_longitude,1000,5)
	nearby_station_status = get_station_availability(nearby_station_list)
	if len(nearby_station_status)>0:
		for station in nearby_station_status:
				print(station["name"]+" Station is "+str(int(station["distance"]))+" meters away"+": "+str(station["bikes"])+" bikes out of "+str(station["bikes"]+station["docks"])+" available.")
	else:
		print("no citi bike stations nearby")

if __name__ == "__main__":
	main_function()


