from tkinter import *

class MyApp:
    def __init__(self, parent):
        self.myParent = parent

        self.main_container = Frame(parent, bg="green")
        self.main_container.grid()

        self.top_frame = Frame(self.main_container)
        self.top_frame.grid()

        self.top_left = Frame(self.top_frame, bd=2)
        self.top_left.grid(row=0, column=0)

        self.top_right = Frame(self.top_frame, bd=2)
        self.top_right.grid(row=0, column=2)

        self.top_left_label = Label(self.top_left, bd=2, bg="red", text="Top Left", width=100, anchor=W)
        self.top_left_label.grid(row=0, column=0)

        self.top_right_label = Label(self.top_right, bd=2, bg="blue", text="Top Right", width=22, anchor=E)
        self.top_right_label.grid(row=0, column=0)

        self.bottom_frame = Frame(self.main_container, bg="yellow", bd=2)
        self.bottom_frame.grid(row=1, column=0)

        self.text_box = Text(self.bottom_frame, width=40, height=5)
        self.text_box.grid(row=0, column=0)

root = Tk()
root.title("Test UI")
myapp = MyApp(root)
root.mainloop()
