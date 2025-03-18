import unittest
import json
import app
from database import dbmanager

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        self.app.testing = True
        
        # Set up a test database
        self.db = dbmanager()
        self.db.create_db()
        self.db.purge()  # Clear all data
        
        # Insert test data
        self.db.add_user("test.teacher@example.com", "Test", "Teacher", 1, "password123")
        self.db.add_user("test.student@example.com", "Test", "Student", 0, "student123")
        self.db.add_classroom("test.teacher@example.com", "Test Class")
        self.class_id = self.db.conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        self.db.add_user_to_classroom("test.student@example.com", self.class_id)
        self.db.add_question("Test Question", "Test content", "test input", "test output", "medium", "2025-04-01")
        self.question_id = self.db.conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        self.db.assign_question(self.question_id, self.class_id)
        self.db.close()

    def tearDown(self):
        # Clean up after the test
        # db = dbmanager()
        # db.purge()
        # db.close()
        None

    # App routes tests
    def test_register_user(self):
        response = self.app.post('/api/register_user', 
                                 data=json.dumps({
                                     'user_id': 'new.user@example.com',
                                     'first_name': 'New',
                                     'last_name': 'User',
                                     'type': 0,
                                     'password': 'newpassword'
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'User added successfully')

    def test_register_user_missing_fields(self):
        response = self.app.post('/api/register_user', 
                                 data=json.dumps({
                                     'user_id': 'incomplete.user@example.com',
                                     'first_name': 'Incomplete'
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_success(self):
        # First we need to get the actual password hash
        db = dbmanager()
        user = db.conn.execute('SELECT pwd_hash FROM user WHERE user_id = ?', 
                               ('test.teacher@example.com',)).fetchone()
        pwd_hash = user['pwd_hash']
        print(f"pwd_hash = {pwd_hash}")
        db.close()
        
        response = self.app.post('/api/login', 
                                 data=json.dumps({
                                     'user_id': 'test.teacher@example.com',
                                     'pwd_hash': 'password123'  # Plain text password in this test
                                 }),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('user_login_successful', False))

    def test_login_failure(self):
        response = self.app.post('/api/login', 
                                 data=json.dumps({
                                     'user_id': 'test.teacher@example.com',
                                     'pwd_hash': 'wrongpassword'
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 401)

    # Classroom route tests
    def test_get_classroom_questions_teacher_view(self):
        response = self.app.get(f'/api/classroom/{self.class_id}/questions')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        if data:  # If there are questions in the response
            self.assertIn('name', data[0])
            self.assertIn('success_rate', data[0])

    def test_get_classroom_questions_student_view(self):
        response = self.app.get(f'/api/classroom/{self.class_id}/questions/test.student@example.com')
        print(f"response = {response}")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        if data:  # If there are questions in the response
            self.assertIn('name', data[0])
            self.assertIn('submission_count', data[0])
            self.assertIn('due_date', data[0])

    def test_get_classroom_students(self):
        response = self.app.get(f'/api/classroom/{self.class_id}/students')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        if data:  # If there are students in the response
            self.assertIn('first_name', data[0])
            self.assertIn('last_name', data[0])
            self.assertIn('user_id', data[0])

    # Teacher route tests
    def test_get_teacher_classrooms(self):
        response = self.app.get('/api/teacher/test.teacher@example.com/classrooms')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        if data:  # If there are classrooms in the response
            self.assertIn('name', data[0])
            self.assertIn('class_id', data[0])

    def test_get_teacher_questions(self):
        response = self.app.get('/api/teacher/test.teacher@example.com/questions')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        if data:  # If there are questions in the response
            self.assertIn('name', data[0])
            self.assertIn('failure_rate', data[0])

    # Question route tests
    def test_create_question(self):
        response = self.app.post('/api/question/create',
                                 data=json.dumps({
                                     'name': 'New Test Question',
                                     'content': 'New test content',
                                     'inputoutput': {'input': 'test input', 'output': 'test output'},
                                     'difficulty': 'easy',
                                     'due_date': '2025-05-01',
                                     'classroom_ids': [self.class_id]
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('question_id', data)
        self.assertEqual(data['message'], 'Question created successfully')

    def test_get_question(self):
        response = self.app.get(f'/api/question/{self.question_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test Question')
        self.assertEqual(data['content'], 'Test content')
        self.assertEqual(data['difficulty'], 'medium')

    # Submission route tests
    def test_add_student_submission(self):
        response = self.app.post('/api/submission/add_student_submission',
                                 data=json.dumps({
                                     'path': '/test/path',
                                     'is_accepted': 1,
                                     'user': 'test.student@example.com',
                                     'question': self.question_id
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Submission added successfully')

    def test_get_student_results(self):
        # First add a submission so we have data to retrieve
        self.app.post('/api/submission/add_student_submission',
                      data=json.dumps({
                          'path': '/test/path',
                          'is_accepted': 1,
                          'user': 'test.student@example.com',
                          'question': self.question_id
                      }),
                      content_type='application/json')
        
        response = self.app.get(f'/api/submission/results/{self.question_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        if data:  # If there are submissions in the response
            self.assertIn('first_name', data[0])
            self.assertIn('last_name', data[0])
            self.assertIn('is_accepted', data[0])

    # Error cases and edge cases
    def test_nonexistent_classroom(self):
        response = self.app.get('/api/classroom/9999/questions')  # Using a non-existent classroom ID
        # Since the API doesn't explicitly check if the classroom exists, it might return an empty list
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])  # Should be an empty list

    def test_nonexistent_question(self):
        response = self.app.get('/api/question/9999')  # Using a non-existent question ID
        self.assertEqual(response.status_code, 404)

    def test_invalid_json(self):
        response = self.app.post('/api/register_user', 
                                 data="This is not valid JSON",
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()