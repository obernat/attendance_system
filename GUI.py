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
import read_card2 as rc
import read_card3 as rc3
import ISIC.getName as gN


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
        self.monitoredDatabase = 0
        if os.path.isfile('student_dict'):
            self.students_list = dp.load_student_dict()
        else:
            _, self.students_list = dh.create_students_database(dp.get_teacher())
            print(len(self.students_list))

        self.teacher = dp.load_teacher()

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

                    a = Label(text=active_subjects_list[i - 1].name , anchor = 'w')
                    b = Button(text="Attendance",
                               command=lambda text=active_subjects_list[i - 1].name:
                               self.attendance_page(text, "Skupina", "Tyzden 1"))
                    c = Button(text="Sync subject",
                               command=lambda text=active_subjects_list[i - 1].name: self.login_page(upload=1))

                    d = Button(text="Disable",
                               command=lambda text=active_subjects_list[i - 1].name: self.move_subject(text, 1))


                    a.place(relx=0.375, x=-250, rely=0.20,
                            y=(i * 30), width=210, height=25)
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

                    a = Label(tab1, text=active_subjects_list[i - 1].name, anchor= 'w')
                    b = Button(tab1, text="Subject info",
                               command=lambda text=active_subjects_list[i - 1].name: self.attendance_page(text,
                                                                                                            "Skupina",
                                                                                                            "Tyzden 1"))
                    c = Button(tab1, text="Sync subject",
                               command=lambda text=active_subjects_list[i - 1].name: self.login_page(upload=1))
                    d = Button(tab1, text="Disable",
                               command=lambda text=active_subjects_list[i - 1].name: self.move_subject(text, 1))

                    a.place(relx=0.375, x=-230, rely=0.20,
                            y=(i * 30), width=190, height=25)
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

                    a = Label(tab2, text=inactive_subjects_list[i - 1].name, anchor= 'w')
                    b = Button(tab2, text="Enable",
                               command=lambda text=inactive_subjects_list[i - 1].name: self.move_subject(text, 2))

                    a.place(relx=0.375, x=-150, rely=0.20,
                            y=(i * 30), width=210, height=25)
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
        dp.save_student_dict(self.students_list)
        self.minsize(height=700, width=1150) # set page size
        title_label = Label( self, text="Databáza študentov", font=self.title_font)
        if self.monitoredDatabase == 0:
            read_button = Button(text="Read cards", command=lambda: self.read_card_to_database(page_number))
        else:
            read_button = Button(text="Reading",bg= 'green', command=lambda: self.read_card_to_database(page_number))
        add_students_button = Button(text="Add new students")
        back_button = Button(self, text="Back", command=lambda: [
                self.subjects_page(1),
                self.geometry("700x500"),
                self.minsize(height=500,width=600)])


        num_students_in_column = 30
        num_of_columns = 3

        if len(self.students_list)%(3*num_students_in_column) == 0:   # num of student is the exactly same as one page allow
            num_of_pages = (len(self.students_list) // (3 * num_students_in_column))
        else:  # else we need create one page more
            num_of_pages = (len(self.students_list) // (3 * num_students_in_column)) + 1

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
        nameList = []

        for student in self.students_list:
            j +=1
            nameList.append(student.full_name)
            # range of names and numbers that have to be displayed
            if(j > (page_number*num_of_columns*num_students_in_column)) \
                    and j <= (page_number*num_of_columns*num_students_in_column)+num_of_columns*num_students_in_column:

                if row == num_students_in_column:
                    column += 1
                    row = 0

                if row % 2 == 1:
                    a = student.full_name
                    a = Label( self, text=student.full_name, anchor="w")
                    a.bind(self.right_click, self.popup_edit_db_page)
                    a.bind("<Enter>", self.on_enter)
                    a.place(relx=0.375, x=-370+(column*350), rely=0.3,
                            y=-150+(row * 20), width=170, height=20)
                    b = row
                    b = Label(self, text=student.ISIC, anchor="w")

                    b.place(relx=0.375, x=-200+(column*350), rely=0.3,
                            y=-150+(row * 20), width=150, height=20)

                else:  # only different color of rows
                    a = student.full_name
                    a = Label( self, text=student.full_name, anchor="w",
                              bg="#ecf2f8",
                              borderwidth=2,
                              highlightthickness=2,
                              highlightcolor="#ecf2f8",
                              highlightbackground="#ecf2f8")
                    a.bind(self.right_click, self.popup_edit_db_page)
                    a.bind("<Enter>", self.on_enter)
                    a.place(relx=0.375, x=-370+(column*350), rely=0.3,
                            y=-150+(row * 20), width=170, height=20)
                    b = row
                    b = Label(self, text=student.ISIC,
                              anchor="w",
                              bg="#ecf2f8",
                              borderwidth=2,
                              highlightthickness=2,
                              highlightcolor="#ecf2f8",
                              highlightbackground="#ecf2f8")

                    b.place(relx=0.375, x=-200+(column*350), rely=0.3,
                            y=-150+(row * 20), width=150, height=20)
                row += 1
####################################
        #gN.closestMatch(nameList) ########tu pridavam mena studentov do listu a volam matcher funkciu - len kvoli testovaniu to uz si uprav
####################################
        title_label.place(relx=0.385, rely=0.01, width=300, height=25)
        read_button.place(relx=0.90, rely=0.01, width=100, height=25)
        add_students_button.place(relx=0.90, x = -150, rely=0.01, width=150, height=25)

        back_button.place(relx=0.90, rely=0.95, width=100, height=25)

    def attendance_page(self, subject_name, group, week):
        self.clear_frame()

        colors = [
            "gray",
            "brown",
            "red",
            "yellow",
            "blue",
            "black",
            "green",
            "orange",
            ]

        self.attendance = dp.get_attendence()
        self.groups = dp.get_groups(subject_name)

        if group is "Skupina":
            group = list(self.groups)[0]
        if self.monitored == 0:
            start_button = Button(text="Read cards", command=lambda: self.read_card(subject_name, group, week))
        else:
            start_button = Button(text="Reading",bg = 'green', command=lambda: self.read_card(subject_name, group, week))

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

        self.popup_attendance_menu = Menu(self, tearoff=0)
        self.popup_attendance_menu.add_command(
            label="Prázdne", command=lambda: self.change_attendance(
                subject_name, group, week, 0))
        self.popup_attendance_menu.add_command(
            label="Skorší odchod", command=lambda: self.change_attendance(
                subject_name, group, week, 1))
        self.popup_attendance_menu.add_command(
            label="Neospravedlnená účasť", command=lambda: self.change_attendance(
                subject_name, group, week, 2))
        self.popup_attendance_menu.add_command(
            label="Ospravedlnená účasť", command=lambda: self.change_attendance(
                subject_name, group, week, 3))
        self.popup_attendance_menu.add_command(
            label="Prítomný na inom cvičení", command=lambda: self.change_attendance(
                subject_name, group, week, 4))
        self.popup_attendance_menu.add_command(
            label="Vylúčenie z cvičenia", command=lambda: self.change_attendance(
                subject_name, group, week, 5))
        self.popup_attendance_menu.add_command(
            label="Zúčastnil sa", command=lambda: self.change_attendance(
                subject_name, group, week, 6))
        self.popup_attendance_menu.add_command(
            label="Zúčastnil sa s neskorým príchodom", command=lambda: self.change_attendance(
                subject_name, group, week, 7))

        self.popup_change_group_menu = Menu(self, tearoff=0)
        self.popup_change_group_menu.add_command(
            label="Change group",
            command=lambda: self.change_group(
                subject_name,
                week))

        group_options = []
        for key in self.groups:
            group_options.append(key)

        week_options = []
        for i in range(1, 13):
            week_options.append("Tyzden " + str(i))

        group_variable = StringVar(self)
        group_variable.set(group)

        w = OptionMenu(self, group_variable, *group_options)
        w.place(relx=0.375, x=-50, rely=0.18, width=350, height=28)

        week_variable = StringVar(self)
        week_variable.set(week)

        week_option_menu = OptionMenu(self, week_variable, *week_options)
        week_option_menu.place(relx=0.375, x=-200, rely=0.18, width=150, height=28)

        tmp, week_number = str(week_variable.get()).split(' ')
        select_button = Button(
            self,
            text="Select",
            command=lambda: self.attendance_page(
                subject_name,
                group_variable.get(),
                week_variable.get()))

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
                    t.place(relx=0.4, x=+(k * 27), rely=0.3,
                            y=-22, width=21, height=21)
                else:
                    t = k
                    t = Label(self, text=str(k + 1))
                    t.place(relx=0.4, x=+(k * 27), rely=0.3,
                            y=-22, width=20, height=20)

            for name in self.groups[group]:

                a = name
                a = Label(self, text=name, anchor="w")
                a.place(relx=0.375, x=-150, rely=0.3,
                        y=+(i * 23), width=150, height=20)
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

                        g.place(relx=0.4, x=+(j * 27), rely=0.3,
                                y=+(i * 23), width=21, height=21)
                        g.bind(self.right_click, self.popup)
                        g.bind(
                            "<Button-1>",
                            lambda event: self.attendance_left_click(
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
                        g.place(relx=0.4, x=+(j * 27), rely=0.3,
                                y=+ (i * 23), width=18, height=18)

                bot = len(self.groups[group])
                i = i + 1

        select_button.place(relx=0.375, x=300, rely=0.18, width=150, height=25)
        title_label.place(relx=0.375, x= -250, rely=0.18, y = -75, width=800, height=25)
        back_button.place(relx=0.375, x=85, rely=0.3, y=-30+ (25 * (bot)), width=150, height=25)
        start_button.place(x=0, y=0, width=100, height=25)

        #legend
        legend_label_1 = Label(self, text="Prázdne",anchor= 'w')
        legend_label_1.place(x=15, y=-5 + (25 * (bot)),rely=0.18, width=200, height=15)
        legend_label_1_color = Label(self, text="c", bg= colors[0],fg = colors[0])
        legend_label_1_color.place(x=3, y=-3 + (25 * (bot)),rely=0.18, width=10, height=10)
        legend_label_2 = Label(self, text="Skorší odchod",anchor= 'w')
        legend_label_2.place(x=15, y=10 + (25 * (bot)),rely=0.18, width=200, height=15)
        legend_label_2_color = Label(self, text="c", bg=colors[1], fg=colors[1])
        legend_label_2_color.place(x=3, y=12 + (25 * (bot)),rely=0.18, width=10, height=10)
        legend_label_3 = Label(self, text="Neospravedlnená účasť",anchor= 'w')
        legend_label_3.place(x=15, y=25 + (25 * (bot)),rely=0.18, width=200, height=15)
        legend_label_3_color = Label(self, text="c", bg=colors[2], fg=colors[2])
        legend_label_3_color.place(x=3, y=27 + (25 * (bot)),rely=0.18, width=10, height=10)
        legend_label_4 = Label(self, text="Ospravedlnená účasť",anchor= 'w')
        legend_label_4.place(x=15, y=40 + (25 * (bot)),rely=0.18, width=200, height=15)
        legend_label_4_color = Label(self, text="c", bg=colors[3], fg=colors[3])
        legend_label_4_color.place(x=3, y=42 + (25 * (bot)),rely=0.18, width=10, height=10)
        legend_label_5 = Label(self, text="Prítomný na inom cvičení",anchor= 'w')
        legend_label_5.place(x=15, y=55 + (25 * (bot)),rely=0.18, width=250, height=15)
        legend_label_5_color = Label(self, text="c", bg=colors[4], fg=colors[4])
        legend_label_5_color.place(x=3, y=57 + (25 * (bot)),rely=0.18, width=10, height=10)
        legend_label_6 = Label(self, text="Vylúčenie z cvičenia",anchor= 'w')
        legend_label_6.place(x=15, y=70 + (25 * (bot)),rely=0.18, width=250, height=15)
        legend_label_6_color = Label(self, text="c", bg=colors[5], fg=colors[5])
        legend_label_6_color.place(x=3, y=72 + (25 * (bot)),rely=0.18, width=10, height=10)
        legend_label_7= Label(self, text="Zúčastnil sa",anchor= 'w')
        legend_label_7.place(x=15, y=85 + (25 * (bot)),rely=0.18, width=250, height=15)
        legend_label_7_color = Label(self, text="c", bg=colors[6], fg=colors[6])
        legend_label_7_color.place(x=3, y=87 + (25 * (bot)),rely=0.18, width=10, height=10)
        legend_label_8 = Label(self, text="Zúčastnil sa s neskorým príchodom",anchor= 'w')
        legend_label_8.place(x=15, y=100 + (25 * (bot)),rely=0.18, width=250, height=15)
        legend_label_8_color = Label(self, text="c", bg=colors[7], fg=colors[7])
        legend_label_8_color.place(x=3, y=102 + (25 * (bot)),rely=0.18, width=10, height=10)


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
        teacher = dp.load_teacher()
        new_subjects_list = []
        for subject in teacher.subjects_list:
            if subject.name == subject_name:
                if subject.is_active:
                    subject.is_active = 0
                else:
                    subject.is_active = 1
            new_subjects_list.append(subject)
        teacher.subjects_list = new_subjects_list
        dp.save_teacher(teacher)
        self.subjects_page(tab_number)

    def attendance_left_click(self, event, subject_name, group, week_selected):

        name, week = str(self.selected).split('_')

        if self.attendance[str(name)][0][int(week)] == 6:
            self.change_attendance(subject_name, group, week_selected, 2)
        else:
            self.change_attendance(subject_name, group, week_selected, 6)

    def popup(self, event):
        self.popup_attendance_menu.post(event.x_root, event.y_root)

    def popup_student(self, event):
        self.popup_change_group_menu.post(event.x_root, event.y_root)

    def popup_edit_db_page(self, event):
        popup_edit_menu = Menu(self, tearoff=0)
        popup_edit_menu.add_command(label="Edit number",
                                    command=lambda: self.popup_edit_db_page_2(event.widget['text']))
        popup_edit_menu.post(event.x_root, event.y_root)

    def popup_edit_db_page_2(self, name):
        toplevel = Toplevel()
        toplevel.geometry("320x35")
        number_entry = Entry(toplevel)
        button = Button(toplevel, text="Edit number", command=lambda: self.rewrite_student_number(name, number_entry.get()))
        number_entry.place(x=5, y=5, width=150, height=25)
        button.place(x=160, y=5, width=150, height=25)

    def rewrite_student_number(self, name, number):
        for student in self.students_list:
            if student.full_name == name:
                    student.ISIC = number
        dp.save_student_dict(self.students_list)
        self.database_page(0)

    def on_enter(self, event):
        self.selected = event.widget['text']

    def close_window(self, window):
        window.destroy()

    def switch_student(self,window,to_group,subject_name,week_selected):

        for subject in self.teacher.subjects_list:
            if subject.name == subject_name:
                for student in subject.student_list:
                    if student.name  == self.selected:
                        student.cv_string = to_group

        dp.save_teacher(self.teacher)
        self.attendance_page(subject_name, to_group, week_selected)

        self.close_window(window)

    def change_group(self, subject_name, week_selected):
        toplevel = Toplevel()
        toplevel.geometry("320x35")
        OPTIONS = []

        for group_tmp in self.groups:
            OPTIONS.append(group_tmp)

        variable = StringVar(self)
        variable.set(OPTIONS[0])

        w = OptionMenu(toplevel, variable, *OPTIONS)
        w.place(x=5, y=5, width=150, height=25)

        button = Button(
            toplevel,
            text="Select",
            command=lambda: self.switch_student(
                toplevel,
                variable.get(),
                subject_name,
                week_selected))
        button.place(x=160, y=5, width=150, height=25)

    def change_attendance(self, subject_name, group, week_selected, choice):
        name, week = str(self.selected).split('_')
        self.attendance[name][0][int(week)] = choice
        print(week)
        for subject in self.teacher.subjects_list:
            for student in subject.student_list:
                if student.name == name:
                    student.attendance = self.attendance[name][0]
        dp.save_teacher(self.teacher)
        self.attendance_page(subject_name, group, week_selected)

    def change_attendance_from_card(self, subject_name, group, week_selected, choice, name, week):
        self.attendance[name][0][int(week_selected)] = choice
        print(week_selected)
        for subject in self.teacher.subjects_list:
            for student in subject.student_list:
                if student.name == name:
                    student.attendance = self.attendance[name][0]
        dp.save_teacher(self.teacher)
        self.attendance_page(subject_name, group, week)

    def read_card(self, subject_name, group, week):
        if (self.monitored == 0):
            self.monitored = 1
            self.attendance_page(subject_name, group, week)
            self.read = rc.read_card2(self, subject_name, group, week)
            self.cardmonitor = self.read.readCards()
        else:
            self.monitored = 0
            self.attendance_page(subject_name, group, week)
            self.read.stopReadCards(self.cardmonitor)


    def read_card_to_database(self, page_number):
        if (self.monitoredDatabase == 0):
            self.monitoredDatabase = 1
            self.database_page(page_number)
            self.read = rc3.read_card2(self, page_number)
            self.cardmonitor = self.read.readCards()
        else:
            self.monitored = 0
            self.database_page(page_number)
            self.read.stopReadCards(self.cardmonitor)



if __name__ == "__main__":
    app = Application()
    app.mainloop()
