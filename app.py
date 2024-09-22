import os
import json
from flask import Flask, request, jsonify
from datetime import datetime, timezone
import uuid
import re
from loguru import logger
from werkzeug.utils import secure_filename
from database import setup_database, session, Upload, User

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
LOGS_FOLDER = 'logs'
FLASK_APP_LOGS_FOLDER = os.path.join(LOGS_FOLDER, 'flask_app')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure the logs folder exists at startup
os.makedirs(LOGS_FOLDER, exist_ok=True)
os.makedirs(FLASK_APP_LOGS_FOLDER, exist_ok=True)

# Configure logging with loguru
logger.add(os.path.join(FLASK_APP_LOGS_FOLDER, 'flask_app.log'), rotation='1 day', retention='5 days', level='DEBUG')

# Function to ensure upload and output directories exist
def ensure_directories_exist():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def generate_uid():
    return str(uuid.uuid4())

def extract_timestamp(filename):
    pattern = r'_(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}\.\d+)'
    match = re.search(pattern, filename)
    if match:
        timestamp_str = match.group(1)
        try:
            return datetime.strptime(timestamp_str, '%Y-%m-%dT%H-%M-%S.%f').replace(tzinfo=timezone.utc)
        except ValueError:
            return None
    return None

@app.route('/upload', methods=['POST'])
def upload_file():
    ensure_directories_exist()  # Ensure directories exist before file operation
    try:
        logger.info("Starting upload_file function...")  # Log function start

        file = request.files.get('file')
        email = request.form.get('email')

        if not file:
            error_msg = 'No file provided in the request'
            logger.error(error_msg)
            return jsonify({'error': 'No file provided in the request'}), 400

        filename = secure_filename(file.filename)
        uid = generate_uid()
        timestamp = datetime.now(timezone.utc).isoformat()
        timestamp_formatted = timestamp.replace(':', '-')
        timestamp_part = timestamp_formatted.split('+')[0]

        new_filename = f"{os.path.splitext(filename)[0]}_{timestamp_part}_{uid}{os.path.splitext(filename)[1]}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

        user = None
        if email:
            user = session.query(User).filter_by(email=email).first()
            if not user:
                user = User(email=email)
                session.add(user)
                session.commit()

        new_upload = Upload(uid=uid, filename=new_filename, status='pending', user_id=user.id if user else None)
        session.add(new_upload)
        session.commit()

        logger.info("File uploaded successfully.")  # Log successful upload

        return jsonify({'uid': uid, 'status': 'File uploaded successfully'}), 200
    except Exception as e:
        session.rollback()
        error_msg = f"Failed to upload file: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': f"Failed to upload file: {str(e)}"}), 500

@app.route('/status', methods=['GET'])
def get_status():
    ensure_directories_exist()  # Ensure directories exist before checking status
    try:
        logger.info("Starting get_status function...")  # Log function start

        uid = request.args.get('uid')

        if not uid:
            error_msg = 'UID not provided'
            logger.error(error_msg)
            return jsonify({'error': 'UID not provided'}), 400

        upload = session.query(Upload).filter_by(uid=uid).first()

        if not upload:
            return jsonify({'status': 'not found', 'filename': None, 'timestamp': "Timestamp not found",
                            'explanation': 'No upload exists with the given UID'}), 404

        if upload.finish_time:
            output_file_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{upload.uid}.json")
            if os.path.exists(output_file_path):
                with open(output_file_path, 'r') as output_file:
                    explanation = json.load(output_file)
                logger.info(f"File explained successfully: {output_file_path}")
                return jsonify({
                    'status': 'done',
                    'filename': upload.filename,
                    'timestamp': upload.upload_time.isoformat(),
                    'explanation': explanation
                }), 200
            else:
                return jsonify({
                    'status': 'done',
                    'filename': upload.filename,
                    'timestamp': upload.upload_time.isoformat(),
                    'explanation': 'Output file not found'
                }), 200
        else:
            return jsonify({
                'status': 'pending',
                'filename': upload.filename,
                'timestamp': upload.upload_time.isoformat(),
                'explanation': None
            }), 200
    except Exception as e:
        error_msg = f"Failed to get status: {str(e)}"
        logger.error(error_msg)
        return jsonify({'error': f"Failed to get status: {str(e)}"}), 500

@app.route('/history', methods=['GET'])
def get_history():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = session.query(User).filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    uploads = session.query(Upload).filter_by(user_id=user.id).all()
    history = [
        {
            'uid': upload.uid,
            'filename': upload.filename,
            'upload_time': upload.upload_time,
            'status': upload.status,
            'finish_time': upload.finish_time,
            'error_message': upload.error_message
        } for upload in uploads
    ]

    return jsonify(history), 200

if __name__ == '__main__':
    setup_database()
    logger.info("Flask app started.")
    app.run(debug=True, use_reloader=False)  # Disable Flask reloader
    logger.info("Flask app ended.")
