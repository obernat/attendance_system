from tkinter  import *               # python 3
from tkinter import font  as tkfont # python 3
import tkinter.messagebox as tm
from PIL import Image, ImageTk


#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

class SampleApp(Tk):

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
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()


class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.label = Label(self, text="Login", font=controller.title_font)
        self.label_1 = Label(self, text="Username")
        self.label_2 = Label(self, text="Password")

        self.entry_1 = Entry(self)
        self.entry_2 = Entry(self, show="*")

        self.label.grid(columnspan=2)
        self.label_1.grid(row=1, sticky=E)
        self.label_2.grid(row=2, sticky=E)
        self.entry_1.grid(row=1, column=1)
        self.entry_2.grid(row=2, column=1)

        self.checkbox = Checkbutton(self, text="Keep me logged in")
        self.checkbox.grid(columnspan=2)

        self.logbtn = Button(self, text="Login", command=self._login_btn_clickked)
        self.logbtn.grid(columnspan=2)

        self.pack()

    def _login_btn_clickked(self):

        username = self.entry_1.get()
        password = self.entry_2.get()

        if username == "matus" and password == "pass":
            self.controller.show_frame("PageTwo")
        else:
            tm.showinfo("Login info", "Wrong Password or Username")


class PageTwo(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.label = Label(self, text="This is page 2", font=controller.title_font)

        self.button = Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        list_img = Image.open('list_img.png')
        download_img = Image.open("download_img.png")
        upload_img = Image.open("upload_img.png")

        list_icon = ImageTk.PhotoImage(list_img)
        download_icon = ImageTk.PhotoImage(download_img)
        upload_icon = ImageTk.PhotoImage(upload_img)

        self.list_button = Button(self, height=10, width=20)

        self.download_button = Label(self, height=10, width=20, text='sdknfsdlkjndsflkn')
        self.upload_button = Button(self, height=20, width=20)
        # self.download_button = Button(self, image= download_icon)
        # self.upload_button = Button(self, image= upload_icon)

        self.list_button.grid(row=1, column=1)
        self.download_button.grid(row=1, column=2)
        self.upload_button.grid(row=1, column=3)
        self.button.grid(row =2,column=2)

        self.pack()


if __name__ == "__main__":

    app = SampleApp()
    app.mainloop()