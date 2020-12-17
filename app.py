from flask import Flask, url_for, request, render_template, redirect, flash, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import sqlite3
import dhash
import os

from database_structure import database_migrations
from image_store_processing import compare_files, preprocess, ALLOWED_EXTENSIONS

# conn = sqlite3.connect('.\\database\\database.db')
# print("Opened database successfully")
# conn.close()

#initialize database
IMAGE_STORE = ".\image_store"
db = database_migrations()
compare_images = compare_files()
preprocess_images = preprocess()
preprocess_images.load_images_into_to_db()
preprocess_images.generate_hash()
db.image_store_migrations()

DEBUG = True

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGE_STORE'] = IMAGE_STORE
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files and 'text' not in request.form['text']:
            print('No text or file uploaded')
            return redirect(request.url)

        file = request.files['file']
        text = request.form['text'].lower()
        print("there is text" + text)

        if file.filename == '' and text == '':
            print('No input text or file selected')
            return redirect(request.url)

        if file.filename != '':
            print("file was uploaded")
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = Image.open(file)
                row, col = dhash.dhash_row_col(image)
                uploaded_image_hash = dhash.format_hex(row, col)
                print(type(uploaded_image_hash))
                print("Here is the hash " + str(uploaded_image_hash))

                list_of_available_image_hashes = compare_images.request_image_hashes(
                )

                # similar_images.clear()
                # similarity.clear()
                global similarity
                global similar_images
                similar_images = list()
                similarity = dict()
                similar_images.clear()
                for img_hash in list_of_available_image_hashes:
                    # print("uploaded_image_hash: " + str(uploaded_image_hash))
                    similarity[
                        "index"] = compare_images.calculate_hamming_dist(
                            uploaded_image_hash, img_hash["image_hash"])

                    print(similarity["index"])

                    if similarity["index"] < 10:
                        similarity["image_name"] = img_hash["image_name"]
                        similar_images.append(similarity.copy())

                    similarity.clear()

                    print("these are the images to display" +
                          str(similar_images))

                return render_template('search_results.html',
                                       images=similar_images)

                #redirect(url_for('upload_file', filename=filename))
                #return render_template('uploaded_image.html')

    return render_template('home_page.html')


@app.route('/uploads/<filename>')
def upload_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/search_results', methods=['GET', 'POST'])
def search_results():
    if request.method == 'POST':
        if 'file' not in request.files and 'text' not in request.form['text']:
            print('No text or file uploaded')
            return redirect(request.url)

        file = request.files['file']
        text = request.form['text'].lower()
        print("there is text" + text)

        if file.filename == '' and text == '':
            print('No input text or file selected')
            return redirect(request.url)

        if file.filename != '':
            print("file was uploaded")
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = Image.open(file)
                row, col = dhash.dhash_row_col(image)
                uploaded_image_hash = dhash.format_hex(row, col)
                print(type(uploaded_image_hash))
                print("Here is the hash " + str(uploaded_image_hash))

                list_of_available_image_hashes = compare_images.request_image_hashes(
                )

                # similar_images.clear()
                # similarity.clear()
                global similarity
                global similar_images
                similar_images = list()
                similarity = dict()
                similar_images.clear()
                for img_hash in list_of_available_image_hashes:
                    # print("uploaded_image_hash: " + str(uploaded_image_hash))
                    similarity[
                        "index"] = compare_images.calculate_hamming_dist(
                            uploaded_image_hash, img_hash["image_hash"])

                    print(similarity["index"])

                    if similarity["index"] < 10:
                        similarity["image_name"] = img_hash["image_name"]
                        similar_images.append(similarity.copy())

                    similarity.clear()

                    print("these are the images to display" +
                          str(similar_images))

                return render_template('search_results.html',
                                       images=similar_images)

    images = list()
    print(images)
    images = preprocess_images.request_list_of_images_in_db()
    return render_template('search_results.html', images=images)


@app.route('/image_store/<filename>')
def image_store(filename):
    return send_from_directory(app.config['IMAGE_STORE'], filename)


if __name__ == "__main__":
    app.run(debug=DEBUG)
