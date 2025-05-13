from flask import Flask, request, render_template, redirect
import os

# imposrt the analyze tools
from process_data import SlopeDataProcessor, SlopeSummary
from visualize_data import SlopeVisualizer

# define the upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("static", exist_ok=True)


# create a app object
app = Flask(
    __name__,
    static_folder = "static" , # 靜態檔案資料夾名稱(可以自己決定)
)


# 使用GET方法 建立路徑 / 對應的處裡函式
@app.route("/" , methods= ['GET']) # 函式的裝飾(decortor): 以函式為基礎，提供附加功能
def index():
    lang = request.headers.get("accept-language")
    if lang.startswith("en"):
        return render_template("upload.html") 
    else:
        return render_template("upload.html")
    

ALLOWED_EXTENSIONS = {'gpx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    if not allowed_file(file.filename):
        return "Invalid file type. Please upload a .gpx file."

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
        # 👉 呼叫分析流程
    processor = SlopeDataProcessor(filepath)
    df = processor.summarize_segments()

    # 👉 地圖儲存為 HTML
    visualizer = SlopeVisualizer(df)
    visualizer.save_map("static/ski_map.html")  # Flask 自動提供 static 資料夾

    # 👉 圖表儲存成圖片
    summary = SlopeSummary(df)
    summary.plot_all_segments()       # 可以額外修改成存圖而不是 show()
    summary.plot_all_segments_sep()

    return redirect("/result")

@app.route("/result")
def result():
    return render_template("result.html")
 
if __name__ == "__main__": #如果以主程式執行
    app.run(port=3000, debug=True) #立刻啟動伺服器, 可透過 port參數 指定埠號