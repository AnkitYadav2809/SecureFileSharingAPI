from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
from database import get_database_session, File
import jwt
from config import app

UPLOAD_FOLDER = 'uploads'  # Define your upload folder
ALLOWED_EXTENSIONS = {'.pptx', '.docx', '.xlsx','.pdf'}  # Define allowed file extensions

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and os.path.splitext(filename)[1] in ALLOWED_EXTENSIONS

def upload_file(user):
    session = get_database_session()

    # Check if the upload folder exists, if not, create it
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not allowed_file(filename):
        return jsonify({"message": "Only pptx, docx, and xlsx files are allowed"}), 400

    file.save(file_path)  # This will now succeed if the 'uploads' folder exists

    new_file = File(
        file_name=filename,
        file_url=file_path,
        uploaded_by=user.id,  # The user object is already passed from api.py
        file_type=file.content_type
    )
    session.add(new_file)
    session.commit()

    return jsonify({"message": "File uploaded successfully"}), 201
