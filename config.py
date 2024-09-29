
from flask import Flask
from flask_mail import Mail
import secrets

app = Flask(__name__)


secret_key = secrets.token_hex(32)
app.config['SECRET_KEY'] = secret_key  # For token generation

# Initialize Flask-Mail
mail = Mail(app)
