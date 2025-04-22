import gpxpy
import gpxpy.gpx
from geopy.distance import geodesic
import pandas as pd

class SlopeDataProcessor():
    def __init__(self, gpx_path):
        self.gpx_path = gpx_path
        with open(gpx_path, 'r') as f:
            self.gpx = gpxpy.parse(f)

    
    def load_data(self):
        data = []
        for track in self.gpx.tracks:
            for i, segment in enumerate(track.segments):
                for point in segment.points:
                # here i only extract out the start and end data

                    data.append( {
                        "segment_id": i,
                        "latitude" : point.latitude,
                        "longitude" : point.longitude,
                        "elevation" : point.elevation,
                        "time": point.time
                        })
                    
        df = pd.DataFrame(data)
        df['time'] = pd.to_datetime(df['time'])  # transfer "time" into datetime format
        df['time'] = df['time'].dt.tz_localize(None)  # get rid of timezone
        return df # all points in the gpx
    
    def compute_distance(self, row):
        if row['segment_id'] != row['segment_prev']:
            return None
        return geodesic((row['latitude'], row['longitude']), (row['lat_prev'], row['lon_prev'])).meters
    
    def summarize_segments(self):
        df = self.load_data()
        df['lat_prev'] = df["latitude"].shift(1)
        df['lon_prev'] = df["longitude"].shift(1)
        df['ele_prev'] = df["elevation"].shift(1)
        df['time_prev'] = df['time'].shift(1)
        df['segment_prev'] = df['segment_id'].shift(1)
        # new 'time_diff(s)'
        df['time_diff(s)'] = (df['time'] - df['time_prev']).dt.total_seconds()
        df['distance_to_prev(m)'] = df.apply(self.compute_distance, axis=1)

        # new 'speed_m/s'
        df['speed_m/s'] = df['distance_to_prev(m)'] / df['time_diff(s)']

        # test if the run is lift
        segment_drop = (
            df.groupby('segment_id')
            .agg(start_ele=('elevation', 'first'), end_ele=('elevation', 'last'))
        )

        segment_drop['ele_drop'] = segment_drop['end_ele'] - segment_drop['start_ele']
        segment_drop['is_lift'] = segment_drop['ele_drop'] > 0 
        df = df.merge(
            segment_drop['is_lift'],
            left_on='segment_id',
            right_index=True
        )
        return df
