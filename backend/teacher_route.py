# teacher_route.py
from flask import Blueprint, jsonify, request
import sqlite3

bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')

def get_db_connection():
    conn = sqlite3.connect('professeur.db')
    conn.row_factory = sqlite3.Row
    return conn


@bp.route('/<string:teacher_id>/classrooms', methods=['GET'])
def get_teacher_classrooms(teacher_id):
    conn = get_db_connection()
    try:
        # Get all classrooms for the teacher
        classrooms = conn.execute('''
            SELECT * FROM classroom WHERE teacher = ?
        ''', (teacher_id,)).fetchall()
        
        result = []
        for classroom in classrooms:
            result.append({
                'name': classroom['name'],
                'class_id': classroom['class_id']
            })
        
        conn.close()
        return jsonify(result)
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@bp.route('/<string:teacher_id>/questions', methods=['GET'])
def get_teacher_questions(teacher_id):
    conn = get_db_connection()
    try:
        #Get all questions for a specific teacher with success rates
        result = []
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
                
            failure_rate = 0
            if total_submissions > 0:
                failure_rate = ((total_submissions - successful_submissions) / total_submissions) * 100
                
            result.append({
                    'name': question['name'],
                    'success_rate': round(failure_rate, 2)
                })
            
        conn.close()
        return jsonify(result)
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500