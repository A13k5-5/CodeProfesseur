import unittest
import json
import os
import sqlite3
from app import app

class FlaskTestApi(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Create a test database connection
        self.conn = sqlite3.connect('professeur.db')
        self.conn.row_factory = sqlite3.Row
        
        # Sample data for testing
        self.test_user = {
            "user_id": "test_user_id",
            "first_name": "Test",
            "last_name": "User",
            "type": 0,  # 0 for student, 1 for teacher
            "pwd_hash": "test_password_hash"
        }
        
        self.test_question = {
            "name": "Test Question",
            "content": "Write a function that adds two numbers.",
            "difficulty": 1,
            "classroom_ids": []  # Will be populated in setup
        }
        
        self.test_submission = {
            "path": "/path/to/submission.py",
            "user": "test_user_id",
            "question": 1,  # Will be updated with actual question ID if needed
            "is_accepted": 1
        }
        
        # Get a sample classroom for testing
        cursor = self.conn.cursor()
        classroom = cursor.execute('SELECT class_id FROM classroom LIMIT 1').fetchone()
        if classroom:
            self.test_classroom_id = classroom['class_id']
            self.test_question["classroom_ids"] = [self.test_classroom_id]
        else:
            self.test_classroom_id = None
        
        # Get a sample teacher for testing
        teacher = cursor.execute('SELECT user_id FROM user WHERE type = 1 LIMIT 1').fetchone()
        if teacher:
            self.test_teacher_id = teacher['user_id']
        else:
            self.test_teacher_id = None
        
        # Get a sample student for testing
        student = cursor.execute('SELECT user_id FROM user WHERE type = 0 LIMIT 1').fetchone()
        if student:
            self.test_student_id = student['user_id']
        else:
            self.test_student_id = None
        
        # Get a sample question for testing
        question = cursor.execute('SELECT question_id FROM question LIMIT 1').fetchone()
        if question:
            self.test_question_id = question['question_id']
            self.test_submission["question"] = self.test_question_id
        else:
            self.test_question_id = None
            
        cursor.close()

    def tearDown(self):
        # Clean up test data
        cursor = self.conn.cursor()
        
        # Remove test user if it was created
        cursor.execute('DELETE FROM user WHERE user_id = ?', (self.test_user["user_id"],))
        
        # Remove test submission if it was created
        cursor.execute('DELETE FROM submission WHERE path = ?', (self.test_submission["path"],))
        
        self.conn.commit()
        cursor.close()
        self.conn.close()

    # app.py Tests
    def test_add_user(self):
        response = self.client.post('/api/add_user', 
                                     data=json.dumps(self.test_user),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'User added successfully')
        
        # Test duplicate user
        response = self.client.post('/api/add_user', 
                                     data=json.dumps(self.test_user),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 409)
        
        # Test missing fields
        incomplete_user = {"user_id": "incomplete_user"}
        response = self.client.post('/api/add_user', 
                                     data=json.dumps(incomplete_user),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_user_password(self):
        # First add the test user
        self.client.post('/api/add_user', 
                          data=json.dumps(self.test_user),
                          content_type='application/json')
        
        # Test getting password hash
        response = self.client.post('/api/get_user_password', 
                                     data=json.dumps({"user_id": self.test_user["user_id"]}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['pwd_hash'], self.test_user["pwd_hash"])
        
        # Test non-existent user
        response = self.client.post('/api/get_user_password', 
                                     data=json.dumps({"user_id": "nonexistent_user"}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 404)
        
        # Test missing fields
        response = self.client.post('/api/get_user_password', 
                                     data=json.dumps({}),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_add_student_submission(self):
        # First add the test user if not already present
        self.client.post('/api/add_user', 
                          data=json.dumps(self.test_user),
                          content_type='application/json')
        
        # Test adding submission
        response = self.client.post('/api/add_student_submission', 
                                     data=json.dumps(self.test_submission),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('submission_id', data)
        
        # Test missing fields
        incomplete_submission = {"path": "/path/to/file.py"}
        response = self.client.post('/api/add_student_submission', 
                                     data=json.dumps(incomplete_submission),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

    # classroom_route.py Tests
    def test_get_questions_option1(self):
        if self.test_teacher_id:
            response = self.client.get(f'/api/classroom/get_questions?option=1&teacher_id={self.test_teacher_id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
            if len(data) > 0:
                self.assertIn('name', data[0])
                self.assertIn('success_rate', data[0])
        else:
            self.skipTest("No teacher ID available for testing")

    def test_get_questions_option2(self):
        if self.test_classroom_id:
            response = self.client.get(f'/api/classroom/get_questions?option=2&classroom_id={self.test_classroom_id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
            if len(data) > 0:
                self.assertIn('name', data[0])
                self.assertIn('success_rate', data[0])
        else:
            self.skipTest("No classroom ID available for testing")

    def test_get_questions_option3(self):
        if self.test_classroom_id and self.test_student_id:
            response = self.client.get(f'/api/classroom/get_questions?option=3&classroom_id={self.test_classroom_id}&student_id={self.test_student_id}')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
            if len(data) > 0:
                self.assertIn('name', data[0])
                self.assertIn('submission_count', data[0])
                self.assertIn('due_date', data[0])
        else:
            self.skipTest("No classroom ID or student ID available for testing")

    def test_get_questions_invalid_option(self):
        response = self.client.get('/api/classroom/get_questions?option=4')
        self.assertEqual(response.status_code, 400)

    def test_get_classroom_students(self):
        if self.test_classroom_id:
            response = self.client.get(f'/api/classroom/{self.test_classroom_id}/students')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
            if len(data) > 0:
                self.assertIn('first_name', data[0])
                self.assertIn('last_name', data[0])
                self.assertIn('user_id', data[0])
        else:
            self.skipTest("No classroom ID available for testing")

    # question_route.py Tests
    def test_create_question(self):
        if self.test_classroom_id:
            # Update classroom_ids with a valid classroom ID
            self.test_question["classroom_ids"] = [self.test_classroom_id]
            
            response = self.client.post('/api/question/create', 
                                         data=json.dumps(self.test_question),
                                         content_type='application/json')
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            self.assertIn('question_id', data)
            
            # Clean up the created question
            try:
                cursor = self.conn.cursor()
                question_id = data['question_id']
                cursor.execute('DELETE FROM questionclassroom WHERE question_id = ?', (question_id,))
                cursor.execute('DELETE FROM question WHERE question_id = ?', (question_id,))
                self.conn.commit()
                cursor.close()
            except sqlite3.Error:
                pass
        else:
            self.skipTest("No classroom ID available for testing")
        
        # Test missing fields
        incomplete_question = {"name": "Incomplete Question"}
        response = self.client.post('/api/question/create', 
                                     data=json.dumps(incomplete_question),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_student_results(self):
        if self.test_question_id:
            response = self.client.get(f'/api/question/{self.test_question_id}/results')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
            if len(data) > 0:
                self.assertIn('submission_id', data[0])
                self.assertIn('path', data[0])
                self.assertIn('is_accepted', data[0])
                self.assertIn('date', data[0])
                self.assertIn('user_id', data[0])
                self.assertIn('first_name', data[0])
                self.assertIn('last_name', data[0])
        else:
            self.skipTest("No question ID available for testing")

    # teacher_route.py Tests
    def test_get_teacher_classrooms(self):
        if self.test_teacher_id:
            response = self.client.get(f'/api/teacher/{self.test_teacher_id}/classrooms')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
            if len(data) > 0:
                self.assertIn('name', data[0])
                self.assertIn('class_id', data[0])
        else:
            self.skipTest("No teacher ID available for testing")

    def test_get_teacher_questions(self):
        if self.test_teacher_id:
            response = self.client.get(f'/api/teacher/{self.test_teacher_id}/questions')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
            if len(data) > 0:
                self.assertIn('question_id', data[0])
                self.assertIn('name', data[0])
                self.assertIn('content', data[0])
                self.assertIn('input', data[0])
                self.assertIn('output', data[0])
                self.assertIn('difficulty', data[0])
                self.assertIn('due_date', data[0])
        else:
            self.skipTest("No teacher ID available for testing")

if __name__ == '__main__':
    unittest.main()