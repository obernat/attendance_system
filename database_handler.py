#!/usr/bin/env python3
import database as db

def create_students_database(teacher):
    students_list = []

    if teacher == None:
        return -1, None;

    for subject in teacher.subjects_list:
        for student in subject.student_list:
            students_list.append(db.Person(student.name, "--------------------"))


    return 1, students_list

def create_database_of_students(teacher):
    students_dict = {}

    if teacher == None:
        return -1, None;

    for subject in teacher.subjects_list:
        for student in subject.student_list:
            students_dict[student.name] = "--------------------"

    return 1, students_dict
