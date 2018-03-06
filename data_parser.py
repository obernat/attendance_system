from six.moves import cPickle as pickle


def save_data(teacher):
    try:
        f = open('teacher', 'wb')
        save = {
            'teacher': teacher,
        }
        pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
        f.close()
    except Exception as e:
         print('Unable to pickle teacher object:', e)

def load_data():
    try:
        with open('teacher', 'rb') as f:
            data = pickle.load(f)
            teacher = data['teacher']
        return teacher
    except Exception as e:
        print('Unable to read data from teacher:', e)

def subjects_lists():
    teacher = load_data()
    active_subjects_list= []
    inactive_subjects_list = []

    for subject in teacher.subjects_list:
        if subject.is_active:
            active_subjects_list.append(subject)
        else:
            inactive_subjects_list.append(subject)

    return active_subjects_list, inactive_subjects_list