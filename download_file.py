
# from flask import jsonify, send_file
# from database import get_database_session, File
# import os

# def download_file(file_id):
#     session = get_database_session()
    
#     file = session.query(File).filter_by(id=file_id).first()
#     if not file:
#         return jsonify({"message": "File not found"}), 404
    
#     file_path = file.file_url
#     if not os.path.exists(file_path):
#         return jsonify({"message": "File does not exist on server"}), 404
    
#     return send_file(file_path, as_attachment=True)
from flask import request, jsonify, send_file
from database import get_database_session, File
import os
from config import app

def download_file(file_id):
    session = get_database_session()
    file_record = session.query(File).filter_by(id=file_id).first()

    if not file_record:
        return jsonify({"message": "File not found"}), 404

    # Assuming the uploaded files are stored in the 'uploads' directory
    file_path = file_record.file_url

    # Check if the file exists
    if not os.path.exists(file_path):
        return jsonify({"message": "File does not exist"}), 404

    # Generate a download link (you can customize this URL structure as needed)
    download_link = f"{request.url_root}download-file/{file_record.id}"

    return jsonify({
        "download-link": download_link,
        "message": "success"
    }), 200
