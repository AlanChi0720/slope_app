import gpxpy
import gpxpy.gpx
from geopy.distance import geodesic
import pandas as pd

file_path = "January 20, 2025 - Mt Naeba.gpx"

gpx_file = open(file_path, 'r')
gpx = gpxpy.parse(gpx_file)

tracks = {}

for track in gpx.tracks:
    for i, segment in enumerate(track.segments):
        start = segment.points[0]
        end  = segment.points[-1]

        tracks[i] = {
            "segment_id": i,
            "start_lat" : start.latitude,
            "start_lon" : start.longitude,
            "start_ele" : start.elevation,
            "end_lat" : end.latitude,
            "end_lon" : end.longitude,
            "end_ele" : end.elevation,
            "distance_mi" : geodesic((start.latitude, start.longitude), (end.latitude, end.longitude)).miles,
            "ele_drop": end.elevation - start.elevation
            }

df = pd.DataFrame.from_dict(tracks, orient = "index")
print(df)