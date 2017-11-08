from tkinter import *
from tkinter import font  as tkfont
from tkinter import ttk



class Application(Tk):
    #GUI Application

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("600x500")
        self.login_page()

    def clear_frame(self):
        # clear frame
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
        self.login_button = Button(self, text="Login", command = self.select_action_page )

        self.title_label.place(x=200, y=80, width=120, height=25)
        self.username_label.place(x=150, y=125, width=120, height=25)
        self.password_label.place(x=150, y=150, width=120, height=25)
        self.username_entry.place(x=255, y=125, width=120, height=25)
        self.password_entry.place(x=255, y=150, width=120, height=25)
        self.checkbox.place(x=200, y=175, width=120, height=25)
        self.login_button.place(x=200, y=210, width=120, height=25)



    def select_action_page(self):

        self.clear_frame()

        self.title_label = Label(self, text="Select Action",font=self.title_font)
        self.subjects_button = Button(self, text="Subjects", command = self.subjects_page)
        self.upload_button = Button(self, text='Upload records',command = self.upload_page)
        self.download_button = Button(self, text="Download student lists")

        self.title_label.place(x=200, y=40, width=160, height=25)
        self.subjects_button.place(x=215, y=120, width=120, height=25)
        self.upload_button.place(x=215, y=150, width=120, height=25)
        self.download_button.place(x=185, y=180, width=170, height=25)


    def subjects_page(self):

        self.clear_frame()

        subjects_araay = ["JOS" , "PT", "Logika"]

        self.title_label = Label(self, text="Subjects", font=self.title_font)
        self.back_button = Button(self, text="Back", command = self.select_action_page)

        for i in range(1,len(subjects_araay)+1):
            a = i
            b = i * 10
            c = i * 10 + 1

            self.a = Label(self, text= subjects_araay[i-1])
            self.b = Button(self,text="Subject info", command = self.subject_info_page)
            self.c = Button(self,text="Create record", command =self.select_event_page)


            self.a.place(x=95, y=90 + (i * 30), width=120, height=25)
            self.b.place(x=215, y=90+(i*30), width=120, height=25)
            self.c.place(x=335, y=90+(i*30), width=120, height=25)

        self.title_label.place(x=200, y=40, width=160, height=25)
        self.back_button.place(x=200, y=120 + 30*(i+1), width=150, height=25)

    def subject_info_page(self):

        self.clear_frame()

        self.title_label = Label(self, text="Subject Info", font=self.title_font)
        self.back_button = Button(self, text="Back", command = self.subjects_page)
        self.tree = ttk.Treeview(self)

        self.tree["columns"] = ("one", "two", "three")
        self.tree.column("one", width=50)
        self.tree.column("two", width=70)
        self.tree.column("three", width=70)

        self.tree.heading("one", text="Class")
        self.tree.heading("two", text="Number of")
        self.tree.heading("three", text="Status")

        self.tree.insert("", 0, text="22.10.2017 - 15:00", values=("18", "22", "NOT OK"))

        self.title_label.place(x=200, y=40, width=160, height=25)
        self.tree.place(x=100, y=80)
        self.back_button.place(x=220, y=300, width=150, height=25)


    def select_event_page(self):

        self.clear_frame()

        self.title_label = Label(self, text="SelectEvent", font=self.title_font)
        self.date_label = Label(self, text="22.10.2017")
        self.time_label = Label(self, text="15:00")
        self.class_label = Label(self, text="Class 01")
        self.select_button = Button(self, text="Select", command = self.agree_page)
        self.back_button = Button(self, text="Back", command = self.subjects_page)


        self.title_label.place(x=220, y=40, width=160, height=25)
        self.date_label.place(x=150, y=120, width=130, height=25)
        self.time_label.place(x=258, y=120, width=50, height=25)
        self.class_label.place(x=310, y=120, width=60, height=25)
        self.select_button.place(x=380, y=120, width=60, height=25)
        self.back_button.place(x=220, y=300, width=150, height=25)



    def agree_page(self):

        self.clear_frame()

        self.title_label = Label(self, text="22.10.2017-15:00-Class 01", font=self.title_font)
        self.agree_button = Button(self, text="Agree", command = self.isic_page)
        self.disagree_button = Button(self, text="Disagree",command =self.select_event_page)


        self.title_label.place(x=120, y=40, width=350, height=25)
        self.agree_button.place(x=215, y=150, width=80, height=25)
        self.disagree_button.place(x=295, y=150, width=80, height=25)


    def isic_page(self):

        self.clear_frame()

        self.title_label = Label(self, text="Add isic", font=self.title_font)
        self.close_button = Button(self, text="Close and save", command=self.select_action_page)

        self.title_label.place(x=220, y=40, width=160, height=25)
        self.close_button.place(x=220, y=190, width=150, height=25)

    def upload_page(self):

        self.clear_frame()

        self.title_label = Label(self, text="Do you want upload records? ", font=self.title_font)
        self.agree_button = Button(self, text="Yes",command = self.select_action_page)
        self.disagree_button = Button(self, text="No", command =self.select_action_page)

        self.title_label.place(x=130, y=40, width=350, height=25)
        self.agree_button.place(x=215, y=150, width=80, height=25)
        self.disagree_button.place(x=295, y=150, width=80, height=25)



app = Application()

app.mainloop()