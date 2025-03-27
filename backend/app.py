#Need to add JWT token
from flask import Flask, request, jsonify 
from flask_cors import CORS
from passlib.hash import bcrypt
from database import dbmanager
import classroom_route, teacher_route, question_route, submission_route
import sqlite3
import atexit
import queuemanager as subq
from database import dbmanager
import classroom_route, teacher_route, question_route, submission_route
import sqlite3
import re 


app = Flask(__name__)
CORS(app)

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Register blueprints
app.register_blueprint(classroom_route.bp)
app.register_blueprint(teacher_route.bp)
app.register_blueprint(question_route.bp)
app.register_blueprint(submission_route.bp)

db = dbmanager("professeur.db")

worker = subq.start_worker()

@app.route("/api/classrooms", methods=['POST'])
def return_classrooms():
    data = request.get_json()
    email = data.get('email')
    pwd = data.get('pwd')
    role = data.get('role')
    print(f"Received email: {email}, pwd: {pwd}")
    if int(role) == 1:
        result = []
        classrooms = db.get_teacher_classrooms(email)
        for classroom in classrooms:
            print(f"Class Id: {classroom[0]}")
            print(f"Class Name: {classroom[1]}")
            result.append({
                'class_name' : classroom[2] 
            })
        return jsonify(result)
    classrooms = db.get_user_classrooms(email, pwd)
    print(f"Classrooms: {classrooms}")
    return jsonify(classrooms)

@app.route("/api/user", methods=['POST'])
def get_user_details(): 
    data = request.get_json()
    email = data.get('email')
    pwd = data.get('pwd')
    print("Failed to receive json data")
    user = db.get_user_details(email, pwd)
    print("Can't access database")
    if user:
        print(jsonify(user))
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route("/api/classroom_id", methods=['POST'])
def get_classroom_id():
    data = request.get_json()
    class_name = data.get('classroom')
    
    if class_name:
        class_name = re.sub(r'[^a-zA-Z0-9\s]', '', class_name)

    print("Name received ", class_name)
    try:
        class_id = db.get_class_id(class_name)
        print("Class Id found is: ", class_id)
    except:
        print("Error in querying database")
    if class_id:
        return jsonify(class_id)
    else:
        return jsonify({"error": "class_id not found"}), 404

@app.route("/api/classroom/questions", methods=['POST'])
def get_student_questions():
    data = request.get_json()
    class_id = data.get('classId') #dict
    student_id = data.get('email')
    questions = db.get_class_questions(class_id)

    if questions:
        return jsonify(questions)
    else:
        return jsonify({"error":"Error getting class questions"}), 404

@app.route('/api/register_user', methods=['POST'])
def register_user():
    db = dbmanager("professeur.db")
    
    data = request.json
    if not data or 'user_id' not in data or 'first_name' not in data or 'last_name' not in data or 'type' not in data or 'password' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    if db.user_exists(data['user_id']):
        db.close()
        return jsonify({"error": "User already exists"}), 409
    
    hasher = bcrypt.using(rounds=11)
    password_hash = hasher.hash(data['password'])
    
    try:
        db.add_user(data['user_id'], data['first_name'], data['last_name'], data['type'], password_hash)
        db.close()
        return jsonify({"message": "User added successfully"}), 201
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": f"Database error: {str(e)}"}), 500


@app.route('/api/login', methods=['POST'])
def login():
    db = dbmanager('professeur.db')
    data = request.json
    
    if not data or 'user_id' not in data or 'password' not in data:
        return jsonify({"error": "Missing required field"}), 400
    
    if not db.user_exists(data['user_id']):
        db.close()
        return jsonify({"error": "User not found"}), 404
    
    user = db.get_user(data['user_id'])
    
    hasher = bcrypt.using(rounds=11)
    
    if hasher.verify(data['password'], user['pwd_hash']):
        db.close()
        return jsonify({"user_login_successful": True}), 200
    else:
        db.close()
        return jsonify({"error": "password does not match"}), 401
    
@atexit.register
def cleanup():
    subq.stop_worker()
    

if __name__ == '__main__':
    app.run(debug=True, port=8080)
