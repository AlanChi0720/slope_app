
# ⛷️ Slope Analyzer Web App

This is a Python-based web application for visualizing and analyzing ski run data from `.gpx` files. It generates interactive maps and detailed visualizations of elevation, speed, and segment information from your ski sessions.

## 📂 Project Structure

```
.
├── app.py                # Flask web server
├── main.py              # Local test script
├── process_data.py      # GPX data processing and analysis
├── visualize_data.py    # Interactive map creation
├── slope_app.ipynb      # Jupyter Notebook (for prototyping or testing)
├── uploads/             # Uploaded GPX files (created automatically)
└── static/              # Output visualizations (maps and charts)
```

## 🚀 Features

- 📁 Upload `.gpx` files through a web interface
- 📊 Automatic processing and segmentation of ski runs
- 🗺️ Generates interactive maps (using Folium) colored by speed
- 📈 Plots elevation and speed profiles for each ski run
- 🚡 Detects and filters out ski lifts based on elevation gain

## 🛠️ Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/yourusername/slope-analyzer.git
   cd slope-analyzer
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is not provided, install manually:
   ```bash
   pip install flask pandas matplotlib gpxpy geopy folium branca
   ```

## 🌐 How to Use

1. **Run the Flask server**
   ```bash
   python app.py
   ```

2. **Open the app**  
   Navigate to `http://localhost:3000` in your browser.

3. **Upload a GPX file**  
   After upload:
   - You will be redirected to a results page
   - An interactive map (`ski_map.html`) and charts (`summary.png`, `summary_sep.png`) are generated in the `static/` folder

## 📌 Notes

- Only `.gpx` files are supported for upload.
- Lifts are detected automatically based on elevation gain.
- The `main.py` script can be used for local testing and visualization outside the web app.

## 📷 Example Outputs

- `static/ski_map.html` – interactive map colored by speed
- `static/summary.png` – combined plot of all ski runs
- `static/summary_sep.png` – individual plots per run

## 📬 Contact

Feel free to reach out if you have questions or suggestions!
