# from flask import Flask, request,jsonify
# from login import login_user
# from upload_file import upload_file
# from download_file import download_file
# from list_file import list_uploaded_files
# from flask_mail import Mail
# from verification import verify
# from config import app
# from functools import wraps
# from database import get_database_session, User
# import jwt
# # Helper function to check user roles
# def role_required(role):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             session = get_database_session()
#             auth_header = request.headers.get('Authorization')
#             if not auth_header or not auth_header.startswith('Bearer '):
#                 return jsonify({"message": "Authorization header is missing or invalid"}), 401

#             token = auth_header.split(" ")[1]
#             try:
#                 decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
#                 user_id = decoded_token['sub']
#                 print(f"Decoded user ID: {user_id}")

#                 user = session.query(User).filter_by(id=user_id).first()
#                 if not user:
#                     return jsonify({"message": "User not found"}), 404
                
#                 if user.role != role:
#                     return jsonify({"message": "Access forbidden: incorrect user role"}), 403

#                 # Pass user information to the route function if needed
#                 return f(*args, user=user, **kwargs)
#             except jwt.ExpiredSignatureError:
#                 return jsonify({"message": "Token has expired"}), 403
#             except jwt.InvalidTokenError:
#                 return jsonify({"message": "Invalid token"}), 403
#             except Exception as e:
#                 print(f"Unexpected error: {str(e)}")  # Log any unexpected errors
#                 return jsonify({"message": "Access forbidden: invalid token or user not found"}), 403

#         return decorated_function
#     return decorator


# @app.route('/login', methods=['POST'])
# def login():
#     response = login_user()
#     return response

# @app.route('/signup', methods=['POST'])
# def signup():
#     from register import signup_user
#     return signup_user()

# @app.route('/verify_email/<token>', methods=['GET'])
# def verify_email(token):
#     return verify(token)

# @app.route('/upload', methods=['POST'])
# @role_required('Ops')  # Restrict this route to Ops users only
# def upload(user):
#     return upload_file(user)

# @app.route('/download/<int:file_id>', methods=['GET'])
# @role_required('Client')  # Restrict this route to Client users only
# def download(file_id):
#     return download_file(file_id)

# @app.route('/files', methods=['GET'])
# @role_required('Client')  # Restrict this route to Client users only
# def list_files():
#     return list_uploaded_files()

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request, jsonify
from login import login_user
from upload_file import upload_file
from download_file import download_file
from list_file import list_uploaded_files
from flask_mail import Mail
from verification import verify
from config import app
from database import get_database_session, User
import jwt

# Helper function to extract user from token and check the role
def check_user_role(required_role):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, jsonify({"message": "Authorization header is missing or invalid"}), 401

    token = auth_header.split(" ")[1]
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = decoded_token['sub']

        session = get_database_session()
        user = session.query(User).filter_by(id=user_id).first()

        if not user:
            return None, jsonify({"message": "User not found"}), 404

        # Check if the user role matches the required role
        if user.role != required_role:
            return None, jsonify({"message": f"Access forbidden: {required_role} role required"}), 403

        return user, None, None  # Return user object if role matches
    except jwt.ExpiredSignatureError:
        return None, jsonify({"message": "Token has expired"}), 403
    except jwt.InvalidTokenError:
        return None, jsonify({"message": "Invalid token"}), 403
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Log the error
        return None, jsonify({"message": "Access forbidden: invalid token or user not found"}), 403


@app.route('/login', methods=['POST'])
def login():
    response = login_user()
    return response

@app.route('/signup', methods=['POST'])
def signup():
    # Clients can sign up, Ops users can't
    auth_header = request.headers.get('Authorization')
    if auth_header:
        user, error_response, status_code = check_user_role('Client')
        if error_response:
            return error_response, status_code
    from register import signup_user
    return signup_user()

@app.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    # Only Clients can verify their email
    auth_header = request.headers.get('Authorization')
    if auth_header:
        user, error_response, status_code = check_user_role('Client')
        if error_response:
            return error_response, status_code
    return verify(token)

@app.route('/upload', methods=['POST'])
def upload():
    # Only Ops users can upload files
    user, error_response, status_code = check_user_role('Ops')
    if error_response:
        return error_response, status_code
    return upload_file(user)

@app.route('/download/<int:file_id>', methods=['GET'])
def download(file_id):
    # Only Clients can download files
    user, error_response, status_code = check_user_role('Client')
    if error_response:
        return error_response, status_code
    return download_file(file_id)

@app.route('/files', methods=['GET'])
def list_files():
    # Only Clients can list files
    user, error_response, status_code = check_user_role('Client')
    if error_response:
        return error_response, status_code
    return list_uploaded_files()


if __name__ == '__main__':
    app.run(debug=True)
