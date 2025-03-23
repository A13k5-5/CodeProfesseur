#Adds a submission and gets the 
from flask import Blueprint, jsonify, request
from database import dbmanager
import sqlite3
import os
from question_route import get_student_submissions 

bp = Blueprint('submission' , __name__ , url_prefix='/api/submission')

@bp.route('/add_student_submission', methods=['POST'])
def add_student_submission():
    print("Entered")

    db = dbmanager()

    data = request.json
    print("Received data")
    if not data or 'user' not in data or 'question' not in data or 'text' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    print("Data is correct")
    student_submissions = get_student_submissions(data['question'], data['user'])
    submission_count = len(student_submissions)
    print("Got student submissions")
    path = save_student_submission(data['user'], data['question'], data['text'], submission_count)
    print("Got path")
    user_id = data['user']
    question = data['question']
    question_id = data['question_id']
    print(f"User Id: {user_id}\n Question Id: {question_id}")
    try:
        db.add_docker_result_to_database(path, 0, data['user'], data['question_id'])
        print("Added to docker")
        db.close()
        return jsonify({
            "message": "Submission added successfully", 
        }), 201
    except sqlite3.Error as e:
        db.close()
        print("Error somewhere", e)
        return jsonify({"error": f"Database error: {str(e)}"}), 500

def save_student_submission(student_id, question, submission, sub_num):
    base_dir = "student_submissions"
    student_dir = os.path.join(base_dir, student_id)
    if not os.path.exists(student_dir):
        os.makedirs(student_dir)
    
    question_dir = os.path.join(student_dir, question)
    if not os.path.exists(question_dir):
        os.makedirs(question_dir)
    
    file_path = os.path.join(question_dir, f"answer{sub_num}.txt")
    with open(file_path, "w") as file:
        file.write(submission)
    
    return file_path

    

#Gets the result for a specific question, sorting the students in last name alphabetical order
#Then the individual attempts are in chronological order
@bp.route('/results/<int:question_id>', methods=['GET'])
def get_student_results(question_id):
    db = dbmanager()
    
    try:
        # Get all submissions for this question
        submissions = db.get_question_submissions(question_id)
        
        result = []
        for submission in submissions:
            result.append({
                'first_name': submission['first_name'],
                'last_name': submission['last_name'],
                'is_accepted': submission['is_accepted'],
            })
        
        db.close()
        return jsonify(result)
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

