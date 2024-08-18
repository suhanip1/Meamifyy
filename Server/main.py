from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import requests
from memeTest import set_template_ids

app = Flask(__name__)
CORS(app, origins='*')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    file_url = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<File {self.filename}>'

class MemeTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<MemeTemplate {self.name}>'

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

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.mp3'):
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        file_url = f'/files/{file.filename}'
        
        new_file = File(filename=file.filename, file_url=file_url)
        db.session.add(new_file)
        db.session.commit()
        
        return jsonify({'message': 'File successfully uploaded', 'file_url': file_url}), 200
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/files/<filename>')
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/files', methods=['GET'])
def get_files():
    files = File.query.all()
    return jsonify([{'id': file.id, 'filename': file.filename, 'file_url': file.file_url} for file in files])


@app.route('/api/memes', methods=['GET'])
def get_memes():
    memes = MemeTemplate.query.all()
    return jsonify([{'id': meme.id, 'name': meme.name, 'url': meme.url} for meme in memes])

@app.route('/api/memify', methods=['GET'])
def memify():
    file_name = request.args.get('file_name')
    templates = set_template_ids(file_name)
    return jsonify([
        {
            'joke_id': template['id'],
            'joke': template['joke'],
            'joke_follow_up': template['joke-followUp'],
            'question': template['question'],
            'option_1': template['options']['Option 1'],
            'option_2': template['options']['Option 2'],
            'option_3': template['options']['Option 3'],
            'option_4': template['options']['Option 4'],
            'answer': template['answer'],
            'name': template['name'],
            'url': template['url']
        } for template in templates
    ])

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=8080)
