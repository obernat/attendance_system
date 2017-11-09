from tkinter import *
from tkinter import font  as tkfont
from tkinter import ttk
from six.moves import cPickle as pickle
import os



class Application(Tk):
    #GUI Application

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("600x500")
        self.login_page()

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
        self.login_button = Button(self, text="Login", command = self.cross_road_function )
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

    def file_check(slef,file):

        try:
            open(file, "r")
            return 1
        except IOError:
            return 0

    def remove_files(self):

        os.remove('active_subjects')
        os.remove('inactive_subjects')

    def cross_road_function(self):

        if self.file_check('active_subjects'):
            self.subjects_page()
        else:
            self.sync_page()

    def load_subjects(self):

        self.active_subjects_array = ["JOS", "PT", "Logika"]
        self.inactive_subjects_array = ["Haha"]
        try:
            f = open('active_subjects', 'wb')
            save = {
                'subjects_array': self.active_subjects_array,
            }
            pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
            f.close()
        except Exception as e:
            print('Unable to save data to active_subjects:', e)

        try:
            f = open('inactive_subjects', 'wb')
            save = {
                'subjects_array': self.inactive_subjects_array,
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
                'subjects_array': self.active_subjects_array,
            }
            pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
            f.close()
        except Exception as e:
            print('Unable to save data to active_subjects:', e)

        try:
            f = open('inactive_subjects', 'wb')
            save = {
                'subjects_array': self.inactive_subjects_array,
            }
            pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
            f.close()
        except Exception as e:
            print('Unable to save data to inactive_subjects:', e)


    def load_data(self, file):

        try:
            with open(file, 'rb') as f:
                data = pickle.load(f)

            subjects_array = data['subjects_array']

            return subjects_array
        except Exception as e:
            print('Unable to read data from '+ file+  ':', e)

    def move_subject(self, subject):
        if subject in self.active_subjects_array:
            self.active_subjects_array.remove(subject)
            self.inactive_subjects_array.append(subject)

        else:
            self.inactive_subjects_array.remove(subject)
            self.active_subjects_array.append(subject)

        self.save_subject_arrays()
        self.subjects_page()


    def subjects_page(self):
        self.clear_frame()

        tabControl = ttk.Notebook(self)

        tab1 = ttk.Frame(tabControl)
        tab2 = ttk.Frame(tabControl)

        tabControl.add(tab1, text='Active')
        tabControl.add(tab2, text='Inactive')
        back_button_tab1 = Button(tab1, text="Back", command = self.login_page)
        back_button_tab2 = Button(tab2, text="Back", command = self.login_page)

        self.active_subjects_array = self.load_data('active_subjects')
        self.inactive_subjects_array = self.load_data('inactive_subjects')


        if(len(self.active_subjects_array)):

            for i in range(1, len(self.active_subjects_array) + 1):

                a = i
                b = i * 10
                c = i * 10 + 1
                d = i * 10 + 2

                a = Label(tab1, text=self.active_subjects_array[i - 1])
                b = Button(tab1, text="Subject info")
                c = Button(tab1, text="Create record")
                d = Button(tab1, text="Disable", command= lambda text=self.active_subjects_array[i - 1]: self.move_subject(text))

                a.place(x=45, y=90 + (i * 30), width=120, height=25)
                b.place(x=165, y=90 + (i * 30), width=120, height=25)
                c.place(x=285, y=90 + (i * 30), width=120, height=25)
                d.place(x=405, y=90 + (i * 30), width=120, height=25)

        if(len(self.inactive_subjects_array)):

            for i in range(1, len(self.inactive_subjects_array) + 1):

                a = i
                b = i * 10

                a = Label(tab2, text=self.inactive_subjects_array[i - 1])
                b = Button(tab2, text="Enable", command= lambda text=self.inactive_subjects_array[i - 1]: self.move_subject(text))

                a.place(x=145, y=90 + (i * 30), width=120, height=25)
                b.place(x=265, y=90 + (i * 30), width=120, height=25)

        back_button_tab1.place(x=200, y=300, width=150, height=25)
        back_button_tab2.place(x=200, y=300, width=150, height=25)

        tabControl.pack(expand=1, fill="both")


app = Application()

app.mainloop()