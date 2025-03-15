import sqlite3

class dbmanager:
    def __init__(self):
        self.conn = sqlite3.connect('professeur.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.conn.execute('PRAGMA foreign_keys = ON;')
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

    def add_question(self, name, content, json, diff, due):
        self.cursor.execute(f'''
        INSERT INTO question(name, content, input, output, difficulty, due_date) VALUES ("{name}", "{content}", "{json}", "{json}", "{diff}", "{due}")
        ''')
        self.conn.commit()

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

    def assign_question(self, question, classroom):
        self.cursor.execute(f'''
        INSERT INTO questionclassroom(question_id, classroom_id) VALUES ({question}, {classroom})
        ''')
        self.conn.commit()
    
    def get_user(self, mail, pwd):
        self.cursor.execute('''
        SELECT
            user.user_id, user.first_name, user.last_name, user.type, user.pwd_hash,
            classroom.class_id, classroom.teacher, classroom.name AS classroom_name,
            question.question_id, question.name AS question_name, question.content, question.input, question.output, question.difficulty, question.due_date,
            submission.submission_id, submission.path, submission.is_accepted, submission.date
        FROM user
        LEFT JOIN classroomstudent ON user.user_id = classroomstudent.student_id
        LEFT JOIN classroom ON classroomstudent.classroom_id = classroom.class_id
        LEFT JOIN questionclassroom ON classroom.class_id = questionclassroom.classroom_id
        LEFT JOIN question ON questionclassroom.question_id = question.question_id
        LEFT JOIN submission ON user.user_id = submission.user AND question.question_id = submission.question
        WHERE user.user_id = ? AND user.pwd_hash = ?
        ''', (mail, pwd))
        return self.cursor.fetchall()

    def get_user_classrooms(self, mail, pwd):
        print(f"Executing query with email: {mail}, pwd: {pwd}")
        self.cursor.execute('''
        SELECT
            classroom.name AS classroom_name
        FROM user
        LEFT JOIN classroomstudent ON user.user_id = classroomstudent.student_id
        LEFT JOIN classroom ON classroomstudent.classroom_id = classroom.class_id
        WHERE user.user_id = ? AND user.pwd_hash = ?
        ''', (mail, pwd))
        result = self.cursor.fetchall()
        print(f"Query result: {result}")
        return result

    #TODO: Submit function

    def purge(self):
        self.cursor.execute('DElETE FROM questionclassroom')
        self.cursor.execute('DElETE FROM classroomstudent')
        self.cursor.execute('DElETE FROM question')
        self.cursor.execute('DElETE FROM submission')
        self.cursor.execute('DElETE FROM classroom')
        self.cursor.execute('DElETE FROM user')

        self.conn.commit()

    def insert_examples(self):
        # Make sure the database is purged before, otherwise might throw error
        self.add_user("martin.benning@ucl.ac.uk", "Martin", "Benning", 1, "password123")
        self.add_user("alex.pison.24@ucl.ac.uk", "Alex", "Pison", 0, "verysecurepassword")
        self.add_classroom("martin.benning@ucl.ac.uk", "Design and Professional Skills")
        self.add_user_to_classroom("alex.pison.24@ucl.ac.uk", 1) # This is a bit dangerous
        self.add_question("Trivia", "What happened during the last Talk Tuah Podcast episode?", "jsontext", "hard", "2025-02-02")
        self.assign_question(1, 1) # This is a bit dangerous

    def close(self):
        self.conn.close()


man = dbmanager()
man.create_db()

man.purge()
man.insert_examples()

man.close()