from flask import Flask, render_template, request
import os

app = Flask(__name__)

#folder to save uploaded files from log
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#home route - shows the upload page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)