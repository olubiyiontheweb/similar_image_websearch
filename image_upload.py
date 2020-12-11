import os
from werkzeug.utils import secure_filename
import cv2
from flask import Flask, flash, request, redirect, url_for, jsonify, render_template, send_from_directory
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K

UPLOAD_FOLDER = "./uploads/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
debug = True


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Initialize Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('not file uploaded')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            print
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            redirect(url_for('upload_file', filename=filename))
            return render_template('uploaded_image.html')

    return render_template('upload_home.html')


@app.route('/uploads/<filename>')
def upload_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=debug)
