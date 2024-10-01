# Secure File Sharing API

## Project Structure

## Technologies Used

- **Flask**: Web framework for building the API
- **SMTP**: For sending email verifications
- **Werkzeug**: For secure filename handling
- **JWT**: For user authentication and authorization
- **SQLAlchemy**: ORM for database interaction
- **PostgreSQL**: Database management system (adjust based on your choice)

## Features

- User authentication (login and signup)
- Role-based access control (Ops and Client users)
- File upload functionality (limited to specific file types)
- File download functionality
- List all uploaded files for Client users
- Email verification for new users

## Requirements

-Python 3.x
-Flask
-Flask-Mail
-SQLAlchemy
-JWT
-Database (PostgreSQL)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/AnkitYadav2809/SecureFileSharingAPI.git1. Clone the repository:

2. Navigate to the Project directory:

   ```bash
   cd SecureFileSharingAPI
   
3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
4. Activate the virtual environment:

    For Windows:

    ```bash
    venv\Scripts\activate
    
5.Install the required packages:

  ```bash
  pip install -r requirements.txt
  ```

6.Set up your database (modify config.py to match your database settings).

7. Create the uploads directory:

  ```bash
  mkdir uploads
  ```
8. Run the application:
 ```bash
  mkdir uploads
  ```

Based on the README file structure you provided, here's how the API endpoints can be designed:

### API Endpoints Design

#### Authentication Endpoints

1. **User Login**
   - **Endpoint**: `POST /login`
   - **Description**: Authenticate a user and return a JWT token.
   - **Request Body**:
     ```json
     {
       "username": "<username>",
       "password": "<password>"
     }
     ```
   - **Response**:
     - **Success**: 
       ```json
       {
         "message": "Login successful",
         "token": "<JWT token>",
         "user_id":<user_id>
         
       }
       ```
     - **Failure**:
       ```json
       {
         "message": "Invalid username or password"
       }
       ```

2. **User Signup**
   - **Endpoint**: `POST /signup`
   - **Description**: Register a new user and send a verification email.
   - **Request Body**:
     ```json
     {
       "username": "<username>",
       "password": "<password>",
       "email": "<email>"
     }
     ```
   - **Response**:
     - **Success**: 
       ```json
       {
         "message": "Signup successful, verification email sent!"
       }
       ```
     - **Failure**:
       ```json
       {
         "message": "Username or email already exists"
       }
       ```

3. **Email Verification**
   - **Endpoint**: `GET /verify_email/<token>`
   - **Description**: Verify a user's email using a token.
   - **Response**:
     - **Success**: 
       ```json
       {
         "message": "Email verification successful"
       }
       ```
     - **Failure**:
       ```json
       {
         "message": "Invalid or expired token"
       }
       ```

#### File Management Endpoints

4. **File Upload**
   - **Endpoint**: `POST /upload`
   - **Description**: Allow Ops users to upload files (only .pptx, .docx, .xlsx).
   - **Request**: Form-data containing the file.
   - **Response**:
     - **Success**: 
       ```json
       {
         "message": "File uploaded successfully"
       }
       ```
     - **Failure**:
       ```json
       {
         "message": "Only pptx, docx, pdf and xlsx files are allowed"
       }
       ```

5. **File Download**
   - **Endpoint**: `GET /download/<int:file_id>`
   - **Description**: Allow Client users to download a file by its ID.
   - **Response**:
     - **Success**:
       ```json
       {
         "download-link": "<download URL>",
         "message": "success"
       }
       ```
     - **Failure**:
       ```json
       {
         "message": "File not found"
       }
       ```

6. **List Uploaded Files**
   - **Endpoint**: `GET /files`
   - **Description**: List all uploaded files for Client users.
   - **Response**:
     - **Success**:
       ```json
       {
         "files": [
           {
             "file_id": 1,
             "file_name": "example.pptx",
             "uploaded_by": "username"
           },
           ...
         ],
         "message": "Files retrieved successfully"
       }
       ```
     - **Failure**:
       ```json
       {
         "message": "No files found"
       }
       ```

