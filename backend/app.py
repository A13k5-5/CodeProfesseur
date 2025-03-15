from flask import Flask, jsonify, request
from flask_cors import CORS
from database import dbmanager

app = Flask(__name__)
CORS(app)

db = dbmanager()

@app.route("/api/classrooms", methods=['POST'])
def return_classrooms():
    data = request.get_json()
    email = data.get('email')
    pwd = data.get('id')
    print(f"Received email: {email}, pwd: {pwd}")
    classrooms = db.get_user_classrooms(email, pwd)
    print(f"Classrooms: {classrooms}")
    return jsonify(classrooms)

@app.route("/api/user", methods=['POST'])
def get_user(): 
    data = request.get_json()
    email = data.get('email')
    pwd = data.get('id')
    user = db.get_user(email, pwd)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=8080)