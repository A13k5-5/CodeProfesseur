import sqlite3

class dbmanager:
    def __init__(self):
        self.conn = sqlite3.connect('professeur.db')
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

    #TODO: Submit function

    def close(self):
        self.conn.close()

man = dbmanager()

man.create_db()
#man.add_user("tt@ucl.ac.uk", "sneens", "sejslfj", 0, "kshkdshfgkdfhgkdfgh")
#man.add_classroom("tt@ucl.ac.uk", "ROOM 1")
#man.add_user_to_classroom("tt@ucl.ac.uk", 1)

man.add_question("Q1", "a question...", "jsontext", "hard", "today")
man.assign_question(1,1)

man.close()