import sqlite3

conn = sqlite3.connect('dochadzka.db')
c = conn.cursor()
users = [ (1,'Peto', 'priezvisko1',1),
          (2,'Palo', 'priezvisko2',2),
          (3,'Paula', 'priezvisko3',1)]

teach_lessons = [ (1,'PT','8PM', 'monday','AB3'),
          (2,'OS','10PM', 'monday','BC3'),
          (3,'AZA','12PM', 'monday','CD3')]


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS lessons(ID_lesson INTEGER PRIMARY KEY, name TEXT, Time TEXT, Day TEXT, Room TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS '
              'students(ID_student INTEGER PRIMARY KEY, Name TEXT,'
              ' Last_name TEXT,lesson INTEGER,FOREIGN KEY(lesson) REFERENCES lessons(ID_lesson))')
    #c.execute('CREATE TABLE IF NOT EXISTS groups(ID_group INTEGER, Description TEXT)')
    #ID_subject by sa malo vytvorit pri prepojeni s tabulkou subjects
    #Prepojenim tabuliek STUDENTS a GROUPS mala by sa vytvorit prepajacia tabulka STUDENTS-GROUPS
    #c.execute('CREATE TABLE IF NOT EXISTS subjects(ID_subject INTEGER, Subject_name TEXT)')

def data_entry(table_name,values):
    if table_name== "students":
        c.executemany("INSERT INTO students VALUES(?,?,?,?)",values)
        conn.commit()
    elif table_name== "lessons":
        c.executemany("INSERT INTO lessons VALUES(?,?,?,?,?)",values)
        conn.commit()

def delete_table(table_name):
    c.execute('DROP TABLE '+ table_name)
    conn.commit()

def print_table(table_name):
    c.execute('SELECT * FROM ' +table_name)
    data=c.fetchall()
    print(data)

def print_students_in_lesson():
    c.execute('SELECT students.Name FROM students JOIN lessons ON students.lesson=lessons.ID_lesson WHERE lessons.name="PT"')
    data=c.fetchall()
    print(data)


delete_table("students")
delete_table("lessons")
create_table()
data_entry("students",users)
data_entry("lessons",teach_lessons)
print_table("students")
print_table("lessons")
print_students_in_lesson()


c.close()
conn.close()
