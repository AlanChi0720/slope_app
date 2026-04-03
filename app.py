from flask import Flask, request, render_template, redirect, url_for
import os, json

from process_data import SlopeDataProcessor, SlopeSummary
from visualize_data import SlopeVisualizer

UPLOAD_FOLDER = 'uploads'
STATS_PATH = 'static/stats.json'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static', exist_ok=True)

app = Flask(__name__, static_folder='static')
app.secret_key = 'slope-app-2025'

ALLOWED_EXTENSIONS = {'gpx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    error = request.args.get('error')
    return render_template('upload.html', error=error)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index', error='no_file'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index', error='no_selection'))

    if not allowed_file(file.filename):
        return redirect(url_for('index', error='invalid_type'))

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    processor = SlopeDataProcessor(filepath)
    df = processor.summarize_segments()

    visualizer = SlopeVisualizer(df)
    visualizer.save_map('static/ski_map.html')

    summary = SlopeSummary(df)
    summary.plot_all_segments()
    summary.plot_all_segments_sep()

    stats = summary.get_stats()
    with open(STATS_PATH, 'w') as f:
        json.dump(stats, f)

    return redirect(url_for('result'))


@app.route('/result')
def result():
    if not os.path.exists(STATS_PATH):
        return redirect(url_for('index'))
    with open(STATS_PATH) as f:
        stats = json.load(f)
    return render_template('result.html', stats=stats)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
