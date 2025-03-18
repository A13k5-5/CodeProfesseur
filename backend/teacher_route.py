# teacher_route.py
from flask import Blueprint, jsonify, request
from database import dbmanager
import sqlite3

bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')

@bp.route('/<string:teacher_id>/classrooms', methods=['GET'])
def get_teacher_classrooms(teacher_id):
    db = dbmanager()
    
    try:
        #check if the teacher exists?

        # Get all classrooms for the teacher
        classrooms = db.get_teacher_classrooms(teacher_id)
        result = []
        for classroom in classrooms:
            result.append({
                'name': classroom['name'],
                'class_id': classroom['class_id']
            })
        
        db.close()
        return jsonify(result)
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@bp.route('/<string:teacher_id>/questions', methods=['GET'])
def get_teacher_questions(teacher_id):
    db = dbmanager()
    
    try:
        #check if the teacher exists?

        #Get all questions for a specific teacher with failure rates
        result = []
        questions = db.get_teacher_question_id_and_names(teacher_id)
            
        for question in questions:  
            result.append({
                    'name': question['name'],
                    'failure_rate': db.calculate_failure_rate(question)
                })
            
        db.close()
        return jsonify(result)
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
 