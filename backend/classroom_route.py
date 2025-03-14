# classroom_route.py 
#get questions displays questions for students and teachers
#get classroom students displays all the stuents in a classroom

#NB: CHANGED STUDENT QUESTION VIEW TO INCLUDE DUE DATE, DELETED 'LAST ATTEMPT'
from flask import Blueprint, jsonify, request
import sqlite3

bp = Blueprint('classroom', __name__, url_prefix='/api/classroom')


def get_db_connection():
    conn = sqlite3.connect('professeur.db')
    conn.row_factory = sqlite3.Row
    return conn


@bp.route('/get_questions', methods=['GET'])
def get_questions():
    # Get parameters from the request
    option = request.args.get('option')
    teacher_id = request.args.get('teacher_id')
    classroom_id = request.args.get('classroom_id')
    student_id = request.args.get('student_id')
    
    # Validate parameters based on the option
    if option not in ['1', '2', '3']:
        return jsonify({"error": "Invalid option. Must be 1, 2, or 3"}), 400
    
    if option == '1' and not teacher_id:
        return jsonify({"error": "teacher_id is required for option 1"}), 400
    
    if option == '2' and not classroom_id:
        return jsonify({"error": "classroom_id is required for option 2"}), 400
    
    if option == '3' and (not classroom_id or not student_id):
        return jsonify({"error": "classroom_id and student_id are required for option 3"}), 400
    
    conn = get_db_connection()
    try:
        result = []
        
        # Option 1: Get all questions for a specific teacher with success rates
        if option == '1':
            # Get all questions for the teacher
            questions = conn.execute('''
                SELECT DISTINCT q.question_id, q.name
                FROM question q
                JOIN questionclassroom qc ON q.question_id = qc.question_id
                JOIN classroom c ON qc.classroom_id = c.class_id
                WHERE c.teacher = ?
            ''', (teacher_id,)).fetchall()
            
            for question in questions:
                # Calculate success rate
                submissions = conn.execute('''
                    SELECT COUNT(*) as total_submissions, SUM(is_accepted) as successful_submissions
                    FROM submission
                    WHERE question = ?
                ''', (question['question_id'],)).fetchone()
                
                total_submissions = submissions['total_submissions']
                successful_submissions = submissions['successful_submissions'] or 0
                
                success_rate = 0
                if total_submissions > 0:
                    success_rate = (successful_submissions / total_submissions) * 100
                
                result.append({
                    'name': question['name'],
                    'success_rate': round(success_rate, 2)
                })
        
        # Option 2: Get all questions for a specific classroom with success rates
        elif option == '2':
            # Get all questions for the classroom
            questions = conn.execute('''
                SELECT q.question_id, q.name
                FROM question q
                JOIN questionclassroom qc ON q.question_id = qc.question_id
                WHERE qc.classroom_id = ?
            ''', (classroom_id,)).fetchall()
            
            for question in questions:
                # Calculate success rate
                submissions = conn.execute('''
                    SELECT COUNT(*) as total_submissions, SUM(is_accepted) as successful_submissions
                    FROM submission
                    WHERE question = ?
                ''', (question['question_id'],)).fetchone()
                
                total_submissions = submissions['total_submissions']
                successful_submissions = submissions['successful_submissions'] or 0
                
                success_rate = 0
                if total_submissions > 0:
                    success_rate = (successful_submissions / total_submissions) * 100
                
                result.append({
                    'name': question['name'],
                    'success_rate': round(success_rate, 2)
                })
        
        # Option 3: Get all questions for a specific student in a specific classroom
        elif option == '3':
            # First check if student is in the classroom
            student_in_classroom = conn.execute('''
                SELECT COUNT(*) as count
                FROM classroomstudent
                WHERE classroom_id = ? AND student_id = ?
            ''', (classroom_id, student_id)).fetchone()
            
            if student_in_classroom['count'] == 0:
                conn.close()
                return jsonify({"error": "Student is not enrolled in this classroom"}), 404
            
            # Get all questions for the classroom

            questions = conn.execute('''
                SELECT q.question_id, q.name, q.due_date
                FROM question q
                JOIN questionclassroom qc ON q.question_id = qc.question_id
                WHERE qc.classroom_id = ?
            ''', (classroom_id,)).fetchall()
            
            for question in questions:
                # Get submission count for this student and question
                submission_count = conn.execute('''
                    SELECT COUNT(*) as count
                    FROM submission
                    WHERE question = ? AND user = ?
                ''', (question['question_id'], student_id)).fetchone()['count']
                
                result.append({
                    'name': question['name'],
                    'submission_count': submission_count,
                    'due_date': question['due_date']
                })

                # # Get the latest submission's is_accepted value
                # latest_submission = conn.execute('''
                #     SELECT is_accepted, date
                #     FROM submission
                #     WHERE question = ? AND user = ?
                #     ORDER BY date DESC
                #     LIMIT 1
                # ''', (question['question_id'], student_id)).fetchone()
                
                # latest_attempt_accepted = None
                # latest_attempt_date = None
                
                # if latest_submission:
                #     latest_attempt_accepted = latest_submission['is_accepted']
                #     latest_attempt_date = latest_submission['date']
                
                # result.append({
                #     'question_id': question['question_id'],
                #     'name': question['name'],
                #     'content': question['content'],
                #     'difficulty': question['difficulty'],
                #     'due_date': question['due_date'],
                #     'submission_count': submission_count,
                #     'latest_attempt_accepted': latest_attempt_accepted,
                #     'latest_attempt_date': latest_attempt_date
                # })


        
        conn.close()
        return jsonify(result)
    
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@bp.route('/<int:classroom_id>/students', methods=['GET'])
def get_classroom_students(classroom_id):
    conn = get_db_connection()
    try:
        # Get all students in the classroom and sorting by last name
        students = conn.execute('''
            SELECT u.user_id, u.first_name, u.last_name FROM user u
            JOIN classroomstudent cs ON u.user_id = cs.student_id
            WHERE cs.classroom_id = ? AND u.type = 0
            ORDER BY u.last_name, u.first_name
        ''', (classroom_id,)).fetchall()
        
        result = []
        for student in students:
            result.append({
                'first_name': student['first_name'],
                'last_name': student['last_name'],
                'user_id': student['user_id']
            })
        
        conn.close()
        return jsonify(result)
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500