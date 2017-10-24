from tkinter  import *               # python 3
from tkinter import font  as tkfont # python 3
import tkinter.messagebox as tm
from PIL import Image, ImageTk
import sqlite3


#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

class GUI(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("700x500")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack()


        self.frames = {}
        for F in (LoginPage, SelectActionPage, ListOfSubjects):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()



class LoginPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Frame.grid(self,row=10, column=11)
        self.controller = controller
        self.label = Label(self, text="Login", font=controller.title_font)
        self.label_1 = Label(self, text="Username")
        self.label_2 = Label(self, text="Password")

        self.entry_1 = Entry(self)
        self.entry_2 = Entry(self, show="*")


        self.checkbox = Checkbutton(self, text="Keep me logged in")
        self.logbtn = Button(self, text="Login", command=self._login_btn_clickked)


        self.label.place(x=200, y=80, width=120, height=25)
        self.label_1.place(x=150,y=125,width=120, height=25)
        self.label_2.place(x=150,y=150,width=120, height=25)
        self.entry_1.place(x=255,y=125,width=120, height=25)
        self.entry_2.place(x=255,y=150,width=120, height=25)
        self.checkbox.place(x=200,y=175,width=120, height=25)
        self.logbtn.place(x=200,y=200,width=120, height =25)

        self.pack()

    def _login_btn_clickked(self):

        username = self.entry_1.get()
        password = self.entry_2.get()

        if username == "matus" and password == "pass":
            self.controller.show_frame("SelectActionPage")
        else:
            tm.showinfo("Login info", "Wrong Password or Username")


class SelectActionPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.label = Label(self, text="Select Action", font=controller.title_font)
        self.button = Button(self, text="Logout",
                           command=lambda: controller.show_frame("LoginPage"))

        list_img = Image.open('list_img.png')
        download_img = Image.open("download_img.png")
        upload_img = Image.open("upload_img.png")

        list_icon = ImageTk.PhotoImage(list_img)
        download_icon = ImageTk.PhotoImage(download_img)
        upload_icon = ImageTk.PhotoImage(upload_img)

        self.list_button = Button(self, text= "List of subjects",
                            command=lambda: controller.show_frame("ListOfSubjects"))
        self.download_button = Button(self, height=400, width=200, text='Upload zaznami',
                                     command=lambda: controller.show_frame("ListOfSubjects"), image= download_icon)
        self.upload_button = Button(self, height=400, width=200, text= "Stiahnut zoznami studentov",
                                    command = lambda: controller.show_frame("ListOfSubjects"), image = upload_icon)
        # self.download_button = Button(self, image= download_icon)
        # self.upload_button = Button(self, image= upload_icon)

        self.list_button.grid(row=1, column=1)
        self.download_button.grid(row=1, column=2)
        self.upload_button.grid(row=1, column=3)
        self.button.grid(row =2,column=2)

        self.pack()


class ListOfSubjects(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.label = Label(self, text="Subjects", font=controller.title_font)
        self.button = Button(self, text="Logout",
                           command=lambda: controller.show_frame("LoginPage"))
        self.button_2 = Button(self, text="Back",
                             command=lambda: controller.show_frame("SelectActionPage"))

        subjects_araay = ["JOS" , "PT", "Logika"]
        self.label.grid(row=0, columnspan=2)

        for i in range(1,len(subjects_araay)+1):
            self.i = Label(self, text= subjects_araay[i-1])
            self.i.grid(row=1*i, column=1)
            a = i*10
            b= i*10 + 1
            self.a = Button(self)
            self.a.grid(row=1*i, column=2)
            self.b = Button(self)
            self.b.grid(row=1*i, column=3)

        self.button.grid(row=len(subjects_araay)+2, column=1)
        self.button_2.grid(row=len(subjects_araay)+2, column=2)


        self.pack()

if __name__ == "__main__":

    app = GUI()
    app.mainloop()