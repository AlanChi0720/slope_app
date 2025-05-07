import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib import colormaps
import folium
import branca

class SlopeVisualizer:
    def __init__(self, df):
        self.df = df
        self._setup_colors()
        self.map = self._draw_map()
        self.add_legend()

    def _setup_colors(self):
        self.min_speed = self.df['speed_m/s'].min()
        self.max_speed = self.df['speed_m/s'].max()
        self.norm = colors.Normalize(vmin=self.min_speed, vmax=self.max_speed)
        self.cmap = colormaps.get_cmap('coolwarm')
    
    def _draw_map(self):
        # finding the center of the map by using the first and last point' location
        center_location = (
            self.df["latitude"].mean(),
            self.df["longitude"].mean()
        )

        # set map's center
        map = folium.Map(location=center_location, tiles="OpenStreetMap", zoom_start=16)

        for i in range(1, len(self.df)):
            if self.df.loc[i, 'segment_id'] != self.df.loc[i-1, 'segment_id']:
                continue

            p1 = (self.df.loc[i-1, "latitude"], self.df.loc[i-1, "longitude"])
            p2 = (self.df.loc[i, "latitude"], self.df.loc[i, "longitude"])
            speed = self.df.loc[i, 'speed_m/s']
            color_rgb = self.cmap(self.norm(speed))
            color_hex = colors.to_hex(color_rgb)
            if self.df["is_lift"][i]:
                folium.PolyLine([p1, p2], color="gray", weight=4).add_to(map)
            else:
                folium.PolyLine([p1, p2], color=color_hex, weight=4).add_to(map)

        return map
    
    def add_legend(self):
        colormap = branca.colormap.LinearColormap(
            colors=[self.cmap(self.norm(v)) for v in [self.min_speed, self.max_speed]],
            vmin=self.min_speed,
            vmax=self.max_speed
        )
        colormap.caption = 'Speed (m/s)'
        colormap.add_to(self.map)
        
    def show_map(self):
        return self.map

    def save_map(self, filename):
        self.map.save(filename)
