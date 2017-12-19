from tkinter import *
from tkinter import font as tkfont
from tkinter import ttk
from six.moves import cPickle as pickle
import os
import time
import sys
from sys import platform
import requests
import is_parser as isp
import error_handler as er
import datetime
import read_card2 as rc


class Application(Tk):
    #GUI Application

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)


        if platform == "darwin":
            self.right_click = "<Button-2>"
        else:
            self.right_click = "<Button-3>"

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("600x500")
        self.login_page()
        self.selected = 0
        #self.session = requests.Session()
        self.monitored = 0

    def clear_frame(self):

        for child in self.winfo_children():
            child.destroy()

    def login_page(self):

        self.clear_frame()
        self.session = requests.Session()

        self.title_label = Label(self, text="Login" ,font=self.title_font)
        self.username_label = Label(self, text="Username")
        self.password_label = Label(self, text="Password")
        self.username_entry = Entry(self)
        self.password_entry = Entry(self, show="*")
        self.checkbox = Checkbutton(self, text="Keep me logged in")
        self.login_button = Button(self, text="Login", command = lambda: self.cross_road_function(self.username_entry.get(),self.password_entry.get()))
        self.remove_button = Button(self, text="Remove files", command = self.remove_files )

        self.title_label.place(relx=0.42, rely=0.42, y=-120, width=120, height=25)
        self.username_label.place(relx=0.42, x=-60, rely=0.42, y=-65, width=120, height=25)
        self.password_label.place(relx=0.42, x=-60, rely=0.42, y=-37, width=120, height=25)
        self.username_entry.place(relx=0.42, x=60, rely=0.42, y=-65, width=120, height=25)
        self.password_entry.place(relx=0.42, x=60, rely=0.42, y=-37, width=120, height=25)
        self.checkbox.place(relx=0.42, rely=0.42, width=120, height=25)
        self.login_button.place(relx=0.42, rely=0.42, y=40, width=120, height=25)
        self.remove_button.place(relx=0.42, rely=0.42, y=70, width=120, height=25)

    def sync_page(self):

        self.clear_frame()

        self.sync_button = Button(self, text='Sync', command=self.load_subjects)
        self.sync_button.place(relx=0.42, rely=0.42, width=120, height=25)

    def file_check(self,file): #TODO - remove

        try:
            open(file, "r")
            return 1
        except IOError:
            return 0

    def remove_files(self):

        os.remove('active_subjects')
        os.remove('inactive_subjects')

    def cross_road_function(self, name="none", password="none"):
        ret_value = isp.try_login(self.session, name, password)

        if ret_value < 0:
            er.showError("Nesprávne prihlasovacie údaje!")
            self.login_page()
            return

        #if self.file_check('active_subjects'):
        if os.path.isfile('active_subjects'):
            self.subjects_page(1)
        else:
            self.sync_page()

    def load_subjects(self):

        ret_value, subjects_list_with_links = isp.get_subjects(self.session)

        if ret_value < 0:
            er.showError("K dispozícii nie sú žiadne predmety!")
            self.sync_page()
            return

        self.active_subjects_list = []
        self.active_subjects_links_list = []
        for subject in subjects_list_with_links:
            self.active_subjects_list.append(subject[0])
            self.active_subjects_links_list.append(subject[1])

        self.inactive_subjects_list = []
        self.inactive_subjects_links_list = []

        groups = dict()
        groups["Skupina 1"] = ["Matus", "Tomas", "Dano"]
        groups["Skupina 2"] = ["Matus2", "Tomas2", "Dano2"]

        attendance = dict()
        attendance["Matus"] = [0, 2, 3, 4, 5, 1, 1, 1, 1, 1, 1, 1]
        attendance["Tomas"] = [1, 2, 3, 4, 5, 1, 1, 1, 1, 3, 3, 3]
        attendance["Dano"] = [1, 2, 3, 4, 5, 1, 1, 1, 2, 4, 1, 1]
        attendance["Matus2"] = [1, 2, 3, 4, 5, 1, 5, 1, 1, 1, 1, 1]
        attendance["Tomas2"] = [1, 2, 3, 4, 5, 1, 1, 5, 4, 1, 1, 1]
        attendance["Dano2"] = [1, 2, 3, 4, 5, 1, 1, 1, 1, 2, 3, 1]

        try:
            f = open('attendance', 'wb')
            save = {
                'attendance': attendance,
                'groups': groups,
            }
            pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
            f.close()
        except Exception as e:
            print('Unable to save data to attendance:', e)


        try:
            f = open('active_subjects', 'wb')
            save = {
                'subjects_array': self.active_subjects_list,
            }
            pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
            f.close()
        except Exception as e:
            print('Unable to save data to active_subjects:', e)

        try:
            f = open('inactive_subjects', 'wb')
            save = {
                'subjects_array': self.inactive_subjects_list,
            }
            pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
            f.close()
        except Exception as e:
            print('Unable to save data to inactive_subjects:', e)

        #self.cross_road_function()
        self.subjects_page(1)


    def save_subject_arrays(self):

        try:
            f = open('active_subjects', 'wb')
            save = {
                'subjects_array': self.active_subjects_list,
            }
            pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
            f.close()
        except Exception as e:
            print('Unable to save data to active_subjects:', e)

        try:
            f = open('inactive_subjects', 'wb')
            save = {
                'subjects_array': self.inactive_subjects_list,
            }
            pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
            f.close()
        except Exception as e:
            print('Unable to save data to inactive_subjects:', e)

    def save_attendace(self):

        try:
            f = open('attendance', 'wb')
            save = {
                'attendance': self.attendance,
                'groups': self.groups,
            }
            pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
            f.close()
        except Exception as e:
            print('Unable to save data to attendance:', e)



    def load_data(self, file):

        try:
            with open(file, 'rb') as f:
                data = pickle.load(f)

            subjects_array = data['subjects_array']

            return subjects_array
        except Exception as e:
            print('Unable to read data from '+ file+  ':', e)

    def load_attendace(self):

        try:
            with open('attendance', 'rb') as f:
                data = pickle.load(f)

                attendance = data['attendance']

            return attendance
        except Exception as e:
            print('Unable to read data from attendance:', e)

    def load_groups(self):

        try:
            with open('attendance', 'rb') as f:
                data = pickle.load(f)

                groups = data['groups']

            return groups
        except Exception as e:
            print('Unable to read data from attendance:', e)

    def move_subject(self, subject, tab_number):
        if subject in self.active_subjects_list:
            self.active_subjects_list.remove(subject)
            self.inactive_subjects_list.append(subject)

        else:
            self.inactive_subjects_list.remove(subject)
            self.active_subjects_list.append(subject)

        self.save_subject_arrays()
        self.subjects_page(tab_number)





    def subjects_page(self,tab_number):
        self.clear_frame()

        self.active_subjects_list = self.load_data('active_subjects')
        self.inactive_subjects_list = self.load_data('inactive_subjects')

        if not self.inactive_subjects_list:

            back_button = Button(text="Logout", command=self.login_page)
            sync_button= Button(text="Sync")
            tmp_button = Button(text="Start", command=self.read_card)

            if (len(self.active_subjects_list)):

                for i in range(1, len(self.active_subjects_list) + 1):
                    a = i
                    b = i * 10
                    c = i * 10 + 1
                    d = i * 10 + 2

                    a = Label(text=self.active_subjects_list[i - 1])
                    b = Button(text="Subject info",
                               command=lambda text=self.active_subjects_list[i - 1]:
                               self.subject_info_page(text, "Skupina"))
                    c = Button(text="Create record")
                    d = Button(text="Disable",
                               command=lambda text=self.active_subjects_list[i - 1]: self.move_subject(text, 1))

                    a.place(relx=0.375, x=-180, rely=0.20, y=(i * 30), width=120, height=25)
                    b.place(relx=0.375, x=-60, rely=0.20, y=(i * 30), width=120, height=25)
                    c.place(relx=0.375, x=+60, rely=0.20, y=(i * 30), width=120, height=25)
                    d.place(relx=0.375, x=+180, rely=0.20, y=(i * 30), width=120, height=25)

            back_button.place(relx=0.375, rely=0.63, width=150, height=25)
            sync_button.place(relx=0.65, x=+38, y=0, width=75, height=25)
            tmp_button.place(relx=0.65, x=-38, y=0, width=75, height=25)

        else:

            tabControl = ttk.Notebook(self)

            tab1 = ttk.Frame(tabControl)
            tab2 = ttk.Frame(tabControl)

            tabControl.add(tab1, text='Active')
            tabControl.add(tab2, text='Inactive')
            back_button_tab1 = Button(tab1, text="Back", command=self.login_page)
            back_button_tab2 = Button(tab2, text="Back", command=self.login_page)
            sync_button_tab1 = Button(tab1, text="Sync")
            sync_button_tab2 = Button(tab2, text="Sync")


            if (len(self.active_subjects_list)):

                for i in range(1, len(self.active_subjects_list) + 1):
                    a = i
                    b = i * 10
                    c = i * 10 + 1
                    d = i * 10 + 2

                    a = Label(tab1, text=self.active_subjects_list[i - 1])
                    b = Button(tab1, text="Subject info", command=lambda text=self.active_subjects_list[i - 1]: self.subject_info_page(text,"Skupina"))
                    c = Button(tab1, text="Create record")
                    d = Button(tab1, text="Disable",
                               command=lambda text=self.active_subjects_list[i - 1]: self.move_subject(text,1))

                    a.place(relx=0.375, x=-180, rely=0.20, y=(i * 30), width=120, height=25)
                    b.place(relx=0.375, x=-60, rely=0.20, y=(i * 30), width=120, height=25)
                    c.place(relx=0.375, x=+60, rely=0.20, y=(i * 30), width=120, height=25)
                    d.place(relx=0.375, x=+180, rely=0.20, y=(i * 30), width=120, height=25)

            if (len(self.inactive_subjects_list)):

                for i in range(1, len(self.inactive_subjects_list) + 1):
                    a = i
                    b = i * 10

                    a = Label(tab2, text=self.inactive_subjects_list[i - 1])
                    b = Button(tab2, text="Enable",
                               command=lambda text=self.inactive_subjects_list[i - 1]: self.move_subject(text,2))

                    a.place(relx=0.375, x=-60, rely=0.20, y=(i * 30), width=120, height=25)
                    b.place(relx=0.375, x=+60, rely=0.20, y=(i * 30), width=120, height=25)

            back_button_tab1.place(relx=0.375, rely=0.63, width=150, height=25)
            back_button_tab2.place(relx=0.375, rely=0.63, width=150, height=25)
            sync_button_tab1.place(relx=0.65, x=+38, y=0, width=75, height=25)
            sync_button_tab2.place(relx=0.65, x=+38, y=0, width=75, height=25)

            tabControl.pack(expand=1, fill="both")

            if tab_number == 1:
                tabControl.select(tab1)
            else:
                tabControl.select(tab2)

    def subject_info_page(self, subject_name, group):

        self.clear_frame()
        colors = ["red", "green","yellow","black","gray","yellow"]
        word_dict = self.load_groups()

        dochadzka = self.load_attendace()

        self.attendance= dochadzka
        self.groups = word_dict



        title_label = Label(self, text=subject_name, font=self.title_font)
        back_button = Button(self, text="Back", command=lambda :self.subjects_page(1))

        self.popupMenu = Menu(self, tearoff=0)
        self.popupMenu.add_command(label="red", command= lambda :self.change_attendance(subject_name,group,0))
        self.popupMenu.add_command(label="green", command= lambda :self.change_attendance(subject_name,group,1))
        self.popupMenu.add_command(label="yellow", command= lambda :self.change_attendance(subject_name,group,2))
        self.popupMenu.add_command(label="black", command= lambda :self.change_attendance(subject_name,group,3))
        self.popupMenu.add_command(label="gray", command= lambda :self.change_attendance(subject_name,group,4))

        self.popupMenu2 = Menu(self, tearoff=0)
        self.popupMenu2.add_command(label="Change group", command= lambda: self.change_group(group,subject_name))

        OPTIONS = []
        for i in range(1,20):
            OPTIONS.append("Skupina " + str(i))

        variable = StringVar(self)
        variable.set(group)

        w = OptionMenu(self, variable, *OPTIONS)
        w.place(relx=0.375, x=-100, rely=0.18, width=150, height=25)



        button = Button(self, text="Select", command= lambda: self.subject_info_page(subject_name,variable.get()))
        button.place(relx=0.375, x=100, rely=0.18, width=150, height=25)

        if group is not "Skupina":
            i = 0

            for k in range (0,12):
                t =k
                t = Label(self, text=str(k+1))
                t.place(relx=0.35, x=+(k*25), rely=0.26, width=20, height=20)
            for name in  word_dict[group]:

                a = name
                a = Label(self, text= name, anchor="w")
                a.place(x=30, y=150+(i*20), width=200, height=20)
                a.bind(self.right_click, self.popup_student)
                a.bind("<Enter>", self.on_enter)


                for j in range (0,12):
                    g= j
                    g = Label(self,text = name+ "_" + str(j),bg = colors[dochadzka[name][j]], fg = colors[dochadzka[name][j]])
                    g.place(relx=0.35, x=+(j*25), rely=0.26, y=+25+(i * 20), width=18, height=18)
                    g.bind(self.right_click, self.popup)
                    g.bind("<Button-1>",lambda event : self.left_click(event,subject_name,group))
                    g.bind("<Enter>", self.on_enter)

                i = i +1

        title_label.place(relx=0.270, rely=0.08, width=300, height=25)
        back_button.place(relx=0.375, rely=0.63, width=150, height=25)

    def left_click(self,event,subject_name,group):

        name, week = str(self.selected).split('_')

        if self.attendance[str(name)][int(week)] == 1:
            self.change_attendance(subject_name,group,3)
        else:
            self.change_attendance(subject_name, group, 1)

    def popup(self, event):
        self.popupMenu.post(event.x_root, event.y_root)

    def popup_student(self, event):
        self.popupMenu2.post(event.x_root, event.y_root)

    def on_enter(self, event):
        self.selected = event.widget['text']

    def close_window(self, window):
        window.destroy()

    def move_stundet_to_other_group(self, window, from_group, to_group, subject_name):

        self.groups[to_group].append(self.selected)
        self.groups[from_group].remove(self.selected)
        self.save_attendace()
        self.subject_info_page(subject_name, to_group)

        self.close_window(window)

    def change_group(self, group, subject_name):

        toplevel = Toplevel()
        toplevel.geometry("320x35")
        OPTIONS = []

        for i in range(1, 20):
            OPTIONS.append("Skupina " + str(i))

        variable = StringVar(self)
        variable.set(OPTIONS[0])

        w = OptionMenu(toplevel, variable, *OPTIONS)
        w.place(x=5, y=5, width=150, height=25)

        button = Button(toplevel, text="Select",
                        command=lambda: self.move_stundet_to_other_group(toplevel, group, variable.get(), subject_name))
        button.place(x=160, y=5, width=150, height=25)

    def change_attendance(self,subject_name,group,a):
        name,week = str(self.selected).split('_')
        self.attendance[str(name)][int(week)]=a
        self.save_attendace()
        self.subject_info_page(subject_name,group)

    def read_card(self):
        if(self.monitored==0):
            self.monitored=1
            self.read = rc.read_card2()
            self.cardmonitor = self.read.readCards()
        else:
            self.monitored=0
            self.read.stopReadCards(self.cardmonitor)


app = Application()

app.mainloop()
