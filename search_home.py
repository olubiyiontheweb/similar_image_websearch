from flask import Flask, url_for, request, render_template

DEBUG = True

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home_page.html')


if __name__ == "__main__":
    app.run(debug=DEBUG)
