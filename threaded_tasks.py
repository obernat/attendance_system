import threading
import queue
import is_parser as isp
import  error_handler as er
import time
import data_parser as dp
import database_handler as dh


class DownloadThread(threading.Thread):
    def __init__(self, queue,session,delegat_id):
        """
        Construct a new 'ThreadedTask' object.
        """
        threading.Thread.__init__(self)
        self.queue = queue
        self.session = session
        self.delegat_id = delegat_id


    def run(self):

        if self.delegat_id:
            ret_value, teacher = isp.dr_download_data(self.session,int(self.delegat_id))
        else:
            ret_value, teacher = isp.dr_download_data(self.session)
        _, students_list = dh.create_students_database(teacher)
        dp.save_student_dict(students_list)

        if ret_value < 0:
            self.queue.put("Download finished")
            time.sleep(0.5)
            er.showError("Nesprávne prihlasovacie údaje!")

        else:
            dp.save_teacher(teacher)
            self.queue.put("Download finished")



class UploadThread(threading.Thread):
    def __init__(self, queue,name,password,subject_name):
        """
        Construct a new 'ThreadedTask' object.
        """
        threading.Thread.__init__(self)
        self.queue = queue
        self.name = name
        self.password = password
        self.subject_name =subject_name

    def run(self):
        teacher = dp.load_teacher()
        for subject in teacher.subjects_list:
            if subject.name == self.subject_name:
                tmp = subject

        ret_value, ret_subject= isp.upload_routine(
            tmp,teacher.delegate_id, self.name, self.password)

        for subject in teacher.subjects_list:
            if subject.name == self.subject_name:
                subject=ret_subject

        dp.save_teacher(teacher)
        if ret_value < 0:
            self.queue.put("Upload finished")
            time.sleep(0.5)
            er.showError("Synchronizácia sa nepodarila")
            return
        self.queue.put("Upload finished")






