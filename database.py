class Teacher:
    def __init__(self):
        self.subjects_list = []


class Subject:
    def __init__(self, name, sid, student_list, is_active=1):
        self.name = name
        self.sid = sid
        self.student_list = student_list
        self.is_active = is_active


class Student:
    def __init__(self, name, cv_string, table_id, attendance, stud_and_group):
        self.name = name
        self.cv_string = cv_string
        self.table_id = table_id
        self.attendance = attendance
        self.study, self.group = self.parse_study_and_group(stud_and_group)

    def parse_study_and_group(self, study_and_group):
        group = study_and_group[:study_and_group.find("s")].lstrip("c")
        study = study_and_group[study_and_group.find(
            "s") + 1:study_and_group.find("k")]

        return study, group


class Person:
    def __init__(self, name, isic):
        self.name = name
        self.isic = isic
