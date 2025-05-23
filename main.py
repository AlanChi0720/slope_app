from process_data import SlopeDataProcessor, SlopeSummary
from visualize_data import SlopeVisualizer

p = SlopeDataProcessor("January 20, 2025 - Mt Naeba.gpx")
df = p.summarize_segments()

viz = SlopeVisualizer(df)
viz.show_map()
# viz.save_map("ski.html")

summary = SlopeSummary(df)

# show the summary results
# if want to run this main, replace the save with show in process_data
summary.plot_all_segments()

# show each runs result
# if want to run this main, replace the save with show in process_data
summary.plot_all_segments_sep()