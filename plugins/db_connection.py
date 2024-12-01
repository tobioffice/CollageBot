import sqlite3

con: sqlite3.Connection = sqlite3.connect('students.db')
cur: sqlite3.Cursor = con.cursor()


def student_info_by_rollno(rollno: str):
    # print(rollno)
    stu = cur.execute("SELECT * FROM students WHERE rollno = ?", (rollno,))
    # print(stu)
    stu = [s for s in stu][0]

    return stu


def student_info_by_section(section):
    stu = cur.execute("SELECT * FROM students WHERE section = ?", (section,))
    return [s for s in stu]


def register_student(UserId):
    a = cur.execute('INSERT INTO tg_users (id) VALUES (?)', (UserId,))
    con.commit()


def is_student_registered(UserId):
    student = cur.execute(
        'SELECT id FROM tg_users WHERE id = ?', (UserId,)
    ).fetchone()
    return bool(student)
