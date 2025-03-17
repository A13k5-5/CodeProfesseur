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
    if not data or 'name' not in data or 'content' not in data or 'input' not in data or 'output' not in data or 'difficulty' not in data or 'classroom_ids' not in data:
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
            data['input'], 
            data['output'], 
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


@bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    conn = get_db_connection()
    try:
        #Checks questionclassroom instead of question as each question
        #must be assigned to at least one classroom
        check_question_exists = conn.execute('''
        SELECT COUNT(*) as count
        FROM questionclassroom
        WHERE question_id = ?                                  
        ''', (question_id)).fetchone()

        if check_question_exists['count'] == 0:
            conn.close()
            return jsonify({"error": "question does not exist"}), 404
        
        question = conn.execute('''
        SELECT DISTINCT q.* FROM question q
        JOIN questionclassroom WHERE q.question_id = qc.question_id
        WHERE qc.question_id = ?
        ''', (question_id)).fetchall()

        conn.close()
        return jsonify({
                'question_id': question['question_id'],
                'name': question['name'],
                'content': question['content'],
                'input': question['input'],
                'output': question['output'],
                'difficulty': question['difficulty'],
                'due_date': question['due_date']
            })
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500