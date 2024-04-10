from flask import Flask, request, send_from_directory, jsonify, render_template
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Uploaded successfully!</title>
</head>
<body>
    <h1>Uploaded successfully!</h1>
    <button onclick="redirectToMainPage()">Go Back</button>

    <script>
        function redirectToMainPage() {
            window.location.href = '/';
        }
    </script>
</body>
</html>""", 200

@app.route('/files/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return 'File not found', 404

@app.route('/list_files', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

@app.route('/delete_file/<filename>', methods=['GET'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Deleted successfully!</title>
</head>
<body>
    <h1>Deleted successfully!</h1>
    <button onclick="redirectToMainPage()">Go Back</button>

    <script>
        function redirectToMainPage() {
            window.location.href = '/';
        }
    </script>
</body>
</html>
""", 200
    else:
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Nah. (404 error)</title>
</head>
<body>
    <h1>Nah. (404 error)</h1>
    <button onclick="redirectToMainPage()">Go Back</button>

    <script>
        function redirectToMainPage() {
            window.location.href = '/';
        }
    </script>
</body>
</html>
""", 404

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run('0.0.0.0', 8080)