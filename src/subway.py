
import requests
import os
from google.transit import gtfs_realtime_pb2
MTA_KEY = os.environ.get('MTA_KEY')

feed = gtfs_realtime_pb2.FeedMessage()
r = requests.get("http://datamine.mta.info/mta_esi.php?key=" +MTA_KEY+"&feed_id=1", allow_redirects=True)
feed.ParseFromString(r.content)
for i in range(len(feed.entity)):
	print(feed.entity[i])
