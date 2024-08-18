from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from vidToAud import process_conversion, convert_video_to_audio

from pdfFetch import extract_text_from_pdf




app = Flask(__name__)

# Enable CORS for all routes
CORS(app, origins='*')

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a model for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Define a model for File
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    file_url = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<File {self.filename}>'

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users])

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(username=data['username'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'username': new_user.username}), 201

def parse_api_response(api_response):
    sections = api_response.strip().split('\n\n')
    cards = []
    for section in sections:
        lines = section.split('\n')
        if len(lines) >= 6:
            joke = lines[0].replace('Joke ', '').strip(':')
            question = lines[1].replace('Question ', '').strip(':')
            options = {lines[i].split(':')[0].strip(): lines[i].split(':')[1].strip() for i in range(2, 6)}
            answer = lines[6].replace('Answer: ', '').strip()
            cards.append({
                'joke': joke,
                'question': question,
                'options': options,
                'answer': answer
            })
    return cards

@app.route('/api/cards', methods=['GET'])
def get_cards():
    api_response = """Your API response here..."""
    cards = parse_api_response(api_response)
    return jsonify(cards)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Uploading pdfs
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        # Extract text from the uploaded PDF
        transcript = extract_text_from_pdf(file_path)
        
        # Optionally, you can delete the file after processing
        os.remove(file_path)
        
        return jsonify({'transcript': transcript}), 200
    
    return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # List of accepted audio and video formats
    accepted_formats = ['.mp3', '.wav', '.ogg', '.m4a', '.mp4', '.mov', '.avi', '.mkv', '.flv']

    # Check if the file extension is in the list of accepted formats
    if file and any(file.filename.endswith(ext) for ext in accepted_formats):
        # Save file to the filesystem
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        file_url = f'/files/{file.filename}'
        
        # Convert video to audio if the uploaded file is a video
        if any(file.filename.endswith(ext) for ext in ['.mp4', '.mov', '.avi', '.mkv', '.flv']):
            audio_filename = f"{os.path.splitext(file.filename)[0]}.mp3"
            audio_path = os.path.join(UPLOAD_FOLDER, audio_filename)
            convert_video_to_audio(filename, audio_path)
            file_url = f'/files/{audio_filename}'
        
        # Save file metadata to the database
        new_file = File(filename=file.filename, file_url=file_url)
        db.session.add(new_file)
        db.session.commit()
        
        return jsonify({'message': 'File successfully uploaded', 'file_url': file_url}), 200
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/videos', methods=['GET'])
def get_videos():
    video_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(('.mp4', '.mov', '.avi', '.mkv', '.flv'))]
    return jsonify(video_files)

@app.route('/convert', methods=['POST'])
def convert_video():
    data = request.get_json()
    video_filename = data.get('video')
    if not video_filename:
        return jsonify({'error': 'No video selected'}), 400
    
    video_path = os.path.join(UPLOAD_FOLDER, video_filename)
    audio_filename = f"{os.path.splitext(video_filename)[0]}.mp3"
    audio_path = os.path.join(UPLOAD_FOLDER, audio_filename)
    
    process_conversion(video_path, audio_path)
    
    return jsonify({'message': 'Conversion completed!', 'audio_file': audio_filename})

@app.route('/files/<filename>')
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/files', methods=['GET'])
def get_files():
    files = File.query.all()
    return jsonify([{'id': file.id, 'filename': file.filename, 'file_url': file.file_url} for file in files])

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=8080)
