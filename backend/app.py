#Need to add JWT token
from flask import Flask, request, jsonify 
from flask_cors import CORS
import classroom_route, teacher_route, question_route, submission_route
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(classroom_route.bp)
app.register_blueprint(teacher_route.bp)
app.register_blueprint(question_route.bp)
app.register_blueprint(submission_route.bp)

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('professeur.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/api/register_user', methods=['POST'])
def register_user():
    data = request.json
    if not data or 'user_id' not in data or 'first_name' not in data or 'last_name' not in data or 'type' not in data or 'password' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    # Check if user exists
    existing_user = conn.execute('SELECT user_id FROM user WHERE user_id = ?', 
                                (data['user_id'])).fetchone()
    
    if existing_user:
        conn.close()
        return jsonify({"error": "User already exists"}), 409
    
    password_hash = generate_password_hash(data['password'], method='pbkdf2:sha256')
    
    try:
        conn.execute('INSERT INTO user (user_id, first_name, last_name, type, pwd_hash) VALUES (?, ?, ?, ?, ?)',
                     (data['user_id'], data['first_name'], data['last_name'], data['type'], password_hash))
        conn.commit()
        conn.close()
        return jsonify({"message": "User added successfully"}), 201
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'user_id' not in data or 'pwd_hash' not in data:
        return jsonify({"error": "Missing required field"}), 400
    
    conn = get_db_connection()
    password = conn.execute('SELECT pwd_hash FROM user WHERE user_id = ?', 
                        (data['user_id'],)).fetchone()
    conn.close()
    
    if password is None:
        return jsonify({"error": "User not found"}), 404
    
    if check_password_hash(password, data['pwd_hash']):
        return jsonify({"user_login_successful": True}), 200
    else:
        return jsonify({"error": "password does not match"}), 401
    

if __name__ == '__main__':
    app.run(debug=True)