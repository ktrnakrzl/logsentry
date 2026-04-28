from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import re

app = Flask(__name__)

# Folder where uploaded log files will be saved
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Only allow text-based log files
ALLOWED_EXTENSIONS = {'log', 'txt'}


# Check if the uploaded file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Home route - shows the upload page
@app.route('/')
def index():
    return render_template('index.html')


# Analyze route - receives the uploaded file and scans it
@app.route('/analyze', methods=['POST'])
def analyze():
    # Get the uploaded file from the form input named "logfile"
    uploaded_file = request.files.get('logfile')

    # Check if the user submitted the form without choosing a file
    if not uploaded_file or uploaded_file.filename == '':
        return 'No file uploaded', 400

    # Check if the uploaded file is not a .log or .txt file
    if not allowed_file(uploaded_file.filename):
        return 'Only .log and .txt files are allowed', 400

    # Make the filename safe before saving it
    filename = secure_filename(uploaded_file.filename)

    # Build the full path where the uploaded file will be saved
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Save the uploaded file into the uploads folder
    uploaded_file.save(file_path)

    # Open and read the uploaded log file
    # errors='ignore' prevents crashes if the file has unusual characters
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    # Convert the log content to lowercase so matching is case-insensitive
    lower_content = content.lower()

    # These words may indicate errors or suspicious activity in a log file
    suspicious_keywords = [
        'error',
        'failed',
        'unauthorized',
        'denied',
        'warning',
        'attack',
        'malware',
        'brute force',
        'login failed',
        'port scan'
    ]

    # This list will store suspicious keywords that were found
    matches = []

    # Count how many times each suspicious keyword appears
    for keyword in suspicious_keywords:
        count = lower_content.count(keyword)

        # Only save keywords that were actually found
        if count > 0:
            matches.append({
                'keyword': keyword,
                'count': count
            })

    # Find possible IP addresses inside the log file
    ip_addresses = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', content)

    # Remove duplicate IP addresses and sort them alphabetically
    unique_ips = sorted(set(ip_addresses))

    # Send the analysis results to the result.html page
    return render_template(
        'results.html',
        filename=filename,
        matches=matches,
        ip_addresses=unique_ips,
        total_lines=len(content.splitlines())
    )


if __name__ == '__main__':
    app.run(debug=True)
