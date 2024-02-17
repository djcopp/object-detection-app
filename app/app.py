from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw
import torch
import os

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        object_name = request.form.get('object_name')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            detections = run_detection(file_path, object_name)
            return render_template('index.html', uploaded_file_url=detections)

    return render_template('index.html')

def run_detection(image_path, object_name):
    # Perform inference
    results = model([image_path])
    results = results.pandas().xyxy[0]  # Get detections in pandas format
    # Filter detections by object name
    results = results[results['name'] == object_name]

    # Load the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Draw bounding boxes
    for index, row in results.iterrows():
        bbox = row[['xmin', 'ymin', 'xmax', 'ymax']]
        draw.rectangle(((bbox['xmin'], bbox['ymin']), (bbox['xmax'], bbox['ymax'])), outline='red', width=2)

    # Save the image with detections
    detection_path = f"{image_path.split('.')[0]}_detection.jpg"
    image.save(detection_path)

    return url_for('uploaded_file', filename=os.path.basename(detection_path))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)