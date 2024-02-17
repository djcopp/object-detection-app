from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# This is the path to the directory where you will store the uploaded files
# and the processed results
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Ensure these folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


def allowed_file(filename):
    # Check if the file is an allowed type
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/detect', methods=['POST'])
def detect():
    # Check if the post request has the file part
    if 'image' not in request.files:
        print('No file part')
        return redirect(request.url)
    file = request.files['image']
    
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        print('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Here, you would call your object detection function and pass the file path
        # For example: detected_objects = object_detection_function(file_path)
        # Then save the processed image to the PROCESSED_FOLDER
        # processed_image_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
        
        # For now, let's just redirect to the upload form page
        return redirect(url_for('index'))
    
    return redirect(request.url)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # This route will be used to display the uploaded image
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/processed/<filename>')
def processed_file(filename):
    # This route will be used to display the processed image
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
