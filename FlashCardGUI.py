import tkinter as tk
from tkinter import messagebox as ms
import os
import glob
import random
from FlashCard import FlashCard


class Application(tk.Frame):
    path = "FlashCards\\"
    files = []
    topics = []
    flashCards = []

    if(not os.path.isdir(path)):
        try:
            os.mkdir(path)
        except OSError:
            print("Failed to create folder")

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        self.setup()
        self.menu()
        self.header = tk.StringVar()
        self.info1 = tk.StringVar()
        self.info2 = tk.StringVar()
        self.info3 = tk.StringVar()
        self.info4 = tk.StringVar()
        self.info5 = tk.StringVar()
        self.info6 = tk.StringVar()

    def setup(self):
        self.master.title("FlashCard")
        self.master.iconbitmap("marisa.ico")
        self.master.maxsize(640,480)
        self.master.minsize(640,480)
        w = 640
        h = 480
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.openTopic = tk.Button(self.master, text = "Open Topic", command = self.openTopicMenu)
        self.openTopic.pack()
        self.openTopic.place(bordermode = "outside", height = "50", width = "200", x = "90", y = "200")

        self.makeTopic = tk.Button(self.master, text = "Create/Delete Topic", command = self.makeTopicMenu)
        self.makeTopic.pack()
        self.makeTopic.place(bordermode = "outside", height = "50", width = "200", x = "350", y = "200")

    def openTopicMenu(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.topics.clear()
        for folder in glob.glob(os.path.join(self.path, "*\\")):
            self.topics.append(folder.split("\\"))

        self.topFrame = tk.Frame(self.master)
        self.topFrame.pack(side = "top")

        self.scrollbar = tk.Scrollbar(self.topFrame)
        self.scrollbar.pack(side = "right", fill = "y")
        
        self.allExistingTopics = tk.Listbox(self.topFrame, selectmode = "single", yscrollcommand = self.scrollbar.set)
        for topic in self.topics:
            self.allExistingTopics.insert("end", topic[1])
        self.allExistingTopics.pack()
        self.scrollbar.config(command = self.allExistingTopics.yview)

        self.editTopic = tk.Button(self.master, text = "EDIT", command = self.editTargetTopic)
        self.editTopic.pack()
        self.editTopic.place()

        self.studyTopic = tk.Button(self.master, text = "STUDY", command = self.studyTargetTopic)
        self.studyTopic.pack()
        self.studyTopic.place()

        self.back = tk.Button(self.master, text = "BACK", command = self.menu)
        self.back.pack()
        self.back.place()

        self.i = 0

    def makeTopicMenu(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.topics.clear()

        for folder in glob.glob(os.path.join(self.path, "*\\")):
            self.topics.append(folder.split("\\"))

        self.topFrame = tk.Frame(self.master)
        self.topFrame.pack(side = "top")

        self.scrollbar = tk.Scrollbar(self.topFrame)
        self.scrollbar.pack(side = "right", fill = "y")
        
        self.allExistingTopics = tk.Listbox(self.topFrame, selectmode = "single", yscrollcommand = self.scrollbar.set)
        for topic in self.topics:
            self.allExistingTopics.insert("end", topic[1])

        self.allExistingTopics.pack()
        self.scrollbar.config(command = self.allExistingTopics.yview)
        
        self.deleteTopic = tk.Button(self.master, text = "DELETE", command = self.deleteExistingTopic)
        self.deleteTopic.pack()
        self.deleteTopic.place(bordermode = "outside", x = "400", y = "50")

        self.newTopic = tk.Entry()
        self.newTopic.pack()
        self.newTopic.place()

        self.create = tk.Button(self.master, text = "CREATE", command = self.createNewTopic)
        self.create.pack()
        self.create.place()

        self.back = tk.Button(self.master, text = "BACK", command = self.menu)
        self.back.pack()
        self.back.place()

    def createNewTopic(self):
        if(len(self.newTopic.get()) > 0):
            self.dirPath = self.path + self.newTopic.get() + "\\"

            if(not os.path.isdir(self.dirPath)):
                try:
                    os.mkdir(self.dirPath)
                    self.makeTopicMenu()
                except OSError:
                    print("Failed to create folder")
            else:
                ms.showinfo("", "\"" + self.newTopic.get() + "\" already exists")

    def deleteExistingTopic(self):
        index = self.allExistingTopics.curselection()
        if not index:
            return
        else:
            try:
                self.dirPath = self.path + self.allExistingTopics.get(index) + "\\"
                for filename in glob.glob(os.path.join(self.dirPath, "*")):
                    os.remove(filename)
                os.rmdir(self.dirPath)
                self.makeTopicMenu()
            except OSError:
                print("Failed to delete folder")

    def editTargetTopic(self):
        index = self.allExistingTopics.curselection()
        if not index:
            return
        else:
            self.dirPath = self.path + self.allExistingTopics.get(index) + "\\"
            
            self.topicInfo()

    def topicInfo(self):
        self.flashCards.clear()
        self.files.clear()
        #all files within a folder
        for filename in glob.glob(os.path.join(self.dirPath, "*")):
            self.files.append(filename)
            with open(os.path.join(os.getcwd(), filename), "r") as f:
                data = f.read().split("\n")
                if(len(data) > 1):
                    x = FlashCard(data[0], data[1])
                    self.flashCards.append(x)

        for widget in self.master.winfo_children():
                widget.destroy()

        self.title = tk.Label(self.master, textvariable = self.header)
        self.header.set(self.dirPath.split("\\")[1])
        self.title.pack()

        self.newName = tk.Entry()
        self.newName.pack()
        self.newName.place()

        self.rename = tk.Button(self.master, text = "RENAME", command = self.renameTopic)
        self.rename.pack()
        self.rename.place()

        if(len(self.flashCards) > 0):
            self.qHeader = tk.Label(self.master, textvariable = self.info1)
            self.info1.set("Question:")
            self.qHeader.pack()

            self.question = tk.Label(self.master, textvariable = self.info2)
            self.info2.set(self.flashCards[self.i].question)
            self.question.pack()

            self.aHeader = tk.Label(self.master, textvariable = self.info3)
            self.info3.set("Answer:")
            self.aHeader.pack()

            self.answer = tk.Label(self.master, textvariable = self.info4)
            self.info4.set(self.flashCards[self.i].answer)
            self.answer.pack()

            self.editFlashCard = tk.Button(self.master, text = "EDIT FLASH CARD", command = self.editFlashCardInfo)
            self.editFlashCard.pack()
            self.editFlashCard.place()

            self.deleteFlashCard = tk.Button(self.master, text = "DELETE FLASH CARD", command = self.deleteFlashCardInfo)
            self.deleteFlashCard.pack()
            self.deleteFlashCard.place()
            if(len(self.flashCards) > 1):
                self.right = tk.Button(self.master, text = "RIGHT", command = self.moveIndexRight)
                self.right.pack()
                self.right.place()

                self.left = tk.Button(self.master, text = "LEFT", command  = self.moveIndexLeft)
                self.left.pack()
                self.left.place()

        self.addFlashCard = tk.Button(self.master, text = "ADD FLASH CARD", command = self.addFlashCardInfo)
        self.addFlashCard.pack()
        self.addFlashCard.place()
            
        self.back = tk.Button(self.master, text = "BACK", command = self.openTopicMenu)
        self.back.pack()
        self.back.place()

    def renameTopic(self):
        if(len(self.newName.get()) > 0):
            os.rename(self.dirPath, self.path + self.newName.get() + "\\")
            self.dirPath = self.path + self.newName.get() + "\\"
            self.topicInfo()    

    def editFlashCardInfo(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.questionTitle = tk.Label(self.master, textvariable = self.info1)
        self.info1.set("Current Question:")
        self.questionTitle.pack()

        self.question = tk.Label(self.master, textvariable = self.info2)
        self.info2.set(self.flashCards[self.i].question)
        self.question.pack()

        self.answerTitle = tk.Label(self.master, textvariable = self.info3)
        self.info3.set("Current Answer:")
        self.answerTitle.pack()

        self.answer = tk.Label(self.master, textvariable = self.info4)
        self.info4.set(self.flashCards[self.i].answer)
        self.answer.pack()

        self.rqTitle = tk.Label(self.master, textvariable = self.info5)
        self.info5.set("New Question:")
        self.rqTitle.pack()
        
        self.replaceQuestion = tk.Entry()
        self.replaceQuestion.pack()
        self.replaceQuestion.place()

        self.raTitle = tk.Label(self.master, textvariable = self.info6)
        self.info6.set("New Answer:")
        self.raTitle.pack()

        self.replaceAnswer = tk.Entry()
        self.replaceAnswer.pack()
        self.replaceAnswer.place()

        self.editFlashCard = tk.Button(self.master, text = "EDIT", command = self.editFile)
        self.editFlashCard.pack()
        self.editFlashCard.place()

        self.back = tk.Button(self.master, text = "BACK", command = self.topicInfo)
        self.back.pack()
        self.back.place()

    def editFile(self):
        self.files[self.i]
        q = self.flashCards[self.i].question
        a = self.flashCards[self.i].answer
        f = open(self.files[self.i], "w")
        if len(self.replaceQuestion.get()) > 0:
            self.flashCards[self.i].question = self.replaceQuestion.get()
            q = self.replaceQuestion.get()
        if len(self.replaceAnswer.get()) > 0:
            self.flashCards[self.i].answer = self.replaceAnswer.get()
            a = self.replaceAnswer.get()
        
        f.write(q + "\n" + a)
        f.close()
        self.editFlashCardInfo()

    def deleteFlashCardInfo(self):
        os.remove(self.files[self.i])
        self.i -= 1
        if(self.i < 0):
            self.i = 0
        self.topicInfo()

    def addFlashCardInfo(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.questionTitle = tk.Label(self.master, textvariable = self.info1)
        self.info1.set("Question:")
        self.questionTitle.pack()

        self.newQuestion = tk.Entry()
        self.newQuestion.pack()
        self.newQuestion.place()

        self.answerTitle = tk.Label(self.master, textvariable = self.info2)
        self.info2.set("Answer:")
        self.answerTitle.pack()

        self.newAnswer = tk.Entry()
        self.newAnswer.pack()
        self.newAnswer.place()
        
        self.addFlashCard = tk.Button(self.master, text = "ADD", command = self.addFile)
        self.addFlashCard.pack()
        self.addFlashCard.place()

        self.back = tk.Button(self.master, text = "BACK", command = self.topicInfo)
        self.back.pack()
        self.back.place()

    def addFile(self):
        if(len(self.newQuestion.get()) > 0) and (len(self.newAnswer.get()) > 0):
            pathSplit = ""
            j = 0
            if not self.files:
                pathSplit = self.dirPath.split("\\")
                j = 1
            else:
                pathSplit = self.files[len(self.files) - 1].split("\\")
                j = int(pathSplit[2]) + 1

            x = open(pathSplit[0] + "\\" + pathSplit[1] + "\\" + str(j), "x")
            x.close()
            x = open(pathSplit[0] + "\\" + pathSplit[1] + "\\" + str(j), "a")
            x.write(self.newQuestion.get() + "\n" + self.newAnswer.get())
            x.close()
            self.files.append(pathSplit[0] + "\\" + pathSplit[1] + "\\" + str(j))
            self.addFlashCardInfo()
            ms.showinfo("", "FlashCard Added")
    
    def moveIndexRight(self):
        self.i += 1
        if self.i > len(self.flashCards) - 1:
            self.i = 0
        
        self.topicInfo()

    def moveIndexLeft(self):
        self.i -= 1
        if(self.i < 0):
            self.i = len(self.flashCards) - 1
        
        self.topicInfo()

    def studyTargetTopic(self):
        index = self.allExistingTopics.curselection()
        if not index:
            return
        else:
            self.dirPath = self.path + self.allExistingTopics.get(index) + "\\"

            self.flashCards.clear()
            for filename in glob.glob(os.path.join(self.dirPath,"*")):
                with open(os.path.join(os.getcwd(), filename), "r") as f:
                    data = f.read().split("\n")
                    if(len(data)>1):
                        x = FlashCard(data[0], data[1])
                        self.flashCards.append(x)
            
            if(len(self.flashCards) > 0):
                self.flashCardInfo()
            else:
                ms.showinfo("", "\"" + self.allExistingTopics.get(index) + "\" is empty")

    def flashCardInfo(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.randomFlash = random.sample(self.flashCards, len(self.flashCards))
        self.i = 0

        self.flashCardFrame = tk.Frame(self.master)
        self.flashCardFrame.pack(side = "top")

        self.title = tk.Label(self.flashCardFrame, textvariable = self.header)
        self.header.set("Question:")
        self.title.pack()

        self.question_answer = tk.Label(self.flashCardFrame, textvariable = self.info1)
        self.info1.set(self.randomFlash[self.i].question)
        self.question_answer.pack()

        self.check_flip = True
        self.swap = tk.Button(self.master, text = "FLIP", command = self.swapInfo)
        self.swap.pack()
        self.swap.place()

        self.next = tk.Button(self.flashCardFrame, text = "NEXT", command = self.nextInfo)
        self.next.pack()
        self.next.place()

        self.back = tk.Button(self.master, text = "BACK", command = self.openTopicMenu)
        self.back.pack()
        self.back.place()

    def swapInfo(self):
        self.check_flip = not self.check_flip
        if self.check_flip:
            self.header.set("Question:")
            self.info1.set(self.randomFlash[self.i].question)
        else:
            self.header.set("Answer:")
            self.info1.set(self.randomFlash[self.i].answer)


    def nextInfo(self):
        self.i += 1
        if(self.i < len(self.randomFlash)):
            self.check_flip = True
            self.header.set("Question:")
            self.info1.set(self.randomFlash[self.i].question)
        else:
            for widget in self.master.winfo_children():
                widget.destroy()

            self.reset = tk.Button(self.master, text = "AGAIN", command = self.flashCardInfo)
            self.reset.pack()
            self.reset.place()

            self.back = tk.Button(self.master, text = "BACK", command = self.openTopicMenu)
            self.back.pack()
            self.back.place()


window = tk.Tk()
app = Application(window)
app.mainloop()