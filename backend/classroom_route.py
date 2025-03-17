#classroom_route.py 
#get questions displays questions for students and teachers
#Teacher view shows failure rate, student view shows number of attempts per question

#NB: CHANGED STUDENT QUESTION VIEW TO INCLUDE DUE DATE, DELETED 'LAST ATTEMPT'
from flask import Blueprint, jsonify, request
from database import dbmanager
import sqlite3

bp = Blueprint('classroom', __name__, url_prefix='/api/classroom')

@bp.route('/<int:classroom_id>/questions', methods=['GET'])
@bp.route('/<int:classroom_id>/questions/<int:user_id>', methods=['GET'])
def get_questions(classroom_id, student_id=None):
    db = dbmanager()

    try:
        result = []
        #If they are on the student page checking the classroom, check to make sure they are enrolled
        #Also check if they exist?
        if student_id is not None:
            student_in_classroom = db.is_student_in_classroom(classroom_id, student_id)
            if not student_in_classroom:
                db.close()
                return jsonify({"error": "Student is not enrolled in this classroom"}), 404
        
        # Get all questions for the classroom
        questions = db.get_classroom_questions(classroom_id)

        if student_id is None:    #Teacher view
            for question in questions:
                result.append({
                    'name': question['name'],
                    'success_rate': db.calculate_failure_rate(question)
                })
        else:    #Student view
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
        # Get all students in the classroom and sorting by last name
        students = db.get_classroom_students(classroom_id)
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