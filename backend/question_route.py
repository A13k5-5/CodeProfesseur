#cadd_Question in database has 5 parameters with 6 out
from flask import Blueprint, jsonify, request
from database import dbmanager
import sqlite3
from database import dbmanager

bp = Blueprint('question', __name__, url_prefix='/api/question')

@bp.route('/create', methods=['POST'])
def create_question():
    db = dbmanager()
    data = request.json
    if not data or 'name' not in data or 'content' not in data or 'inputoutput' not in data or 'difficulty' not in data or 'classroom_ids' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        input_data = data['inputoutput'].get('input', {})
        output_data = data['inputoutput'].get('output', {})
        db.add_question(data['name'], data['content'], input_data, output_data, data['difficulty'], data.get('due_date', None))
            
        # Get the ID of the question we just added
        question_id = db.conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        
        # Assign the question to classrooms
        for classroom_id in data['classroom_ids']:
            db.assign_question(question_id, classroom_id)
        
        db.close()
        return jsonify({
            "message": "Question created successfully",
            "question_id": question_id
        }), 201
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    db = dbmanager()
    
    try:
        if not db.question_exists(question_id):
            db.close()
            return jsonify({"error": "question does not exist"}), 404
        
        question = db.get_question(question_id)
        db.close()
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
        db.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500