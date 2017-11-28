from tkinter import *
from tkinter import font  as tkfont
from tkinter import ttk
from six.moves import cPickle as pickle
import os
import time
import sys
import requests
sys.path.append("../")
import is_parser as isp



class Application(Tk):
    #GUI Application

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("600x500")
        self.login_page()
        self.selected = 0
        self.session = requests.Session()

    def clear_frame(self):

        for child in self.winfo_children():
            child.destroy()

    def login_page(self):

        self.clear_frame()

        self.title_label = Label(self, text="Login" ,font=self.title_font)
        self.username_label = Label(self, text="Username")
        self.password_label = Label(self, text="Password")
        self.username_entry = Entry(self)
        self.password_entry = Entry(self, show="*")
        self.checkbox = Checkbutton(self, text="Keep me logged in")
        self.login_button = Button(self, text="Login", command = lambda: self.cross_road_function(self.username_entry.get(),self.password_entry.get()))
        self.remove_button = Button(self, text="Remove files", command = self.remove_files )


        self.title_label.place(x=200, y=80, width=120, height=25)
        self.username_label.place(x=150, y=125, width=120, height=25)
        self.password_label.place(x=150, y=150, width=120, height=25)
        self.username_entry.place(x=255, y=125, width=120, height=25)
        self.password_entry.place(x=255, y=150, width=120, height=25)
        self.checkbox.place(x=200, y=175, width=120, height=25)
        self.login_button.place(x=200, y=210, width=120, height=25)
        self.remove_button.place(x=200, y=235, width=120, height=25)

    def sync_page(self):

        self.clear_frame()

        self.sync_button = Button(self, text='Sync', command=self.load_subjects)
        self.sync_button.place(x=235, y=150, width=120, height=25)

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
        if isp.try_login(self.session, name, password) < 0:
            print ("TU VYHODIME EXCEPTION ZE NEPODARILO SA PRIHLASIT (NESPRAVNE MENO/HESLO/INTERNET)")
            return

        #if self.file_check('active_subjects'):
        if os.path.isfile('active_subjects'):
            self.subjects_page(1)
        else:
            self.sync_page()









    def load_subjects(self):

        ret_value, subjects_list_with_links = isp.get_subjects(self.session)
        if ret_value < 0:
            print ("TU VYHODIME EXCEPTION ZE ZIADNE PREDMETY NEMAME")
            return

        self.active_subjects_list = []
        for subject in subjects_list_with_links:
            self.active_subjects_list.append(subject[0])

        self.inactive_subjects_list = ["Haha"]

        word_dict = dict()
        word_dict["Skupina 1"] = ["Matus", "Tomas", "Dano"]
        word_dict["Skupina 2"] = ["Matus2", "Tomas2", "Dano2"]

        dochadzka = dict()
        dochadzka["Matus"] = [0, 2, 3, 4, 5, 1, 1, 1, 1, 1, 1, 1]
        dochadzka["Tomas"] = [1, 2, 3, 4, 5, 1, 1, 1, 1, 3, 3, 3]
        dochadzka["Dano"] = [1, 2, 3, 4, 5, 1, 1, 1, 2, 4, 1, 1]
        dochadzka["Matus2"] = [1, 2, 3, 4, 5, 1, 5, 1, 1, 1, 1, 1]
        dochadzka["Tomas2"] = [1, 2, 3, 4, 5, 1, 1, 5, 4, 1, 1, 1]
        dochadzka["Dano2"] = [1, 2, 3, 4, 5, 1, 1, 1, 1, 2, 3, 1]

        try:
            f = open('attendance', 'wb')
            save = {
                'attendance': dochadzka,
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

        self.cross_road_function()

















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

    def move_subject(self, subject, tab_number):
        if subject in self.active_subjects_list:
            self.active_subjects_list.remove(subject)
            self.inactive_subjects_list.append(subject)

        else:
            self.inactive_subjects_list.remove(subject)
            self.active_subjects_list.append(subject)

        self.save_subject_arrays()
        self.subjects_page_edit(tab_number)


    def subjects_page(self, tab_number):
        self.clear_frame()

        tabControl = ttk.Notebook(self)

        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)

        tabControl.add(tab1, text='Active')
        tabControl.add(tab2, text='Inactive')
        back_button_tab1 = Button(tab1, text="Back", command = self.login_page)
        back_button_tab2 = Button(tab2, text="Back", command = self.login_page)
        edit_button_tab1 = Button(tab1, text="Edit", command=lambda : self.subjects_page_edit(1))
        edit_button_tab2 = Button(tab2, text="Edit", command=lambda : self.subjects_page_edit(2))



        self.active_subjects_list = self.load_data('active_subjects')
        self.inactive_subjects_list = self.load_data('inactive_subjects')


        if(len(self.active_subjects_list)):

            for i in range(1, len(self.active_subjects_list) + 1):

                a = i
                b = i * 10
                c = i * 10 + 1
                d = i * 10 + 2

                a = Label(tab1, text=self.active_subjects_list[i - 1])
                b = Button(tab1, text="Subject info", command=lambda text=self.active_subjects_list[i - 1]: self.subject_info_page(text,"Skupina"))
                c = Button(tab1, text="Create record")

                a.place(x=105, y=90 + (i * 30), width=120, height=25)
                b.place(x=225, y=90 + (i * 30), width=120, height=25)
                c.place(x=345, y=90 + (i * 30), width=120, height=25)

        if(len(self.inactive_subjects_list)):

            for i in range(1, len(self.inactive_subjects_list) + 1):

                a = i
                b = i * 10

                a = Label(tab2, text=self.inactive_subjects_list[i - 1])

                a.place(x=220, y=90 + (i * 30), width=120, height=25)

        back_button_tab1.place(x=200, y=300, width=150, height=25)
        back_button_tab2.place(x=200, y=300, width=150, height=25)
        edit_button_tab1.place(x=470, y=0, width=75, height=25)
        edit_button_tab2.place(x=470, y=0, width=75, height=25)

        tabControl.pack(expand=1, fill="both")

        if tab_number == 1:
            tabControl.select(tab1)
        else:
            tabControl.select(tab2)



    def subjects_page_edit(self,tab_number):
        self.clear_frame()

        tabControl = ttk.Notebook(self)

        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)

        tabControl.add(tab1, text='Active')
        tabControl.add(tab2, text='Inactive')
        back_button_tab1 = Button(tab1, text="Back", command=self.login_page)
        back_button_tab2 = Button(tab2, text="Back", command=self.login_page)
        save_button_tab1 = Button(tab1, text="Save changes", command=lambda : self.subjects_page(1))
        save_button_tab2 = Button(tab2, text="Save changes",command= lambda : self.subjects_page(2))
        sync_button_tab1 = Button(tab1, text="Sync")
        sync_button_tab2 = Button(tab2, text="Sync")

        self.active_subjects_list = self.load_data('active_subjects')
        self.inactive_subjects_list = self.load_data('inactive_subjects')

        if (len(self.active_subjects_list)):

            for i in range(1, len(self.active_subjects_list) + 1):
                a = i
                b = i * 10
                c = i * 10 + 1
                d = i * 10 + 2

                a = Label(tab1, text=self.active_subjects_list[i - 1])
                b = Button(tab1, text="Subject info")
                c = Button(tab1, text="Create record")
                d = Button(tab1, text="Disable",
                           command=lambda text=self.active_subjects_list[i - 1]: self.move_subject(text,1))

                a.place(x=45, y=90 + (i * 30), width=120, height=25)
                b.place(x=165, y=90 + (i * 30), width=120, height=25)
                c.place(x=285, y=90 + (i * 30), width=120, height=25)
                d.place(x=405, y=90 + (i * 30), width=120, height=25)

        if (len(self.inactive_subjects_list)):

            for i in range(1, len(self.inactive_subjects_list) + 1):
                a = i
                b = i * 10

                a = Label(tab2, text=self.inactive_subjects_list[i - 1])
                b = Button(tab2, text="Enable",
                           command=lambda text=self.inactive_subjects_list[i - 1]: self.move_subject(text,2))

                a.place(x=145, y=90 + (i * 30), width=120, height=25)
                b.place(x=265, y=90 + (i * 30), width=120, height=25)

        back_button_tab1.place(x=200, y=300, width=150, height=25)
        back_button_tab2.place(x=200, y=300, width=150, height=25)
        save_button_tab1.place(x=425, y=0, width=120, height=25)
        save_button_tab2.place(x=425, y=0, width=120, height=25)
        sync_button_tab1.place(x=340, y=0, width=75, height=25)
        sync_button_tab2.place(x=340, y=0, width=75, height=25)

        tabControl.pack(expand=1, fill="both")

        if tab_number == 1:
            tabControl.select(tab1)
        else:
            tabControl.select(tab2)

    def subject_info_page(self, subject_name, group):

        self.clear_frame()
        colors = ["red", "green","yellow","black","gray","yellow"]
        word_dict = dict()
        word_dict["Skupina 1"] = ["Matus", "Tomas", "Dano" ]
        word_dict["Skupina 2"] = ["Matus2", "Tomas2", "Dano2" ]

        dochadzka = self.load_attendace()

        self.attendance= dochadzka



        title_label = Label(self, text=subject_name, font=self.title_font)
        back_button = Button(self, text="Back", command=lambda :self.subjects_page(1))

        self.popupMenu = Menu(self, tearoff=0)
        self.popupMenu.add_command(label="red", command= lambda :self.change_attendance(subject_name,group,0))
        self.popupMenu.add_command(label="green", command= lambda :self.change_attendance(subject_name,group,1))
        self.popupMenu.add_command(label="yellow", command= lambda :self.change_attendance(subject_name,group,2))
        self.popupMenu.add_command(label="black", command= lambda :self.change_attendance(subject_name,group,3))
        self.popupMenu.add_command(label="gray", command= lambda :self.change_attendance(subject_name,group,4))

        OPTIONS = []
        for i in range(1,20):
            OPTIONS.append("Skupina " + str(i))

        variable = StringVar(self)
        variable.set(group)

        w = OptionMenu(self, variable, *OPTIONS)
        w.place(x=150, y=80, width=150, height=25)



        button = Button(self, text="Select", command= lambda: self.subject_info_page(subject_name,variable.get()))
        button.place(x=315, y=80, width=150, height=25)

        if group is not "Skupina":
            i = 0

            for k in range (0,12):
                t =k
                t = Label(self, text=str(k+1))
                t.place(x=235+(k*25), y=120, width=20, height=20)
            for name in  word_dict[group]:

                a = name
                a = Label(self, text= name, anchor="w")
                a.place(x=30, y=150+(i*20), width=200, height=20)


                for j in range (0,12):
                    g= j
                    g = Label(self,text = name+ "_" + str(j),bg = colors[dochadzka[name][j]], fg = colors[dochadzka[name][j]])
                    g.place(x=235+(j*25), y=150 + (i * 20), width=18, height=18)
                    g.bind("<Button-2>", self.popup)
                    g.bind("<Enter>", self.on_enter)

                i = i +1

        title_label.place(x=200, y=40, width=160, height=25)
        back_button.place(x=220, y=300, width=150, height=25)

    def popup(self, event):
        self.popupMenu.post(event.x_root, event.y_root)

    def on_enter(self, event):
        self.selected = event.widget['text']


    def change_attendance(self,subject_name,group,a):
        print(self.selected,a)
        name,week = str(self.selected).split('_')
        self.attendance[str(name)][int(week)]=a
        self.save_attendace()
        self.subject_info_page(subject_name,group)
app = Application()

app.mainloop()
