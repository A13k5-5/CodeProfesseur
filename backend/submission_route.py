#Adds a submission and gets the 
from flask import Blueprint, jsonify, request
from database import dbmanager
import sqlite3

import queuemanager as subq

bp = Blueprint('submission' , __name__ , url_prefix='/api/submission')

@bp.route('/add_student_submission', methods=['POST'])
def add_student_submission():
    db = dbmanager('professeur.db')

    data = request.json
    if not data or 'path' not in data or 'user' not in data or 'question' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        # db.add_docker_result_to_database(data['path'], data.get('is_accepted', 0), data['user'], data['question'])
        # db.close()

        subq.add_submission(data['path'], data['user'], data['question'])

        return jsonify({
            "message": "Submission added successfully", 
        }), 201
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    

#Gets the result for a specific question, sorting the students in last name alphabetical order
#Then the individual attempts are in chronological order
@bp.route('/results/<int:question_id>', methods=['GET'])
def get_student_results(question_id):
    db = dbmanager('professeur.db')
    
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