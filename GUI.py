from tkinter import *
from tkinter import font as tkfont
from tkinter import ttk
from six.moves import cPickle as pickle
import os
import sys
from sys import platform
import requests
import is_parser as isp
import data_parser as dp
import error_handler as er
import datetime
from threaded_tasks import DownloadThread, UploadThread
import queue
import database_handler as dh

# import read_card2 as rc


class Application(Tk):
    # GUI Application

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        #platforms have different bind for rightclick
        if platform == "darwin":
            self.right_click = "<Button-2>"
        else:
            self.right_click = "<Button-3>"

        self.title_font = tkfont.Font(
            family='Helvetica',
            size=18,
            weight="bold",
            slant="italic")
        self.geometry("700x500")
        self.minsize(height=500, width=600)
        self.cross_road_function()
        self.selected = 0
        self.monitored = 0


# PAGES GUI -------------------------------------------------

    def login_page(self, download=0, upload=0):
        """
        Page with login formular
        :param download - when is set up on 1 is called download function
        :param upload - when is set up on 1 is called upload function
        """
        self.clear_frame()

        self.title_label = Label(self, text="Login", font=self.title_font)
        self.username_label = Label(self, text="Username")
        self.password_label = Label(self, text="Password")
        self.username_entry = Entry(self)
        self.password_entry = Entry(self, show="*")
        self.back_button = Button(
            self, text="Back", command=self.cross_road_function)

        if download:
            self.login_button = Button(
                self, text="Login", command=lambda: self.download_data(
                    self.username_entry.get(), self.password_entry.get()))
        if upload:
            self.login_button = Button(
                self, text="Login", command=lambda: self.upload_data(
                    self.username_entry.get(), self.password_entry.get()))

        self.title_label.place(
            relx=0.42,
            rely=0.42,
            y=-120,
            width=120,
            height=25)
        self.username_label.place(
            relx=0.42,
            x=-60,
            rely=0.42,
            y=-65,
            width=120,
            height=25)
        self.password_label.place(
            relx=0.42,
            x=-60,
            rely=0.42,
            y=-37,
            width=120,
            height=25)
        self.username_entry.place(
            relx=0.42,
            x=60,
            rely=0.42,
            y=-65,
            width=120,
            height=25)
        self.password_entry.place(
            relx=0.42,
            x=60,
            rely=0.42,
            y=-37,
            width=120,
            height=25)
        self.login_button.place(
            relx=0.42,
            rely=0.42,
            width=120,
            height=25)
        self.back_button.place(
            relx=0.42,
            rely=0.42,
            y=40,
            width=120,
            height=25)

    def downloading_page(self):
        """
        Download_page display progress bar while data is downloading
        """
        self.clear_frame()
        self.prog_bar = ttk.Progressbar(self, orient="horizontal",mode="determinate")
        self.sync_label = Label(self, text="Downloading data...")

        self.prog_bar.place(relx=0.37, rely=0.35, width=200, height=25)
        self.sync_label.place(relx=0.37, rely=0.30, width=200, height=25)
        self.prog_bar.start()

    def uploading_page(self):
        """
        Upload_page display progress bar while data is uploading
        """
        self.clear_frame()
        self.prog_bar = ttk.Progressbar(self, orient="horizontal",mode="determinate" )
        self.sync_label = Label(self,text="Upload data...")

        self.prog_bar.place(relx=0.37, rely=0.35, width=200, height=25)
        self.sync_label.place(relx=0.37, rely=0.30, width=200, height=25)
        self.prog_bar.start()

    def no_connection_page(self):
        """
        No_connection_page display only report and reload button
        """
        self.clear_frame()

        self.sync_label= Label(
            self, text="Žiadne internetové pripojenie")
        self.sync_button = Button(
            self, text='Reload', command=lambda: self.cross_road_function())

        self.sync_label.place(relx=0.37, rely=0.30, width=200, height=25)
        self.sync_button.place(relx=0.42, rely=0.42, width=120, height=25)

    def subjects_page(self, tab_number):
        self.clear_frame()

        active_subjects_list, inactive_subjects_list = dp.get_subjects_lists()

        if not inactive_subjects_list:

            database_button= Button(text="Database",command=lambda: self.database_page(0))
            sync_button = Button(text="Sync All")

            if (len(active_subjects_list)):

                for i in range(1, len(active_subjects_list) + 1):
                    a = i
                    b = i * 10
                    c = i * 10+1
                    d = i * 10+2
                    e = i * 10+3

                    a = Label(text=active_subjects_list[i - 1].name)
                    b = Button(text="Attendance",
                               command=lambda text=active_subjects_list[i - 1].name:
                               self.subject_info_page(text, "Skupina", "Tyzden 1"))
                    c = Button(text="Sync subject",
                               command=lambda text=active_subjects_list[i - 1].name: self.login_page(upload=1))

                    d = Button(text="Disable",
                               command=lambda text=active_subjects_list[i - 1].name: self.move_subject(text, 1))


                    a.place(relx=0.375, x=-210, rely=0.20,
                            y=(i * 30), width=180, height=25)
                    b.place(relx=0.375, x=-30, rely=0.20,
                            y=(i * 30), width=120, height=25)
                    c.place(relx=0.375, x=+90, rely=0.20,
                            y=(i * 30), width=120, height=25)
                    d.place(relx=0.375, x=+210, rely=0.20,
                            y=(i * 30), width=120, height=25)

            database_button.place(relx=0.83, x= +10,rely=0.00, width=100, height=25)
            sync_button.place(relx=0.83,x= -70, rely=0.00, width=75, height=25)

        else:

            tabControl = ttk.Notebook(self)

            tab1 = ttk.Frame(tabControl)
            tab2 = ttk.Frame(tabControl)

            tabControl.add(tab1, text='Active')
            tabControl.add(tab2, text='Inactive')
            sync_button_tab1 = Button(tab1, text="Sync All")
            database_button_tab1 = Button(tab1,text="Database", command=lambda: self.database_page(0))
            sync_button_tab2 = Button(tab2, text="Sync All")
            database_button_tab2 = Button(tab2,text="Database", command=lambda: self.database_page(0))

            if (len(active_subjects_list)):

                for i in range(1, len(active_subjects_list) + 1):
                    a = i
                    b = i * 10
                    c = i * 10 + 1
                    d = i * 10 + 2

                    a = Label(tab1, text=active_subjects_list[i - 1].name)
                    b = Button(tab1, text="Subject info",
                               command=lambda text=active_subjects_list[i - 1].name: self.subject_info_page(text,
                                                                                                            "Skupina",
                                                                                                            "Tyzden 1"))
                    c = Button(tab1, text="Sync subject",
                               command=lambda text=active_subjects_list[i - 1].name: self.login_page(upload=1))
                    d = Button(tab1, text="Disable",
                               command=lambda text=active_subjects_list[i - 1].name: self.move_subject(text, 1))

                    a.place(relx=0.375, x=-180, rely=0.20,
                            y=(i * 30), width=120, height=25)
                    b.place(relx=0.375, x=-60, rely=0.20,
                            y=(i * 30), width=120, height=25)
                    c.place(relx=0.375, x=+60, rely=0.20,
                            y=(i * 30), width=120, height=25)
                    d.place(relx=0.375, x=+180, rely=0.20,
                            y=(i * 30), width=120, height=25)

            if (len(inactive_subjects_list)):

                for i in range(1, len(inactive_subjects_list) + 1):
                    a = i
                    b = i * 10

                    a = Label(tab2, text=inactive_subjects_list[i - 1].name)
                    b = Button(tab2, text="Enable",
                               command=lambda text=inactive_subjects_list[i - 1].name: self.move_subject(text, 2))

                    a.place(relx=0.375, x=-60, rely=0.20,
                            y=(i * 30), width=120, height=25)
                    b.place(relx=0.375, x=+60, rely=0.20,
                            y=(i * 30), width=120, height=25)

            sync_button_tab1.place(relx=0.65, x=+38, y=0, width=75, height=25)
            sync_button_tab2.place(relx=0.65, x=+38, y=0, width=75, height=25)
            database_button_tab1.place(
                relx=0.65, x=+114, y=0, width=100, height=25)
            database_button_tab2.place(
                relx=0.65, x=+114, y=0, width=100, height=25)

            tabControl.pack(expand=1, fill="both")

            if tab_number == 1:
                tabControl.select(tab1)
            else:
                tabControl.select(tab2)

    def database_page(self,page_number):
        self.clear_frame()
        self.minsize(height=700, width=1150) # set page size

        title_label = Label( self, text="Databáza študentov", font=self.title_font)
        read_button = Button(text="Read cards")
        back_button = Button(self, text="Back", command=lambda: [
                self.subjects_page(1),
                self.geometry("700x500"),
                self.minsize(height=500,width=600)])

        i, students_dict = dh.create_database_of_students(dp.get_teacher())
        num_students_in_column = 30
        num_of_columns = 3

        if len(students_dict)%(3*num_students_in_column) == 0:   # num of student is the exactly same as one page allow
            num_of_pages = (len(students_dict)//(3*num_students_in_column))
        else:  # else we need create one page more
            num_of_pages = (len(students_dict)//(3*num_students_in_column))+1

        # when we have more student as one page allow we need create 'pages switcher'
        if num_of_pages > 1:
            next = (page_number + 1) % num_of_pages
            prev = (page_number - 1 + num_of_pages) % num_of_pages
            page_label = Label(self, text=page_number + 1, font=self.title_font)
            next_button = Button(text="Next", command=lambda: self.database_page(next))
            prev_button = Button(text="Prev", command=lambda: self.database_page(prev))
            page_label.place(relx=0.385, x=140, rely=0.95, width=15, height=25)
            prev_button.place(relx=0.385, x=17, rely=0.95, width=100, height=25)
            next_button.place(relx=0.385, x=170, rely=0.95, width=100, height=25)

        row = 0
        j = 0
        column = 0

        for name in students_dict:
            j +=1
            # range of names and numbers that have to be displayed
            if(j > (page_number*num_of_columns*num_students_in_column)) \
                    and j <= (page_number*num_of_columns*num_students_in_column)+num_of_columns*num_students_in_column:

                if row == num_students_in_column:
                    column += 1
                    row = 0

                if row % 2 == 1:
                    a = name
                    a = Label( self, text=name, anchor="w")
                    a.place(relx=0.375, x=-370+(column*350), rely=0.3,
                            y=-150+(row * 20), width=170, height=20)
                    b = row
                    b = Label( self, text=students_dict[name], anchor="w")
                    b.place(relx=0.375, x=-200+(column*350), rely=0.3,
                            y=-150+(row * 20), width=150, height=20)

                else:  # only different color of rows
                    a = name
                    a = Label( self, text=name, anchor="w",
                              bg="#ecf2f8",
                              borderwidth=2,
                              highlightthickness=2,
                              highlightcolor="#ecf2f8",
                              highlightbackground="#ecf2f8")
                    a.place(relx=0.375, x=-370+(column*350), rely=0.3,
                            y=-150+(row * 20), width=170, height=20)
                    b = row
                    b = Label( self, text=students_dict[name], anchor="w",
                              bg="#ecf2f8",
                              borderwidth=2,
                              highlightthickness=2,
                              highlightcolor="#ecf2f8",
                              highlightbackground="#ecf2f8")
                    b.place(relx=0.375, x=-200+(column*350), rely=0.3,
                            y=-150+(row * 20), width=150, height=20)
                row += 1

        title_label.place(relx=0.385, rely=0.01, width=300, height=25)
        read_button.place(relx=0.90, rely=0.01, width=100, height=25)
        back_button.place(relx=0.90, rely=0.95, width=100, height=25)

    def subject_info_page(self, subject_name, group, week):
        self.clear_frame()

        colors = [
            "red",
            "green",
            "yellow",
            "black",
            "gray",
            "yellow",
            "blue",
            'brown']
        self.attendance = dp.get_attendence()
        self.groups = dp.get_groups()

        start_button = Button(text="tmp_start", command=self.read_card)
        title_label = Label(self, text=subject_name, font=self.title_font)
        back_button = Button(
            self,
            text="Back",
            command=lambda: [
                self.subjects_page(1),
                self.geometry("700x500"),
                self.minsize(
                    height=500,
                    width=600)])

        self.popupMenu = Menu(self, tearoff=0)
        self.popupMenu.add_command(
            label="red", command=lambda: self.change_attendance(
                subject_name, group, week, 0))
        self.popupMenu.add_command(
            label="green", command=lambda: self.change_attendance(
                subject_name, group, week, 1))
        self.popupMenu.add_command(
            label="yellow", command=lambda: self.change_attendance(
                subject_name, group, week, 2))
        self.popupMenu.add_command(
            label="black", command=lambda: self.change_attendance(
                subject_name, group, week, 3))
        self.popupMenu.add_command(
            label="gray", command=lambda: self.change_attendance(
                subject_name, group, week, 4))

        self.popupMenu2 = Menu(self, tearoff=0)
        self.popupMenu2.add_command(
            label="Change group",
            command=lambda: self.change_group(
                group,
                subject_name,
                week))

        OPTIONS = []
        for key in self.groups:
            OPTIONS.append(key)

        week_options = []
        for i in range(1, 13):
            week_options.append("Tyzden " + str(i))

        variable = StringVar(self)
        variable.set(group)

        w = OptionMenu(self, variable, *OPTIONS)
        w.place(relx=0.375, x=0, rely=0.18, width=350, height=28)

        week_variable = StringVar(self)
        week_variable.set(week)

        week_option_menu = OptionMenu(self, week_variable, *week_options)
        week_option_menu.place(
            relx=0.375,
            x=-150,
            rely=0.18,
            width=150,
            height=28)

        tmp, week_number = str(week_variable.get()).split(' ')
        button = Button(
            self,
            text="Select",
            command=lambda: self.subject_info_page(
                subject_name,
                variable.get(),
                week_variable.get()))
        button.place(relx=0.375, x=350, rely=0.18, width=150, height=25)
        bot = 0
        if group is not "Skupina":
            i = 0

            for k in range(0, 12):
                if (k == int(week_number) - 1):
                    t = k
                    t = Label(
                        self,
                        text=str(
                            k + 1),
                        bg="#37d3ff",
                        borderwidth=2,
                        highlightthickness=2,
                        highlightcolor="#37d3ff",
                        highlightbackground="#37d3ff",
                    )
                    t.place(relx=0.4, x=+(k * 25), rely=0.3,
                            y=-22, width=21, height=21)
                else:
                    t = k
                    t = Label(self, text=str(k + 1))
                    t.place(relx=0.4, x=+(k * 25), rely=0.3,
                            y=-22, width=20, height=20)

            for name in self.groups[group]:

                a = name
                a = Label(self, text=name, anchor="w")
                a.place(relx=0.375, x=-150, rely=0.3,
                        y=+(i * 20), width=150, height=20)
                a.bind(self.right_click, self.popup_student)
                a.bind("<Enter>", self.on_enter)

                for j in range(0, 12):
                    if (j == int(week_number) - 1):
                        g = j
                        g = Label(self,
                                  text=name + "_" + str(j),
                                  bg=colors[self.attendance[name][0][j]],
                                  fg=colors[self.attendance[name][0][j]],
                                  borderwidth=2,
                                  highlightthickness=2,
                                  highlightcolor="#37d3ff",
                                  highlightbackground="#37d3ff",
                                  )

                        g.place(relx=0.4, x=+(j * 25), rely=0.3,
                                y=+(i * 20), width=21, height=21)
                        g.bind(self.right_click, self.popup)
                        g.bind(
                            "<Button-1>",
                            lambda event: self.left_click(
                                event,
                                subject_name,
                                group,
                                week))
                        g.bind("<Enter>", self.on_enter)
                    else:
                        g = j
                        g = Label(self,
                                  text=name + "_" + str(j),
                                  bg=colors[self.attendance[name][0][j]],
                                  fg=colors[self.attendance[name][0][j]])
                        g.place(relx=0.4, x=+(j * 25), rely=0.3,
                                y=+ (i * 20), width=18, height=18)

                bot = len(self.groups[group])
                i = i + 1

        title_label.place(relx=0.385, rely=0.08, width=300, height=25)
        back_button.place(relx=0.375, x=85, rely=0.25, y=+
                          (25 * (bot)), width=150, height=25)
        start_button.place(x=0, y=0, width=100, height=25)

        self.minsize(height=(250 + (bot * 25)), width=1000)

# FUNCTIONS GUI -------------------------------------------------

    def clear_frame(self):
        """
        Function clear frame, is called on every function which shows tkinter objects
        """
        for child in self.winfo_children():
            child.destroy()

    def cross_road_function(self):
        """
        Function decide witch page will displayed first
        """
        if os.path.isfile('teacher'):
            self.subjects_page(1) #Data is downloaded - display page with subjest
        else:
            if isp.try_connection() == 1:
                self.login_page(download=1) #Connection is OK but we have not data - display login page and download data
            else:
                self.no_connection_page() #Connection is KO - display page with warnning

    def upload_data(self, name="none", password="none"):
        """
        Function create thread for uploading data and call upload_page
        :param name:  login to IS
        :param password: password to IS
        :return: nothing
        """
        self.uploading_page()
        self.queue = queue.Queue()
        UploadThread(self.queue, name, password).start()
        self.after(100, self.process_queue)

    def download_data(self, name="none", password="none", ):
        """
        Function create thread for dowloading data and call download_page
        :param name: name to IS
        :param password:  password to IS
        :return: nothing
        """
        self.downloading_page()
        self.queue = queue.Queue()
        DownloadThread(self.queue, name, password).start()
        self.after(100, self.process_queue)

    def process_queue(self):
        """
        Function checking when thread ends and then call right page
        """
        try:
            msg = self.queue.get(0)
            if(msg == "Download finished"):
                self.cross_road_function()
            if(msg == "Upload finished"):
                self.subjects_page(1)

        except queue.Empty:
            self.after(100, self.process_queue)

    def move_subject(self, subject_name, tab_number):
        teacher = dp.load_data()
        new_subjects_list = []
        for subject in teacher.subjects_list:
            if subject.name == subject_name:
                if subject.is_active:
                    subject.is_active = 0
                else:
                    subject.is_active = 1
            new_subjects_list.append(subject)
        teacher.subjects_list = new_subjects_list
        dp.save_data(teacher)
        self.subjects_page(tab_number)

    def left_click(self, event, subject_name, group, week_selected):

        name, week = str(self.selected).split('_')

        if self.attendance[str(name)][int(week)] == 1:
            self.change_attendance(subject_name, group, week_selected, 3)
        else:
            self.change_attendance(subject_name, group, week_selected, 1)

    def popup(self, event):
        self.popupMenu.post(event.x_root, event.y_root)

    def popup_student(self, event):
        self.popupMenu2.post(event.x_root, event.y_root)

    def on_enter(self, event):
        self.selected = event.widget['text']

    def close_window(self, window):
        window.destroy()

    # TODO Upravit to
    def switch_student(self,window,from_group,to_group,subject_name,week_selected):

        self.groups[to_group].append(self.selected)
        self.groups[from_group].remove(self.selected)
        self.save_attendace()
        self.subject_info_page(subject_name, to_group, week_selected)

        self.close_window(window)

    def change_group(self, group, subject_name, week_selected):

        toplevel = Toplevel()
        toplevel.geometry("320x35")
        OPTIONS = []

        for i in range(1, 20):
            OPTIONS.append("Skupina " + str(i))

        variable = StringVar(self)
        variable.set(OPTIONS[0])

        w = OptionMenu(toplevel, variable, *OPTIONS)
        w.place(x=5, y=5, width=150, height=25)

        button = Button(
            toplevel,
            text="Select",
            command=lambda: self.switch_student(
                toplevel,
                group,
                variable.get(),
                subject_name,
                week_selected))
        button.place(x=160, y=5, width=150, height=25)

    def change_attendance(self, subject_name, group, week_selected, a):
        teacher = dp.load_data()
        name, week = str(self.selected).split('_')
        self.attendance[name][0][int(week)] = a

        for subject in teacher.subjects_list:
            for student in subject.student_list:
                if student.name == name:
                    student.attendance = self.attendance[name][0]
        dp.save_data(teacher)
        self.subject_info_page(subject_name, group, week_selected)

    def read_card(self):
        if (self.monitored == 0):
            self.monitored = 1
            self.read = rc.read_card2(self)
            self.cardmonitor = self.read.readCards()
        else:
            self.monitored = 0
            self.read.stopReadCards(self.cardmonitor)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
