import threading
import queue
import is_parser as isp
import  error_handler as er
import time
import data_parser as dp


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
        if ret_value < 0:
            self.queue.put("Download finished")
            time.sleep(0.5)
            er.showError("Nesprávne prihlasovacie údaje!")

        else:
            dp.save_data(teacher)
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
        teacher = dp.load_data()

        ret_value = isp.upload_routine(
            teacher.subjects_list[0], self.name, self.password)
        if ret_value < 0:
            self.queue.put("Upload finished")
            time.sleep(0.5)
            er.showError("FAIL UPLOAD")
            return
        self.queue.put("Upload finished")






