from database import get_database_session
import jwt
from config import mail, app 
from flask import request, jsonify
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from database import get_database_session, User
from database import User
from register import serializer

def verify(token):
    try:
        # Deserialize or decode the token to get the email
        email = serializer.loads(token, salt='email-confirmation', max_age=3600)
    except SignatureExpired:
        return jsonify({"message": "The token has expired."}), 400
    except BadSignature:
        return jsonify({"message": "Invalid token."}), 400

    # Check if the user exists in the database
    session = get_database_session()
    user = session.query(User).filter_by(email=email).first()

    if user is None:
        return jsonify({"message": "User not found."}), 404

    # Mark the user as verified
    user.is_verified = True
    session.commit()

    return jsonify({"message": "Email verified successfully!"}), 200