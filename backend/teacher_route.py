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
        # Get all questions assigned to the teacher's classrooms
        questions = conn.execute('''
            SELECT DISTINCT q.* FROM question q
            JOIN questionclassroom qc ON q.question_id = qc.question_id
            JOIN classroom c ON qc.classroom_id = c.class_id
            WHERE c.teacher = ?
        ''', (teacher_id,)).fetchall()
        
        result = []
        for question in questions:
            result.append({
                'question_id': question['question_id'],
                'name': question['name'],
                'content': question['content'],
                'input': question['input'],
                'output': question['output'],
                'difficulty': question['difficulty'],
                'due_date': question['due_date']
            })
        
        conn.close()
        return jsonify(result)
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500