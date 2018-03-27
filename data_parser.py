from six.moves import cPickle as pickle


def save_teacher(teacher):
    try:
        f = open('teacher', 'wb')
        save = {
            'teacher': teacher,
        }
        pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
        f.close()
    except Exception as e:
         print('Unable to pickle teacher object:', e)

def save_student_dict(student_dict):
    try:
        f = open('student_dict', 'wb')
        save = {
            'student_dict': student_dict,
        }
        pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
        f.close()
    except Exception as e:
         print('Unable to pickle student_dict object:', e)

def load_teacher():
    try:
        with open('teacher', 'rb') as f:
            data = pickle.load(f)
            teacher = data['teacher']
        return teacher
    except Exception as e:
        print('Unable to read data from teacher:', e)

def load_student_dict():
    try:
        with open('student_dict', 'rb') as f:
            data = pickle.load(f)
            student_dict = data['student_dict']
        return student_dict
    except Exception as e:
        print('Unable to read data from teacher:', e)

def get_subjects_lists():
    teacher = load_teacher()
    active_subjects_list= []
    inactive_subjects_list = []

    for subject in teacher.subjects_list:
        if subject.is_active:
            active_subjects_list.append(subject)
        else:
            inactive_subjects_list.append(subject)

    return active_subjects_list, inactive_subjects_list


def get_attendence():

    teacher = load_teacher()
    attendance = {}
    for subject in teacher.subjects_list:
        for student in subject.student_list:
            attendance.setdefault(student.name, []).append(student.attendance)
    return attendance

def get_groups(subject_name):

    teacher = load_teacher()
    groups = {}
    for subject in teacher.subjects_list:
        if subject.name == subject_name:
            for student in subject.student_list:
                groups.setdefault(student.cv_string, []).append(student.name)
    return groups

def get_teacher():
    return load_teacher()
