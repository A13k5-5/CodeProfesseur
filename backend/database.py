#might need to add an integer id to the user table, otherwise the teacher's email will be in the url
from passlib.hash import bcrypt
import sqlite3

class dbmanager:
    def __init__(self):
        self.conn = sqlite3.connect('professeur.db')
        #Added this line so values can be accessed by column name
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.cursor.execute('PRAGMA foreign_keys = ON;')
        self.conn.commit()

    def create_db(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            user_id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            type INTEGER NOT NULL,
            pwd_hash TEXT NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS classroom (
            class_id INTEGER PRIMARY KEY,
            teacher TEXT NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (teacher) REFERENCES user(user_id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS submission (
            submission_id INTEGER PRIMARY KEY,
            path TEXT NOT NULL,
            is_accepted INTEGER DEFAULT 0,
            user TEXT NOT NULL,
            question INTEGER NOT NULL,
            date TEXT,
            FOREIGN KEY (user) REFERENCES user(user_id),
            FOREIGN KEY (question) REFERENCES question(question_id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS question (
            question_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            content TEXT,
            input TEXT,
            output TEXT,
            difficulty TEXT NOT NULL,
            due_date TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS questionclassroom (
            question_id INTEGER NOT NULL,
            classroom_id INTEGER NOT NULL,
            PRIMARY KEY (question_id, classroom_id)
            FOREIGN KEY (question_id) REFERENCES question(question_id),
            FOREIGN KEY (classroom_id) REFERENCES classroom(class_id)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS classroomstudent (
            classroom_id INTEGER NOT NULL,
            student_id TEXT NOT NULL,
            PRIMARY KEY (classroom_id, student_id)
            FOREIGN KEY (classroom_id) REFERENCES classroom(class_id),
            FOREIGN KEY (student_id) REFERENCES user(user_id)
        )
        ''')

        self.conn.commit()

    def add_user(self, mail, first, last, type, pwd):
        self.cursor.execute(f'''
        INSERT INTO user(user_id, first_name, last_name, type, pwd_hash) VALUES ("{mail}", "{first}", "{last}", {type}, "{pwd}")
        ''')
        self.conn.commit()

    def get_user(self, user_id):
        return self.cursor.execute('''SELECT * FROM user WHERE user_id = ?''', (user_id,)).fetchone()
    
    def user_exists(self, user_id):
        exists = self.cursor.execute('''SELECT user_id FROM user WHERE user_id = ?''', (user_id,)).fetchone()
        if exists is None:
            return False
        else:
            return True
    
    def add_question(self, name, content, input, output, diff, due):
        self.cursor.execute(f'''
        INSERT INTO question(name, content, input, output, difficulty, due_date) VALUES ("{name}", "{content}", "{input}", "{output}", "{diff}", "{due}")
        ''')
        self.conn.commit()

    def get_question(self,question_id):
        question = self.cursor.execute('''SELECT * FROM question q WHERE q.question_id = ?''', (question_id,)).fetchone()
        return question
    
    def question_exists(self, question_id):
        exists = self.cursor.execute('''SELECT q.question_id FROM question q WHERE q.question_id = ?''', (question_id,)).fetchone()
        if exists is None:
            return False
        else:
            return True
        
    def assign_question(self, question, classroom):
        self.cursor.execute(f'''
        INSERT INTO questionclassroom(question_id, classroom_id) VALUES ({question}, {classroom})
        ''')
        self.conn.commit()

    def get_question_submissions(self, question_id):
        return self.cursor.execute('''
            SELECT  s.is_accepted, u.first_name, u.last_name
            FROM submission s
            JOIN user u ON s.user = u.user_id
            WHERE s.question = ?
            ORDER BY u.last_name, u.first_name, s.date ASC
        ''', (question_id,)).fetchall()

    #Used to get all questions created by the teacher
    def get_teacher_question_id_and_names(self, teacher_id):
        return self.cursor.execute('''
                SELECT DISTINCT q.question_id, q.name
                FROM question q
                JOIN questionclassroom qc ON q.question_id = qc.question_id
                JOIN classroom c ON qc.classroom_id = c.class_id
                WHERE c.teacher = ?
            ''', (teacher_id,)).fetchall()
    
    def number_of_submissions(self, question, student_id):
        return self.cursor.execute('''SELECT COUNT(*) as count FROM submission WHERE question = ? AND user = ?''', (question['question_id'], student_id)).fetchone()['count']
    
    def calculate_failure_rate(self, question):
        submissions = self.cursor.execute('''
                    SELECT COUNT(*) as total_submissions, SUM(is_accepted) as successful_submissions
                    FROM submission
                    WHERE question = ?
                ''', (question['question_id'],)).fetchone()
                
        total_submissions = submissions['total_submissions']
        successful_submissions = submissions['successful_submissions'] or 0
                
        failure_rate = 100
        if total_submissions > 0:
            failure_rate = ((total_submissions - successful_submissions) / total_submissions) * 100
        
        return round(failure_rate,2)

    def add_classroom(self, teacher, name):
        self.cursor.execute(f'''
        INSERT INTO classroom(teacher, name) VALUES ("{teacher}", "{name}")
        ''')
        self.conn.commit()

    def add_user_to_classroom(self, user, classroom):
        self.cursor.execute(f'''
        INSERT INTO classroomstudent(classroom_id, student_id) VALUES ({classroom}, "{user}")
        ''')
        self.conn.commit()

    def get_teacher_classrooms(self, teacher_id):
        return self.cursor.execute('''SELECT * FROM classroom WHERE teacher = ?''', (teacher_id,)).fetchall()
     
    def get_classroom_questions(self, classroom_id):
        return self.cursor.execute('''
                SELECT q.question_id, q.name, q.due_date
                FROM question q
                JOIN questionclassroom qc ON q.question_id = qc.question_id
                WHERE qc.classroom_id = ?
            ''', (classroom_id,)).fetchall()

    def get_users_in_classroom(self, classroom_id):
        return self.cursor.execute('''
            SELECT u.user_id, u.first_name, u.last_name FROM user u
            JOIN classroomstudent cs ON u.user_id = cs.student_id
            WHERE cs.classroom_id = ? AND u.type = 0
            ORDER BY u.last_name, u.first_name
        ''', (classroom_id,)).fetchall()
    
    def is_student_in_classroom(self, classroom_id, student_id):
        registered = self.cursor.execute('''SELECT cs.student_id FROM classroomstudent cs WHERE classroom_id = ? AND student_id = ?''', (classroom_id, student_id)).fetchone()
        if registered is None:
            return False
        else:
            return True

    #TODO: Submit function


    #Is the submission id automatically generated by the db?
    def add_docker_result_to_database(self,path, is_accepted, user, question):
        self.cursor.execute(f'''
        INSERT INTO submission(path, is_accepted, user, question, date) 
        VALUES ("{path}", "{is_accepted}", "{user}", "{question}", datetime('now'))
        ''')
        self.conn.commit()
        
    def purge(self):
        self.cursor.execute('DELETE FROM questionclassroom')
        self.cursor.execute('DELETE FROM classroomstudent')
        self.cursor.execute('DELETE FROM submission')
        self.cursor.execute('DELETE FROM question')
        self.cursor.execute('DELETE FROM classroom')
        self.cursor.execute('DELETE FROM user')

        self.conn.commit()

    def insert_examples(self):
    
        self.add_user("martin.benning@ucl.ac.uk", "Martin", "Benning", 1, "password123")
        self.add_user("alex.pison.24@ucl.ac.uk", "Alex", "Pison", 0, "verysecurepassword")
        # Make sure the database is purged before, otherwise might throw error
        self.add_classroom("martin.benning@ucl.ac.uk", "Design and Professional Skills")
        self.add_user_to_classroom("alex.pison.24@ucl.ac.uk", 1) # This is a bit dangerous
        self.add_question("Trivia", "What happened during the last Talk Tuah Podcast episode?", "input","output", "hard", "2025-02-02")
        self.assign_question(1, 1) # This is a bit dangerous

    def close(self):
        self.conn.close()


man = dbmanager()
man.create_db()

man.purge()
man.insert_examples()

man.close()