# Added functions add_submission, get_question, question_exists, get_teacher_question_id_and_names,
# get_question_submissions, calculate_failure_rate
# Changed add_question parameters by splitting 'json' into 'input' and 'output'
# might need to add an integer id to the user table, otherwise the teacher's email will be in the url
# Is the submission_id autogenerated by the table, such that you don't need to INSERT INTO
import sqlite3
import datetime


class dbmanager:
    def __init__(self, filepath):
        self.conn = sqlite3.connect(filepath, check_same_thread=False)
        # Added this line so values can be accessed by column name
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.conn.commit()
    
    def disable_row_factory(self):
        self.conn.row_factory = None
        self.cursor = self.conn.cursor()
        self.conn.execute('PRAGMA foreign_keys = ON;')
        self.conn.commit()

    def create_db(self):
        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS user (
            user_id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            type INTEGER NOT NULL,
            pwd_hash TEXT NOT NULL
        )
        """
        )

        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS classroom (
            class_id INTEGER PRIMARY KEY,
            teacher TEXT NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (teacher) REFERENCES user(user_id)
        )
        """
        )

        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS submission (
            submission_id INTEGER PRIMARY KEY,
            path TEXT NOT NULL,
            is_accepted TEXT,
            user TEXT NOT NULL,
            question INTEGER NOT NULL,
            date TEXT,
            FOREIGN KEY (user) REFERENCES user(user_id),
            FOREIGN KEY (question) REFERENCES question(question_id)
        )
        """
        )

        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS question (
            question_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            content TEXT,
            input TEXT,
            output TEXT,
            difficulty TEXT NOT NULL,
            due_date TEXT
        )
        """
        )

        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS questionclassroom (
            question_id INTEGER NOT NULL,
            classroom_id INTEGER NOT NULL,
            PRIMARY KEY (question_id, classroom_id)
            FOREIGN KEY (question_id) REFERENCES question(question_id),
            FOREIGN KEY (classroom_id) REFERENCES classroom(class_id)
        )
        """
        )

        self.cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS classroomstudent (
            classroom_id INTEGER NOT NULL,
            student_id TEXT NOT NULL,
            PRIMARY KEY (classroom_id, student_id)
            FOREIGN KEY (classroom_id) REFERENCES classroom(class_id),
            FOREIGN KEY (student_id) REFERENCES user(user_id)
        )
        """
        )

        self.conn.commit()

    def add_user(self, mail, first, last, type, pwd):
        self.cursor.execute(
            f"""
        INSERT INTO user(user_id, first_name, last_name, type, pwd_hash) VALUES ("{mail}", "{first}", "{last}", {type}, "{pwd}")
        """
        )
        self.conn.commit()

    def get_user(self, user_id):
        return self.cursor.execute(
            """SELECT * FROM user WHERE user_id = ?""", (user_id,)
        ).fetchone()

    def user_exists(self, user_id):
        exists = self.cursor.execute(
            """SELECT user_id FROM user WHERE user_id = ?""", (user_id,)
        ).fetchone()
        if exists is None:
            return False
        else:
            return True

    def add_question(self, name, content, input, output, diff, due):
        self.cursor.execute(
            f"""
        INSERT INTO question(name, content, input, output, difficulty, due_date) VALUES ("{name}", "{content}", "{input}", "{output}", "{diff}", "{due}")
        """
        )
        self.conn.commit()

    def get_question(self, question_id):
        question = self.cursor.execute(
            """SELECT * FROM question q WHERE q.question_id = ?""", (question_id,)
        ).fetchone()
        return question

    def question_exists(self, question_id):
        exists = self.cursor.execute(
            """SELECT q.question_id FROM question q WHERE q.question_id = ?""",
            (question_id,),
        ).fetchone()
        if exists is None:
            return False
        else:
            return True

    def assign_question(self, question, classroom):
        self.cursor.execute(
            f"""
        INSERT INTO questionclassroom(question_id, classroom_id) VALUES ({question}, {classroom})
        """
        )
        self.conn.commit()
    
    def get_student_question_submissions(self, user_id, question_id):
        
        print(f"User Id in db: {user_id}")
        submissions = self.cursor.execute('''
            SELECT s.path, s.is_accepted, s.date
            FROM submission s
            JOIN user u on s.user = u.user_id
            JOIN question q on s.question = q.question_id
            WHERE s.user = ? AND s.question = ?
            ORDER BY s.date DESC 
        ''', (user_id, question_id,)).fetchall()
        return submissions

    def get_question_submissions(self, question_id):
        return self.cursor.execute(
            """
            SELECT  s.is_accepted, u.first_name, u.last_name, s.path
            FROM submission s
            JOIN user u ON s.user = u.user_id
            WHERE s.question = ?
            ORDER BY u.last_name, u.first_name, s.date ASC
        """,
            (question_id,),
        ).fetchall()
    
    def get_question_id(self, question_name):
        question = self.cursor.execute('''SELECT q.question_id FROM question q WHERE q.name = ?''', (question_name,)).fetchone()
        return question

    # Used to get all questions created by the teacher
    def get_teacher_question_id_and_names(self, teacher_id):
        return self.cursor.execute(
            """
                SELECT DISTINCT q.question_id, q.name
                FROM question q
                JOIN questionclassroom qc ON q.question_id = qc.question_id
                JOIN classroom c ON qc.classroom_id = c.class_id
                WHERE c.teacher = ?
            """,
            (teacher_id,),
        ).fetchall()

    def number_of_submissions(self, question, student_id):
        return self.cursor.execute(
            """SELECT COUNT(*) as count FROM submission WHERE question = ? AND user = ?""",
            (question["question_id"], student_id),
        ).fetchone()["count"]
    
    def get_num_submissions_in_class(self, student_id, class_id):
        return self.cursor.execute(
        """
            SELECT COUNT(*) as total_submissions
            FROM submission s
            JOIN questionclassroom qc ON s.question = qc.question_id
            WHERE qc.classroom_id = ? AND s.user = ? 
        """, (class_id, student_id),
        ).fetchone()["total_submissions"]

    def calculate_failure_rate(self, question):
        submissions = self.cursor.execute(
            """
                    SELECT COUNT(*) as total_submissions, SUM(is_accepted) as successful_submissions
                    FROM submission
                    WHERE question = ?
                """,
            (question["question_id"],),
        ).fetchone()

        total_submissions = submissions["total_submissions"]
        successful_submissions = submissions["successful_submissions"] or 0

        failure_rate = 100
        if total_submissions > 0:
            failure_rate = (
                (total_submissions - successful_submissions) / total_submissions
            ) * 100

        return round(failure_rate, 2)

    def add_classroom(self, teacher, name):
        self.cursor.execute(
            f"""
        INSERT INTO classroom(teacher, name) VALUES ("{teacher}", "{name}")
        """
        )
        self.conn.commit()

    def add_user_to_classroom(self, user, classroom):
        self.cursor.execute(
            f"""
        INSERT INTO classroomstudent(classroom_id, student_id) VALUES ({classroom}, "{user}")
        """
        )
        self.conn.commit()

    def get_teacher_classrooms(self, teacher_id):
        return self.cursor.execute(
            """SELECT * FROM classroom WHERE teacher = ?""", (teacher_id,)
        ).fetchall()

    def get_classroom_questions(self, classroom_id):
        return self.cursor.execute(
            """
                SELECT q.question_id, q.name, q.due_date
                FROM question q
                JOIN questionclassroom qc ON q.question_id = qc.question_id
                WHERE qc.classroom_id = ?
            """,
            (classroom_id,),
        ).fetchall()

    def get_users_in_classroom(self, classroom_id):
        return self.cursor.execute(
            """
            SELECT u.user_id, u.first_name, u.last_name FROM user u
            JOIN classroomstudent cs ON u.user_id = cs.student_id
            WHERE cs.classroom_id = ? AND u.type = 0
            ORDER BY u.last_name, u.first_name
        """,
            (classroom_id,),
        ).fetchall()

    def is_student_in_classroom(self, classroom_id, student_id):
        registered = self.cursor.execute(
            """SELECT cs.student_id FROM classroomstudent cs WHERE classroom_id = ? AND student_id = ?""",
            (classroom_id, student_id),
        ).fetchone()
        if registered is None:
            return False
        else:
            return True

    # TODO: Submit function

    # Is the submission id automatically generated by the db?
    def add_docker_result_to_database(
        self, submission_path, is_accepted, user, question
    ):
        self.cursor.execute(
            f"""
        INSERT INTO submission(path, is_accepted, user, question, date) 
        VALUES ("{submission_path}", "{is_accepted}", "{user}", "{question}", "{datetime.date.today()}")
        """
        )
        self.conn.commit()

    def purge(self):
        self.cursor.execute("DELETE FROM questionclassroom")
        self.cursor.execute("DELETE FROM classroomstudent")
        self.cursor.execute("DELETE FROM submission")
        self.cursor.execute("DELETE FROM classroom")
        self.cursor.execute("DELETE FROM question")
        self.cursor.execute("DELETE FROM user")
        
    def get_total_submissions_for_question(self, question_id):
        total_submissions = self.cursor.execute('''
            SELECT COUNT(*) as count
            FROM submission
            WHERE question = ?
        ''', (question_id,)).fetchone()
        
        return total_submissions['count'] if total_submissions else 0
        
        
    # Ammar's Functions

    def get_user_details(self, mail, pwd):
        self.disable_row_factory()
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
        ''', (mail, pwd,))
        result = self.cursor.fetchall()
        return result

    def get_user_classrooms(self, mail, pwd):
        self.disable_row_factory()
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
    
    def get_class_questions(self, class_id):
        self.disable_row_factory()
        self.cursor.execute('''
        SELECT questionclassroom.question_id
        FROM questionclassroom
        WHERE questionclassroom.classroom_id = ?
        ''', (class_id,))
        question_ids = self.cursor.fetchall()

        if not question_ids:
            return []
        question_ids = [q_id[0] for q_id in question_ids]
        print(question_ids)

        self.cursor.execute('''
        SELECT * FROM question
        WHERE question_id IN ({})
        '''.format(','.join('?' * len(question_ids))), question_ids)
        questions = self.cursor.fetchall()
        return questions
    
    def get_class_id(self, classroom_name):
        try: self.disable_row_factory()
        except:
            print("Error in disabling row factory")
        try:
            self.cursor.execute('''
            SELECT classroom.class_id
            FROM classroom
            WHERE classroom.name = ?
            ''', (classroom_name,))
            class_id_result = self.cursor.fetchone()
        except:
            print("Error in query")
        if not class_id_result:
            return []
        class_id = class_id_result[0]
        return class_id


        self.conn.commit()

    def insert_examples(self):
        import json

        # Define the test cases as Python objects
        test_input = [[1], [2], [3], [4], [5], [6], [7]]
        test_output = [1, 1, 1, 1, 1, 1, 1]

        # Convert to JSON strings
        input_json = json.dumps(test_input)
        output_json = json.dumps(test_output)

        # Make sure the database is purged before, otherwise might throw error
        self.add_user("martin.benning@ucl.ac.uk", "Martin", "Benning", 1, "password123")
        self.add_user(
            "alex.pison.24@ucl.ac.uk", "Alex", "Pison", 0, "verysecurepassword"
        )
        self.add_classroom("martin.benning@ucl.ac.uk", "Design and Professional Skills")
        self.add_user_to_classroom(
            "alex.pison.24@ucl.ac.uk", 1
        )  # This is a bit dangerous
        self.add_question(
            "Example question",
            "Write a function answer that takes an integer and always returns 1",
            input_json,
            output_json,
            "easy",
            "2025-02-02",
        )
        self.assign_question(1, 1)  # This is a bit dangerous

    def close(self):
        self.conn.close()



# Run the main function using python database.py
# to reset the database into its example configuration
if __name__ == "__main__":
    man = dbmanager("professeur.db")
    man.create_db()

    man.purge()
    man.insert_examples()
    man.purge()
    man.insert_examples()

    man.close()
