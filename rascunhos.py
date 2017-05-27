from tkinter import *
import threading

def sendMessage():
    print("hi there")
    threading.Thread(name='window', target=window()).start()

def window():
    mainFrame = Tk()
    button = Button(mainFrame,text="send message",command=sendMessage)
    # button.place(relx=0.5,rely=0.5,anchor=CENTER)
    button.pack()
    # c = Canvas(mainFrame, width=720,height=400)
    # c.pack()
    # c.create_line(72,4,700,300)

    mainloop()

window()
