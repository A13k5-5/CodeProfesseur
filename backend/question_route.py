#cadd_Question in database has 5 parameters with 6 out
from flask import Blueprint, jsonify, request
from database import dbmanager
import sqlite3

bp = Blueprint('question', __name__, url_prefix='/api/question')

@bp.route('/create', methods=['POST'])
def create_question():
    print("Create Question is called")
    db = dbmanager("professeur.db")
    data = request.json

    
    try:
        input_data = data['input']
        output_data = data['output']
        db.add_question(data['name'], data['content'], input_data, output_data, data['difficulty'], data.get('due_date', None))
            
        # Get the ID of the question we just added
        question_id = db.conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        
        # Assign the question to classrooms
        db.assign_question(question_id, data['classroom_ids'])
        
        db.close()
        return jsonify({
            "message": "Question created successfully",
            "question_id": question_id
        }), 201
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@bp.route('/<string:question_name>', methods=['GET'])
def get_question_id(question_name):
    db = dbmanager("professeur.db")
    print("Get question id is called")
    if not question_name:
        return
    try:
        question = db.get_question_id(question_name)
        print("Question id in backend is", question['question_id'])
        db.close()
        return jsonify({
                'question_id': question['question_id']
            })
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    db = dbmanager("professeur.db")
    
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
@bp.route('/<int:question_id>/<string:student_id>', methods=['GET'])
def get_student_submissions(question_id, student_id):
    db = dbmanager("professeur.db")
    try:
        if not db.question_exists(question_id):
            db.close()
            return jsonify({"error": "question does not exist"}), 404
        print(f"Question Id: {question_id}")
        print(f"Student Id: {student_id}")
        submissions = db.get_student_question_submissions(student_id, question_id)

        db.close()
        if submissions:
            print(submissions)
        if not submissions:
            return jsonify({"status": "No submissions yet"})
        
        result = []
        for submission in submissions:
            result.append({
                'submission_path': submission['path'],
                'is_accepted': submission['is_accepted'],
                'date': submission['date'],
                'code': get_submitted_code(submission['path'])
            })
        return jsonify(result)
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

def get_submitted_code(submission_path):
    code = submission_path
    try:
        with open(submission_path, "r") as file:
            code = file.read()
    except:
        print("Error in reading file")
    return code
