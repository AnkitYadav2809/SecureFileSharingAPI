from flask import request, jsonify
from werkzeug.security import check_password_hash
import jwt
import datetime
from database import get_database_session, User
from config import app
def login_user():
    session = get_database_session()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = session.query(User).filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        # Generate a Bearer token
        token = jwt.encode({
            'sub': user.id,  # Store user ID as 'sub'
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration time
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({"message": "Login successful", "user_id": user.id, "token": token}), 200
    
    return jsonify({"message": "Invalid credentials"}), 401
