"""created by barthk12"""
import os
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_from_directory
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.getcwd(),"static/photos")
# create the upload folder should it not exist yet
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


# Configure app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Reload templates automatically
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response
    
# Configure session to use filesystem (instead of signed cookie)
app.config['SESSION_FILE_DIR'] = mkdtemp()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)

# Check if file should be allowed to upload
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/classifier", methods=['GET', 'POST'])
def classifier():
    if request.method == "POST":
         # check if the post request has the file part
         if "file" not in request.files:
             flash("No file part")
             return redirect((request.url))
         file = request.files["file"]
         if file.filename == "":
             flash("No selected file")
             return redirect(request.url)
         if file and allowed_file(file.filename):
             filename = secure_filename(file.filename)
             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
             return render_template("result.html", filename=filename)
         else:
             flash("Filetype not supported")
             return redirect(request.url)
         
    return render_template("classifier.html")

@app.route("/about")
def about_me():
    return render_template("about.html")


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

