from flask import request, jsonify, url_for
from werkzeug.security import generate_password_hash
from database import get_database_session
from database import User
import jwt
import datetime
from config import mail, app  # Assuming you have configured Flask-Mail and your app
from itsdangerous import URLSafeTimedSerializer
import smtplib
import secrets
from email.message import EmailMessage

app.config['SECRET_KEY'] = secrets.token_hex(32)

# Create a serializer for generating tokens
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

server=smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login('YOUR MAIL','YOUR PASSWORD')


def generate_verification_token(email):
    token = jwt.encode({
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def send_verification_email(email, token):
    verification_link = url_for('verify_email', token=token, _external=True)
    # print(verification_link)
    to_mail=email
    from_mail='YOUR MAIL'
    msg=EmailMessage()
    msg['Subject']='VERIFICATION MAIL'
    msg['From']=from_mail
    msg['To']=to_mail
    msg.set_content(f'Please click the link to verify your email: {verification_link}')
    server.send_message(msg)
    print("Email Sent!")

def signup_user():
    session = get_database_session()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role', 'Client')  # Default to 'Client' if not specified

    # Validate the role
    if role not in ['Ops', 'Client']:
        return jsonify({"message": "Invalid role. Must be 'Ops' or 'Client'."}), 400

    # Check if username or email already exists
    if session.query(User).filter_by(username=username).first() is not None:
        return jsonify({"message": "Username already exists"}), 400
    if session.query(User).filter_by(email=email).first() is not None:
        return jsonify({"message": "Email already exists"}), 400

    # Create new user
    new_user = User(
        username=username,
        password_hash=generate_password_hash(password),
        email=email,
        role=role,  # Set the role based on the request
        is_verified=False  # Initially set to False
    )
    session.add(new_user)
    session.commit()

    # Generate verification token and send verification email
    token = serializer.dumps(email, salt='email-confirmation')
    send_verification_email(email, token)

    return jsonify({"message": "Signup successful, verification email sent!"}), 201

