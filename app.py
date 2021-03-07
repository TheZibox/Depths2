from flask import Flask
from flask import render_template
from datetime import time
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os, shutil
import pandas as pd
from analysis import analysis


UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'GDtfDCFYjD'

folder = os.path.abspath(app.config['UPLOAD_FOLDER'])


def delete_existing_files():
    """Make sure previously uploaded files are deleted before new ones are added"""
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def allowed_file(filename):
    """Check for file format"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def depths_file():
    """For uploading the depths csv file.
    This file must not be named depths.csv. The program changes file name"""
    delete_existing_files()

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.filename = 'depths.csv'
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_v_curve_file'))
        else:
            flash('Wrong file format')
            return redirect(request.url)

    return render_template('upload.html')


@app.route('/upload_v_curve_file', methods=['GET', 'POST'])
def upload_v_curve_file():
    """For uploading the v_curve csv file.
        This file must not be named v_curve.csv. The program changes file name"""
    if request.method == 'POST':
        # check if the post request has the file part

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.filename = 'v_curve.csv'
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('success'))
        else:
            flash('Wrong file format')
            return redirect(request.url)

    return render_template('upload_v_curve.html')


@app.route('/success')
def success():
    return render_template('success.html')


@app.route("/scatter")
def scatter():
    results = analysis(folder)

    return render_template('scatter.html', results=results)


if __name__ == "__main__":
    app.run(debug=True)
