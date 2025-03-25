#NB: CHANGED STUDENT QUESTION VIEW TO INCLUDE DUE DATE, DELETED 'LAST ATTEMPT'
from flask import Blueprint, jsonify
from database import dbmanager
import sqlite3

bp = Blueprint('classroom', __name__, url_prefix='/api/classroom')

@bp.route('/<int:classroom_id>/questions', methods=['GET'])
def get_classroom_questions(classroom_id):
    db = dbmanager("professeur.db")

    try:
        print("This is called")
        result = []
        # Get all questions for the classroom
        questions = db.get_classroom_questions(classroom_id)

        for question in questions:
            submission_count = db.get_total_submissions_for_question(question['question_id'])
            result.append({
                'name': question['name'],
                'due_date': question['due_date'],
                'success_rate': db.calculate_failure_rate(question),
                'submission_count': submission_count
            })

        db.close()
        return jsonify(result)
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@bp.route('/<int:classroom_id>/questions/<string:student_id>', methods=['GET'])
def get_student_classroom_questions(classroom_id, student_id):
    db = dbmanager('professeur.db')

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
    db = dbmanager("professeur.db")
    
    try:
        # Get all students in the classroom and sorting by last name
        students = db.get_users_in_classroom(classroom_id)
        result = []
        for student in students:
            result.append({
                'first_name': student['first_name'],
                'last_name': student['last_name'],
                'user_id': student['user_id']
            })
        
        db.close()
        return jsonify(result)
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500