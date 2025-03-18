#Need to add JWT token
from flask import Flask, request, jsonify 
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from database import dbmanager
import classroom_route, teacher_route, question_route, submission_route
import sqlite3


app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(classroom_route.bp)
app.register_blueprint(teacher_route.bp)
app.register_blueprint(question_route.bp)
app.register_blueprint(submission_route.bp)


@app.route('/api/register_user', methods=['POST'])
def register_user():
    db = dbmanager()
    
    data = request.json
    if not data or 'user_id' not in data or 'first_name' not in data or 'last_name' not in data or 'type' not in data or 'password' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    if db.user_exists(data['user_id']):
        db.close()
        return jsonify({"error": "User already exists"}), 409
    
    password_hash = generate_password_hash(data['password'], method='pbkdf2:sha256')
    
    try:
        db.add_user(data['user_id'], data['first_name'], data['last_name'], data['type'], password_hash)
        db.close()
        return jsonify({"message": "User added successfully"}), 201
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/api/login', methods=['POST'])
def login():
    db = dbmanager()
    data = request.json
    if not data or 'user_id' not in data or 'pwd_hash' not in data:
        return jsonify({"error": "Missing required field"}), 400
    
    if not db.user_exists(data['user_id']):
        db.close()
        return jsonify({"error": "User not found"}), 404
    
    user = db.get_user(data['user_id'])
    
    if check_password_hash(user['pwd_hash'], data['pwd_hash']):
        db.close()
        return jsonify({"user_login_successful": True}), 200
    else:
        db.close()
        return jsonify({"error": "password does not match"}), 401
    

if __name__ == '__main__':
    app.run(debug=True)