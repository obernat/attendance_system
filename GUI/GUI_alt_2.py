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

        self.label = Label(self, text="Login" ,font=self.title_font)

        self.label_2 = Label(self, text="Username")
        self.label_3 = Label(self, text="Password")

        self.entry_1 = Entry(self)
        self.entry_2 = Entry(self, show="*")

        self.checkbox = Checkbutton(self, text="Keep me logged in")
        self.logbtn = Button(self, text="Login", command = self.select_action_page )

        self.label.place(x=200, y=80, width=120, height=25)
        self.label_2.place(x=150, y=125, width=120, height=25)
        self.label_3.place(x=150, y=150, width=120, height=25)
        self.entry_1.place(x=255, y=125, width=120, height=25)
        self.entry_2.place(x=255, y=150, width=120, height=25)
        self.checkbox.place(x=200, y=175, width=120, height=25)
        self.logbtn.place(x=200, y=210, width=120, height=25)



    def select_action_page(self):

        self.clear_frame()

        self.label = Label(self, text="Select Action",font=self.title_font)

        self.list_button = Button(self, text="Subjects")
        self.download_button = Button(self, text='Upload records',command = self.upload_page)
        self.upload_button = Button(self, text="Download student lists")

        self.label.place(x=200, y=40, width=160, height=25)
        self.list_button.place(x=215, y=120, width=120, height=25)
        self.list_button ["command"] = self.subjects_page
        self.download_button.place(x=215, y=150, width=120, height=25)
        self.upload_button.place(x=200, y=180, width=150, height=25)


    def subjects_page(self):

        self.clear_frame()

        self.label = Label(self, text="Subjects", font=self.title_font)
        self.back_button = Button(self, text="Back", command = self.select_action_page)

        subjects_araay = ["JOS" , "PT", "Logika"]

        for i in range(1,len(subjects_araay)+1):
            c = i
            self.c = Label(self, text= subjects_araay[i-1])
            self.c.grid(row=1*i, column=0)
            a =i*10
            b= i*10 + 1
            self.a = Button(self,text="Subject info", command = self.subject_info_page)
            self.a.grid(row=1*i, column=1)
            self.b = Button(self,text="Create record", command =self.select_event_page)
            self.b.grid(row=1*i, column=2)

        self.label.place(x=200, y=0, width=160, height=25)
        self.back_button.place(x=200, y=120 + 30*(i+1), width=150, height=25)

    def subject_info_page(self):

        self.clear_frame()

        self.label = Label(self, text="Subject Info", font=self.title_font)
        self.label.grid(row=0, column=2)

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
        self.tree.grid(row=1, columnspan=3)

        self.back_button.place(x=220, y=300, width=150, height=25)


    def select_event_page(self):

        self.clear_frame()

        self.label = Label(self, text="SelectEvent", font=self.title_font)
        self.label_2 = Label(self, text="22.10.2017")
        self.label_3 = Label(self, text="15:00")
        self.label_4 = Label(self, text="Class 01")

        self.button_1 = Button(self, text="Select", command = self.agree_page)

        self.back_button = Button(self, text="Back", command = self.subjects_page)


        self.label.grid(row=0, columnspan=4)
        self.label_2.grid(row=1, column=0)
        self.label_3.grid(row=1, column=1)

        self.label_4.grid(row=1, column=2)

        self.button_1.grid(row=1, column=3)

        self.back_button.place(x=220, y=300, width=150, height=25)



    def agree_page(self):
        self.clear_frame()


        self.label = Label(self, text="Predmet datum cas ", font=self.title_font)
        self.button = Button(self, text="Agree", command = self.isic_page)
        self.button_2 = Button(self, text="Disagree",command =self.select_event_page)

        self.label.grid(row=0, columnspan=3)
        self.button.grid(row=1, column=0)
        self.button_2.grid(row=1, column=1)


    def isic_page(self):
        self.clear_frame()

        label = Label(self, text="Prilozte isic", font=self.title_font)
        button = Button(self, text="Close and save", command=self.select_action_page)

        label.grid(row=0)
        button.grid(row=1)

    def upload_page(self):
        self.clear_frame()

        self.label = Label(self, text="Do you want upload records? ", font=self.title_font)
        self.button = Button(self, text="Yes",command = self.select_action_page)
        self.button_2 = Button(self, text="No", command =self.select_action_page)
        self.back_button = Button(self, text="Back", command = self.select_action_page)

        self.label.place(x=150, y=0, width=350, height=25)
        self.button.place(x=215, y=150, width=80, height=25)
        self.button_2.place(x=295, y=150, width=80, height=25)
        self.back_button.place(x=220, y=190, width=150, height=25)



app = Application()

app.mainloop()