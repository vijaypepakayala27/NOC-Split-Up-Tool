import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from werkzeug.utils import secure_filename
import pandas as pd
import zipfile
import io
import shutil

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.before_request
def create_session_folder():
    # Generate a unique folder for each session
    session_id = session.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())  # Generate a new unique session ID
        session['session_id'] = session_id

    session_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    if not os.path.exists(session_folder):
        os.makedirs(session_folder)
    session['session_folder'] = session_folder

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'logged_in' not in session or not session['logged_in']:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/do_login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    # Simplified check for demonstration purposes
    if username == 'admin' and password == 'password':
        session['logged_in'] = True
        return redirect(url_for('chat'))
    else:
        flash('Invalid credentials, please try again.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    clear_session_folder()
    session.pop('logged_in', None)
    session.pop('session_id', None)  # Clear the session ID
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload():
    clear_session_folder()  # Clear any existing files in this session

    if 'file1' not in request.files or 'file2' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file1 = request.files['file1']
    file2 = request.files['file2']
    names = request.form['names'].split(',')

    if file1.filename == '' or file2.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file1 and file2 and names:
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        session_folder = session.get('session_folder')
        file1_path = os.path.join(session_folder, filename1)
        file2_path = os.path.join(session_folder, filename2)
        file1.save(file1_path)
        file2.save(file2_path)

        # If the files are ZIP, extract them
        if zipfile.is_zipfile(file1_path):
            file1_paths = extract_zip(file1_path, session_folder)
        else:
            file1_paths = [file1_path]

        if zipfile.is_zipfile(file2_path):
            file2_paths = extract_zip(file2_path, session_folder)
        else:
            file2_paths = [file2_path]

        process_files(file1_paths, file2_paths, names)

        # Create a ZIP file in memory
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for name in names:
                output_filename = f"{name.strip()}_tickets.csv"
                zf.write(os.path.join(session_folder, output_filename), arcname=output_filename)
        memory_file.seek(0)

        return send_file(memory_file, download_name='split_tickets.zip', as_attachment=True)
    else:
        flash('Error processing files')
        return redirect(request.url)

def clear_session_folder():
    session_folder = session.get('session_folder')
    if session_folder and os.path.exists(session_folder):
        shutil.rmtree(session_folder)
        os.makedirs(session_folder)

def extract_zip(zip_path, extract_to_folder):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_folder)
    # Return a list of all extracted CSV file paths
    return [os.path.join(extract_to_folder, file) for file in os.listdir(extract_to_folder) if file.endswith('.csv')]

def process_files(file1_paths, file2_paths, names):
    # Process the first set of CSV files
    for file1_path in file1_paths:
        sort_and_divide_tickets(file1_path, names)

    # Process the second set of CSV files
    for file2_path in file2_paths:
        sort_and_divide_tickets(file2_path, names)

def sort_and_divide_tickets(input_csv_path, names):
    # Read and sort the CSV by ID
    df = pd.read_csv(input_csv_path)
    df.sort_values(by='ID', inplace=True)

    # Calculate the number of tickets per name
    tickets_per_name = len(df) // len(names)

    for i, name in enumerate(names):
        start_index = i * tickets_per_name
        end_index = start_index + tickets_per_name if i < len(names) - 1 else None

        # Slice the dataframe for the current name
        name_df = df.iloc[start_index:end_index]

        # Generate the output file path using os.path.join for better path handling
        output_file_path = os.path.join(session.get('session_folder'), f"{name.strip()}_tickets.csv")

        # Append data to the file, without headers
        name_df.to_csv(output_file_path, mode='a', index=False, header=False)

        # Manually append new lines for visual separation (optional)
        with open(output_file_path, 'a') as csv_file:
            csv_file.write('\n\n')

if __name__ == '__main__':
    app.run(debug=True)
