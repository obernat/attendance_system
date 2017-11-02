import tkinter as tk
from tkinter import font  as tkfont
from tkinter import ttk


class SampleApp(tk.Tk):

    actual_page = "LoginPage"
    D = {'LoginPage': 'LoginPage', 'SelectActionPage': 'LoginPage','SubjectListsPage':'SelectActionPage',
         'UploadPage':'SelectActionPage','StudentListsPage':'SelectActionPage', 'SubjectInfoPage' :'SubjectListsPage',
         'SelectEventPage':'SubjectListsPage'}

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry('700x500')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        menu = tk.Menu(self)
        self.config(menu=menu)




        edit_menu = tk.Menu(menu)
        menu.add_cascade(label='Edit', menu= edit_menu)
        edit_menu.add_command(label='Previous page', command=lambda: self.show_frame(self.D[self.actual_page]))

        log_menu = tk.Menu(menu)
        menu.add_cascade(label='Logout', menu=log_menu)
        log_menu.add_command(label='Logout', command=lambda: self.show_frame("LoginPage"))

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack()



        self.frames = {}
        for F in (LoginPage, SelectActionPage, SubjectListsPage,SubjectInfoPage,SelectEventPage,AgreePage,
                  IsicPage,UploadPage,StudentListsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=10, column=10, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        self.actual_page = page_name
        frame.tkraise()


class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Login", font=controller.title_font)

        self.label_1 = tk.Label(self, text="Username")
        self.label_2 = tk.Label(self, text="Password")

        self.entry_1 = tk.Entry(self)
        self.entry_2 = tk.Entry(self, show="*")

        self.checkbox = tk.Checkbutton(self, text="Keep me logged in")
        self.logbtn = tk.Button(self, text="Login",
                         command=lambda: controller.show_frame("SelectActionPage"))


        self.label.grid(row=0, columnspan=2)
        self.label_1.grid(row=1,column=0)
        self.label_2.grid(row=2,column=0)

        self.entry_1.grid(row=1, column=1)
        self.entry_2.grid(row=2, column=1)
        self.checkbox.grid(row=3, columnspan=2)
        self.logbtn.grid(row=4, columnspan=2)



class SelectActionPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label = tk.Label(self, text="Select Action", font=controller.title_font)

        self.list_button = tk.Button(self, text= "Subjects",
                            command=lambda: controller.show_frame("SubjectListsPage"))
        self.download_button = tk.Button(self, text='Upload records',
                                     command=lambda: controller.show_frame("UploadPage"))
        self.upload_button = tk.Button(self, text= "Download student lists",
                                    command = lambda: controller.show_frame("StudentListsPage"))

        self.label.grid(row=0, columnspan=3)
        self.list_button.grid(row=1,column=0)
        self.download_button.grid(row=1,column=1)
        self.upload_button.grid(row=1,column=2)


class SubjectListsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label = tk.Label(self, text="Subjects", font=controller.title_font)
        self.label.grid(row=0, columnspan=3)


        subjects_araay = ["JOS" , "PT", "Logika"]

        for i in range(1,len(subjects_araay)+1):
            c = i
            self.c = tk.Label(self, text= subjects_araay[i-1])
            self.c.grid(row=1*i, column=0)
            a =i*10
            b= i*10 + 1
            self.a = tk.Button(self,text="Subject info",
                          command=lambda: controller.show_frame("SubjectInfoPage"))
            self.a.grid(row=1*i, column=1)
            self.b = tk.Button(self,text="Create record",
                          command=lambda: controller.show_frame("SelectEventPage"))
            self.b.grid(row=1*i, column=2)




class SubjectInfoPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label = tk.Label(self, text="Subject Info", font=controller.title_font)
        self.label.grid(row=0, column =1)

        self.tree = ttk.Treeview(self)

        self.tree["columns"] = ("one", "two","three")

        self.tree.column("one", width=50)
        self.tree.column("two", width=70)
        self.tree.column("three", width=70)


        self.tree.heading("one", text="Class")
        self.tree.heading("two", text="Number of")
        self.tree.heading("three", text="Status")





        self.tree.insert("", 0,text="22.10.2017 - 15:00", values=("18","22","NOT OK"))
        self.tree.grid(row=1, columnspan =3)


class SelectEventPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label = tk.Label(self, text="SelectEvent", font=controller.title_font)
        self.label_2 = tk.Label(self, text="22.10.2017")
        self.label_3 = tk.Label(self, text="15:00")
        self.label_4 = tk.Label(self, text="Class 01")

        self.button_1 = tk.Button(self, text="Select",
                             command = lambda: controller.show_frame("AgreePage"))


        self.label.grid(row=0, columnspan=4)
        self.label_2.grid(row=1, column =0)
        self.label_3.grid(row=1, column=1)

        self.label_4.grid(row=1, column=2)

        self.button_1.grid(row=1, column=3)




class AgreePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


        self.label = tk.Label(self, text="Predmet datum cas ", font=controller.title_font)
        self.button = tk.Button(self, text="Agree",
                                command=lambda: controller.show_frame("IsicPage"))
        self.button_2 = tk.Button(self, text="Disagree",
                                  command=lambda: controller.show_frame("SelectEventPage"))

        self.label.grid(row=0, columnspan=3)
        self.button.grid(row=1, column=0)
        self.button_2.grid(row=1, column=1)

class IsicPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Prilozte isic", font=controller.title_font)
        button = tk.Button(self, text="Close and save",
                           command=lambda: controller.show_frame("SelectActionPage"))


        label.pack()
        button.pack()

class StudentListsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Student Lists", font=controller.title_font)
        button = tk.Button(self, text="Logout",
                           command=lambda: controller.show_frame("LoginPage"))
        button_2 = tk.Button(self, text="Back",
                             command=lambda: controller.show_frame("SelectActionPage"))



        label.pack()
        button.pack()
        button_2.pack()



class UploadPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label = tk.Label(self, text="Do you want upload records? ", font=controller.title_font)
        self.button = tk.Button(self, text="Yes",
                           command=lambda: controller.show_frame("SelectActionPage"))
        self.button_2 = tk.Button(self, text="No",
                             command=lambda: controller.show_frame("SelectActionPage"))

        self.label.grid(row=0,columnspan=3)
        self.button.grid(row=1,column=0)
        self.button_2.grid(row=1, column=1)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()