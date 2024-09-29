
from flask import jsonify
from database import get_database_session, File

def list_uploaded_files():
    session = get_database_session()
    
    # Retrieve all files from the database
    files = session.query(File).all()
    if not files:
        return jsonify({"message": "No files uploaded yet"}), 404
    
    file_list = [{"file_id": file.id, "file_name": file.file_name, "file_url": file.file_url} for file in files]
    
    return jsonify({"files": file_list}), 200
