from tkinter import *
from tkinter import font  as tkfont
from tkinter import ttk



class Application(Frame):
    #GUI Application

    def __init__(self, master):
        #Initialize the Frame
        Frame.__init__(self,master)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.pack()
        self.login_page()

    def login_page(self):

        self.label = Label(self, text="Login" ,font=self.title_font)

        self.label_2 = Label(self, text="Username")
        self.label_3 = Label(self, text="Password")

        self.entry_1 = Entry(self)
        self.entry_2 = Entry(self, show="*")

        self.checkbox = Checkbutton(self, text="Keep me logged in")
        self.logbtn = Button(self, text="Login", command = self.select_action_page )

        self.label.grid(row=0, columnspan=2)
        self.label_2.grid(row=1, column=0)
        self.label_3.grid(row=2, column=0)

        self.entry_1.grid(row=1, column=1)
        self.entry_2.grid(row=2, column=1)
        self.checkbox.grid(row=3, columnspan=2)
        self.logbtn.grid(row=4, columnspan=2)

    def clear_frame(self):
        # clear frame
        for child in self.winfo_children():
            child.destroy()


    def select_action_page(self):

        self.clear_frame()

        self.label = Label(self, text="Select Action",font=self.title_font)

        self.list_button = Button(self, text="Subjects")
        self.download_button = Button(self, text='Upload records',command = self.upload_page)
        self.upload_button = Button(self, text="Download student lists")

        self.label.grid(row=0, columnspan=3)
        self.list_button.grid(row=1, column=0)
        self.list_button ["command"] = self.subjects_page
        self.download_button.grid(row=1, column=1)
        self.upload_button.grid(row=1, column=2)

    def subjects_page(self):

        self.clear_frame()

        self.label = Label(self, text="Subjects", font=self.title_font)
        self.label.grid(row=0, columnspan=3)

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

    def subject_info_page(self):

        self.clear_frame()

        self.label = Label(self, text="Subject Info", font=self.title_font)
        self.label.grid(row=0, column=1)

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

    def select_event_page(self):

        self.clear_frame()

        self.label = Label(self, text="SelectEvent", font=self.title_font)
        self.label_2 = Label(self, text="22.10.2017")
        self.label_3 = Label(self, text="15:00")
        self.label_4 = Label(self, text="Class 01")

        self.button_1 = Button(self, text="Select", command = self.agree_page)

        self.label.grid(row=0, columnspan=4)
        self.label_2.grid(row=1, column=0)
        self.label_3.grid(row=1, column=1)

        self.label_4.grid(row=1, column=2)

        self.button_1.grid(row=1, column=3)

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

        self.label.grid(row=0, columnspan=3)
        self.button.grid(row=1, column=0)
        self.button_2.grid(row=1, column=1)


root = Tk()
root.title("Welcome")
root.geometry('700x500')
app = Application(root)

root.mainloop()