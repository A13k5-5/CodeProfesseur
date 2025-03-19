#NB: CHANGED STUDENT QUESTION VIEW TO INCLUDE DUE DATE, DELETED 'LAST ATTEMPT'
from flask import Blueprint, jsonify
from database import dbmanager
import sqlite3
from database import dbmanager

bp = Blueprint('classroom', __name__, url_prefix='/api/classroom')

@bp.route('/<int:classroom_id>/questions', methods=['GET'])
def get_classroom_questions(classroom_id):
    db = dbmanager()

    try:
        result = []
        # Get all questions for the classroom
        questions = db.get_classroom_questions(classroom_id)

        for question in questions:
            result.append({
                'name': question['name'],
                'success_rate': db.calculate_failure_rate(question)
            })

        db.close()
        return jsonify(result)
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@bp.route('/<int:classroom_id>/questions/<string:student_id>', methods=['GET'])
def get_student_classroom_questions(classroom_id, student_id):
    db = dbmanager()

    try:
        result = []
        if not db.is_student_in_classroom(classroom_id, student_id):
            db.close()
            return jsonify({"error": "Student is not enrolled in this classroom"}), 404
        
        # Get all questions for the classroom
        questions = db.get_classroom_questions(classroom_id)

        for question in questions:
            result.append({
                'name': question['name'],
                'submission_count': db.number_of_submissions(question, student_id),
                'due_date': question['due_date']
            })

        db.close()
        return jsonify(result)
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@bp.route('/<int:classroom_id>/students', methods=['GET'])
def get_classroom_students(classroom_id):
    db = dbmanager()
    
    try:

        students = db.get_students_in_class(classroom_id)
        # Get all students in the classroom and sorting by last name
        students = db.get_users_in_classroom(classroom_id)
        result = []
        for student in students:
            result.append({
                'first_name': student[1],
                'last_name': student[2],
                'user_id': student[0]
            })
        
        db.close()
        return jsonify(result)
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500