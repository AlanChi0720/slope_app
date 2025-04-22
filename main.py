from process_data import SlopeDataProcessor
from visualize_data import SlopeVisualizer

p = SlopeDataProcessor("slope_app\January 20, 2025 - Mt Naeba.gpx")
df = p.summarize_segments()

viz = SlopeVisualizer(df)
viz.show_map()
viz.save_map("slope_app/ski.html")