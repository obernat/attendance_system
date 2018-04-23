import threading
import queue
import is_parser as isp
import  error_handler as er
import time
import data_parser as dp
import database_handler as dh


class DownloadThread(threading.Thread):
    def __init__(self, queue,name,password):
        """
        Construct a new 'ThreadedTask' object.
        """
        threading.Thread.__init__(self)
        self.queue = queue
        self.name = name
        self.password = password


    def run(self):

        ret_value, teacher = isp.download_routine(self.name, self.password)
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
    def __init__(self, queue,name,password):
        """
        Construct a new 'ThreadedTask' object.
        """
        threading.Thread.__init__(self)
        self.queue = queue
        self.name = name
        self.password = password

    def run(self):
        teacher = dp.load_teacher()

        ret_value = isp.upload_routine(
            teacher.subjects_list[0], self.name, self.password)
        if ret_value < 0:
            self.queue.put("Upload finished")
            time.sleep(0.5)
            er.showError("Synchronizácia sa nepodarila")
            return
        self.queue.put("Upload finished")






