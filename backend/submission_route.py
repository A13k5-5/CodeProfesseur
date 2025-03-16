#Adds a submission and gets the 
from flask import Blueprint, jsonify, request
import sqlite3

bp = Blueprint('submission' , __name__ , url_prefix='/api/submission')

def get_db_connection():
    conn = sqlite3.connect('professeur.db')
    conn.row_factory = sqlite3.Row
    return conn


@bp.route('/add_student_submission', methods=['POST'])
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
    

#Gets the result for a specific question, sorting the students in last name alphabetical order
#Then the individual attempts are in chronological order
@bp.route('/results/<int:question_id>', methods=['GET'])
def get_student_results(question_id):
    conn = get_db_connection()
    try:
        # Get all submissions for this question
        submissions = conn.execute('''
            SELECT  s.is_accepted, s.date, u.user_id, u.first_name, u.last_name
            FROM submission s
            JOIN user u ON s.user = u.user_id
            WHERE s.question = ?
            ORDER BY u.last_name, u.first_name, s.date ASC
        ''', (question_id,)).fetchall()
        
        result = []
        for submission in submissions:
            result.append({
                'first_name': submission['first_name'],
                'last_name': submission['last_name'],
                'is_accepted': submission['is_accepted'],
            })
        
        conn.close()
        return jsonify(result)
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500