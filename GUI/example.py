class Test():
    def __init__(self,root):
        self.root = root
        self.root.columnconfigure(0, weight=1)
        self.root.config(bg='green')
        self.message = 'test message'

        self.contentFrame = Frame(self.root)
        self.contentFrame.config(background='black',borderwidth=5,relief ='sunken')
        self.contentFrame.grid(row=0, column=0, sticky='news')
        self.contentFrame.columnconfigure(0, weight=1)

        self.topBar = Frame(self.contentFrame, border=2, relief=RAISED)
        self.topBar.grid(row=0, column=0, columnspan=23,sticky=W+E)
        self.topBar.config(background='blue')
        self.topBar.columnconfigure(0, weight=1)

        self.newGameButton = Button(self.topBar, text="New Game")
        self.newGameButton.grid(row=0, column=0)
        self.newGameButton.config(background='red')

        self.messageBox = Label(self.topBar, text=self.message, height=2)
        self.messageBox.grid(row=1, column=0, columnspan=1,sticky=W+E)
        self.messageBox.config(background='yellow')

Test(root)