import re


class Teacher:
    def __init__(self):
        self.subjects_list = []


class Subject:
    def __init__(self, name, sid, student_list, is_active=1):
        self.name = name
        #self.name = name.replace("&nbsp;"," ")
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
        match = "podrobne=([0-9]+);"
        result = re.search(match, study_and_group, re.DOTALL)
        if result:
            group = result.group(1)
        else:
            group = ""

        match = "studium=([0-9]+);"
        result = re.search(match, study_and_group, re.DOTALL)
        if result:
            study = result.group(1)
        else:
            study = ""

        return study, group

    # parse ONLY from attendance format cXXXXsXXXXk
    # def parse_study_and_group(self, study_and_group):
    #    group = study_and_group[:study_and_group.find("s")].lstrip("c")
    #    study = study_and_group[study_and_group.find(
    #        "s") + 1:study_and_group.find("k")]
    #
    #    return study, group


    #STUDENTS DATABASE "name - isic" will be represented
    #by a dictionary returned by function "create_database_of_students
    #in a database_handler.p, where key is a name (avoid duplicit names)
    #and value is ISIC ID (could be swapper in further release)
