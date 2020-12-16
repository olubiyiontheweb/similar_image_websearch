from flask import Flask, url_for, request, render_template, redirect, flash, send_from_directory
from werkzeug.utils import secure_filename
import sqlite3
import os

from database_structure import database_migrations
from image_store_processing import compare_files, preprocess, ALLOWED_EXTENSIONS, IMAGE_FOLDER

# conn = sqlite3.connect('.\\database\\database.db')
# print("Opened database successfully")
# conn.close()

#initialize database
db = database_migrations()
images = compare_files()
preprocess_images = preprocess()
preprocess_images.load_images_into_to_db()
db.image_store_migrations()

DEBUG = True

UPLOAD_FOLDER = '.\\uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('not file uploaded')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            redirect(url_for('upload_file', filename=filename))
            #return render_template('uploaded_image.html')

    return render_template('home_page.html')


@app.route('/uploads/<filename>')
def upload_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/search_results', methods=['GET'])
def search_results():
    images = list()
    print(images)
    images = preprocess_images.request_list_of_images_in_db()
    return render_template('search_results.html', images=images)


@app.route('/image_store/<filename>')
def image_store(filename):
    return send_from_directory(app.config['IMAGE_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=DEBUG)
