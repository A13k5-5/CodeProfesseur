#backend
# app.py
from flask import Flask, request, jsonify 
from flask_cors import CORS
import classroom_route, teacher_route, question_route
import sqlite3

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(classroom_route.bp)
app.register_blueprint(teacher_route.bp)
app.register_blueprint(question_route.bp)

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('professeur.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/api/add_user', methods=['POST'])
def add_user():
    data = request.json
    if not data or 'user_id' not in data or 'first_name' not in data or 'last_name' not in data or 'type' not in data or 'password' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = get_db_connection()
    # Check if user exists
    existing_user = conn.execute('SELECT user_id FROM user WHERE user_id = ?', 
                                (data['user_id'],)).fetchone()
    
    if existing_user:
        conn.close()
        return jsonify({"error": "User already exists"}), 409
    
    # Hash the password?
    # pwd_hash = hashlib.sha256(data['password'].encode()).hexdigest()
    
    try:
        conn.execute('INSERT INTO user (user_id, first_name, last_name, type, pwd_hash) VALUES (?, ?, ?, ?, ?)',
                     (data['user_id'], data['first_name'], data['last_name'], data['type'], data['pwd_hash']))
        conn.commit()
        conn.close()
        return jsonify({"message": "User added successfully"}), 201
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/api/get_user_password', methods=['POST'])
def get_user_password():
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    
    conn = get_db_connection()
    user = conn.execute('SELECT pwd_hash FROM user WHERE user_id = ?', 
                        (data['user_id'],)).fetchone()
    conn.close()
    
    if user:
        return jsonify({"pwd_hash": user['pwd_hash']})
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/api/add_student_submission', methods=['POST'])
def add_student_submission():
    data = request.json
    if not data or 'path' not in data or 'user' not in data or 'question' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = get_db_connection()
    try:
        
        conn.execute('''
            INSERT INTO submission (path, is_accepted, user, question, date) 
            VALUES (?, ?, ?, ?, datetime('now'))
        ''', (data['path'], data.get('is_accepted', 0), data['user'], data['question']))
        
        conn.commit()
        
        # Get the ID of the submission we just added
        submission_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        
        conn.close()
        return jsonify({
            "message": "Submission added successfully", 
            "submission_id": submission_id
        }), 201
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)