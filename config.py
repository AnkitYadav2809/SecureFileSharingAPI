
from flask import Flask
from flask_mail import Mail
import secrets

app = Flask(__name__)

# Flask-Mail configuration (update these values with your own email service credentials)
app.config['MAIL_SERVER']='live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'api'
app.config['MAIL_PASSWORD'] = 'fecf3f0f320f40b18663a76222c9aecb'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'sy19072003@gmail.com'  # Default sender email
secret_key = secrets.token_hex(32)
app.config['SECRET_KEY'] = secret_key  # For token generation

# Initialize Flask-Mail
mail = Mail(app)
