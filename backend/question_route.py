# question_route.py - Need to change student results to display each students results
#, check if data should include checking for input and output
from flask import Blueprint, jsonify, request
import sqlite3

bp = Blueprint('question', __name__, url_prefix='/api/question')

def get_db_connection():
    conn = sqlite3.connect('professeur.db')
    conn.row_factory = sqlite3.Row
    return conn


@bp.route('/create', methods=['POST'])
def create_question():
    data = request.json
    if not data or 'name' not in data or 'content' not in data or 'difficulty' not in data or 'classroom_ids' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = get_db_connection()
    try:
        # Insert the question
        conn.execute('''
            INSERT INTO question (name, content, input, output, difficulty, due_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'], 
            data['content'], 
            data.get('input', ''), 
            data.get('output', ''), 
            data['difficulty'], 
            data.get('due_date', None)
        ))
        
        # Get the ID of the question we just added
        question_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        
        # Assign the question to classrooms
        for classroom_id in data['classroom_ids']:
            conn.execute('''
                INSERT INTO questionclassroom (question_id, classroom_id)
                VALUES (?, ?)
            ''', (question_id, classroom_id))
        
        conn.commit()
        conn.close()
        return jsonify({
            "message": "Question created successfully",
            "question_id": question_id
        }), 201
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@bp.route('/<int:question_id>/results', methods=['GET'])
def get_student_results(question_id):
    conn = get_db_connection()
    try:
        # Get all submissions for this question
        submissions = conn.execute('''
            SELECT s.submission_id, s.path, s.is_accepted, s.date, u.user_id, u.first_name, u.last_name
            FROM submission s
            JOIN user u ON s.user = u.user_id
            WHERE s.question = ?
            ORDER BY u.last_name, u.first_name, s.date DESC
        ''', (question_id,)).fetchall()
        
        result = []
        for submission in submissions:
            result.append({
                'submission_id': submission['submission_id'],
                'path': submission['path'],
                'is_accepted': submission['is_accepted'],
                'date': submission['date'],
                'user_id': submission['user_id'],
                'first_name': submission['first_name'],
                'last_name': submission['last_name']
            })
        
        conn.close()
        return jsonify(result)
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500