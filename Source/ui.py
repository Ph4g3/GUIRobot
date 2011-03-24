import os.path
from subprocess import Popen

from Tix import *
from tkFileDialog import askopenfilename, asksaveasfile

class App():

    def __init__(self, master):

        self.tabs = NoteBook(master)
        self.tabs.add('scripts', label='Scripts')
        scriptsTab = ScriptsTab(self.tabs.scripts)
        self.tabs.add('apps', label='Applications')
        self.tabs.grid(row=0, column=0, columnspan=5, rowspan=5)

class ScriptsTab():
    
    def __init__(self, master):
        self.scriptControlFrame = Frame(master)
        self.scriptControlFrame.grid(row=0, column=0, columnspan=5, rowspan=5)
        
        self.usingText = Label(self.scriptControlFrame, text="Using:")
        self.usingText.grid(row=0, column=0, sticky=E)

        #This button will have additional dialog popup, with dynamic text
        self.using = Button(self.scriptControlFrame, text="Nothing!",
                            bg="red", command=self.openFile)
        self.using.grid(row=0, column=1, sticky=N+E+S+W)

        self.runButton = Button(self.scriptControlFrame, text="Run", bg="green",
                                command=self.run)
        self.runButton.grid(row=0, column=3, sticky=N+E+S+W)

        self.saveButton = Button(self.scriptControlFrame, text="Save", command=self.saveFile)
        self.saveButton.grid(row=0, column=4, sticky=N+E+S+W)

        self.saveAsButton = Button(self.scriptControlFrame, text="Save As", command=self.saveFileAs)
        self.saveAsButton.grid(row=0, column=5, sticky=N+E+S+W)

        self.textArea = Text(self.scriptControlFrame)
        self.scrollbar = Scrollbar(self.scriptControlFrame, command=self.textArea.yview)
        self.textArea.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=1, column=20, rowspan=20, sticky=N+S)
        self.textArea.grid(row=1, column=0, columnspan=20, rowspan=20, pady=3)

        #Put some help info into the textArea
        self.textArea.insert(0.0,
            """To start, you should select a file to use. Click the 'Nothing!' button.""")

    def run(self):
        if 'Virtual_HID' not in dir():
            from GUIRobot.Source import Virtual_HID
            mouse = Virtual_HID.VMouse()
            keyboard = Virtual_HID.VKeyboard()

        #Popen('python '+str(self.currentFile))
        with open(self.currentFile) as run:
            commands = run.readlines()
            for command in commands:
                exec(command)

    def openFile(self):
        try:
            #Open file dialog
            inFile = askopenfilename()

            #Store the file in a list of lines
            #Set button text and hold the file name
            with open(inFile, 'r') as f:
                self.setUsing(inFile)
                self.currentFile = inFile
                lines = f.readlines()

            #Remove all text from textArea
            #Will probably want to check for save on change here
            self.removeText()

            #Reverse so we can push to textarea - stack like
            lines.reverse()
            for line in lines:
                self.textArea.insert(0.0, line)

            #Stop annoying the user and set the Using button white
            self.using.config(bg='white')
        except IOError:
            #If user doesn't choose a file an IOError will be thrown.
            #We can ignore this safely.
            pass

    def saveFile(self):
        linesToWrite = self.getTextAreaText()
        
        try:
            #Skip the check for 'same file' for now
            #with open(self.currentFile, 'r') as read:
            #    linesWritten = read.readlines()

            with open(self.currentFile, 'w') as write:
                write.writelines(linesToWrite)
        except AttributeError:
            #If an AttributeError is thrown it means our
            #current file has not been set. Proceed to the saveFileAs
            #method
            self.saveFileAs()

    def saveFileAs(self):
        with asksaveasfile() as write:
            text = self.getTextAreaText()
            write.writelines(text)
            self.setUsing(write.name)

    def setUsing(self, _file):
        if os.path.isabs(_file):
            _file = os.path.split(_file)[-1]
        self.using.config(text=_file)

    def stripTupleInfo(self, listOfTuples):
        i=0
        for line in listOfTuples:
            listOfTuples[i] = line[1]
            i+=1
        return listOfTuples

    def getTextAreaText(self):
        text = self.textArea.dump(0.0, END, text=True)
        text = self.stripTupleInfo(text)
        return text

    def removeText(self):
        self.textArea.delete(0.0, END)

def makeFileMenu(master):
    fileMenu = Menu(master)
    fileMenu.add_command(label="Save", command=None)
    fileMenu.add_command(label="Exit", command=quitApp, accelerator="Ctrl+Q")
    return fileMenu

def makeEditMenu(master):
    editMenu = Menu(master)
    editMenu.add_cascade(label="Filler", command=None)
    return editMenu


def quitApp():
    root.destroy()

if __name__ == '__main__':
    #Start tkinter instance
    root = Tk()

    #Create menu bar
    menu = Menu(root)

    #Create menu selections
    filemenu = makeFileMenu(menu)
    editmenu = makeEditMenu(menu)
    viewmenu = Menu(menu)
    helpmenu = Menu(menu)
    
    menu.add_cascade(label="File", menu=filemenu)
    menu.add_cascade(label="Edit", menu=editmenu)
    root.config(menu=menu)

    app = App(root)
    root.mainloop()
