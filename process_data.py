import gpxpy
import gpxpy.gpx
from geopy.distance import geodesic
import pandas as pd
import matplotlib.pyplot as plt
import math


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


class SlopeSummary:
    def __init__(self, df):
        self.df = df

    def plot_all_segments(self):

        # create the plot
        fig, ax1 = plt.subplots(figsize=(10, 4))
        ax2 = ax1.twinx()

        df = self.df[self.df['is_lift'] == False].copy()

        for segment_id, seg_df in df.groupby('segment_id'):
            # calculate each run's total_distance
            seg_df = seg_df.copy()  # aovid SettingWithCopyWarning
            seg_df['total_distance'] = seg_df['distance_to_prev(m)'].fillna(0).cumsum()

            summary = {
            "segment_id": segment_id,
            "start_ele": seg_df['elevation'].iloc[0],
            "end_ele": seg_df['elevation'].iloc[-1],
            "total_distance": seg_df['distance_to_prev(m)'].fillna(0).sum(),
            "avg_speed": seg_df['speed_m/s'].mean(),
            "max_speed": seg_df['speed_m/s'].max(),
            "max_speed_x": seg_df.loc[seg_df['speed_m/s'].idxmax(), 'total_distance']
            }
            summary["avg_gradient"] = (summary["end_ele"] - summary["start_ele"]) / summary["total_distance"] * 100 if summary["total_distance"] != 0 else 0

            self._plot_single_segment(seg_df, summary, ax1, ax2)

        ax1.set_xlabel("Distance (m)")
        ax1.set_ylabel("Elevation (m)", color='sienna')
        ax2.set_ylabel("Speed (m/s)", color='royalblue')

        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")

        plt.title("All Ski Runs: Elevation and Speed")
        plt.tight_layout()
        plt.savefig("static/summary.png")  # 把圖存成靜態檔案
        plt.close()  # 關閉圖表，避免 memory overflow

            

    def _plot_single_segment(self, seg_df, summary, ax1, ax2):

        # 畫 Elevation 曲線
        ax1.plot(
            seg_df['total_distance'],
            seg_df['elevation'],
            label=f"Run {summary['segment_id']} (Elev)"
        )

        # 畫 Speed 曲線
        ax2.plot(
            seg_df['total_distance'],
            seg_df['speed_m/s'],
            linestyle="--",
            label=f"Run {summary['segment_id']} (Speed)"
        )

    
    def plot_all_segments_sep(self):
        # 只保留滑雪段
        df = self.df[self.df['is_lift'] == False].copy()

        runs = list(df['segment_id'].unique())  # 拿到所有 segment_id
        n_runs = len(runs)

        # 設定每行顯示的子圖數量
        ncols = 1  # 每行放 2 個小圖
        nrows = math.ceil(n_runs / ncols)

        # 建立子圖
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(14, nrows * 5))

        # 保證 axs 是一個一維陣列，不管行列數是多少
        axs = axs.flatten()

        for i, (segment_id, seg_df) in enumerate(df.groupby('segment_id')):
            ax1 = axs[i]
            seg_df = seg_df.copy()
            seg_df['total_distance'] = seg_df['distance_to_prev(m)'].fillna(0).cumsum()

            # 計算 summary 數據
            avg_speed = seg_df['speed_m/s'].mean()
            max_speed = seg_df['speed_m/s'].max()
            max_speed_x = seg_df.loc[seg_df['speed_m/s'].idxmax(), 'total_distance']

            # 畫 elevation 曲線
            ax1.plot(seg_df['total_distance'], seg_df['elevation'], color='sienna', label='Elevation')

            # twin x 軸畫 speed 曲線
            ax2 = ax1.twinx()
            ax2.plot(seg_df['total_distance'], seg_df['speed_m/s'], color='royalblue', linestyle='--', label='Speed')

            # 畫 avg speed 虛線
            ax2.axhline(avg_speed, color='blue', linestyle='--', alpha=0.5)
            ax2.text(
                seg_df['total_distance'].max() * 0.7,
                avg_speed + 0.5,
                f"Avg: {avg_speed:.2f} m/s",
                fontsize=8,
                color='blue'
            )

            # 標記最大速度
            ax2.annotate(
                f"Max: {max_speed:.2f} m/s",
                xy=(max_speed_x, max_speed),
                xytext=(max_speed_x, max_speed - 1),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=8,
                color='red'
            )

            # 標題與軸標籤
            ax1.set_title(f"Run {segment_id}")
            ax1.set_xlabel("Distance (m)")
            ax1.set_ylabel("Elevation (m)", color='sienna')
            ax2.set_ylabel("Speed (m/s)", color='royalblue')

        # 如果子圖數量比 runs 多，要關掉多餘的子圖
        for j in range(i+1, len(axs)):
            fig.delaxes(axs[j])

        plt.tight_layout()
        plt.savefig("static/summary_sep.png")  # 把圖存成靜態檔案
        plt.close()  # 關閉圖表，避免 memory overflow