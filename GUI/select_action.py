from tkinter import *
import tkinter.messagebox as tm
from PIL import Image, ImageTk


class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)


        list_img = Image.open('list_img.png')
        download_img = Image.open("download_img.png")
        upload_img = Image.open("upload_img.png")

        list_icon = ImageTk.PhotoImage(list_img)
        download_icon = ImageTk.PhotoImage(download_img)
        upload_icon = ImageTk.PhotoImage(upload_img)

        self.list_button = Button(self,height=10, width=20)

        self.download_button = Label(self ,height=10, width=20,text= 'sdknfsdlkjndsflkn')
        self.upload_button = Button(self,height=20, width=20)
       # self.download_button = Button(self, image= download_icon)
       # self.upload_button = Button(self, image= upload_icon)



        self.list_button.grid(row =1 ,column = 1)
        self.download_button.grid( row = 1,column = 2)
        self.upload_button.grid( row= 1,column = 3)

        self.pack()





root = Tk()
root.geometry("700x500")
lf = LoginFrame(root)
root.mainloop()