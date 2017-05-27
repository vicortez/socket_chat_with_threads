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

# while True:
#     connect, addr = server_socket.accept()
#     print("Connection Address:" + str(addr))
#
#     str_return = "Welcome to visit my test socket server. Waiting for command."
#     connect.sendto(bytes(str_return, 'utf-8'), addr)
#
#     str_recv, temp = connect.recvfrom(1024)
#     print(str_recv)
#
#     str_return = "I got your command, it is " + str(str_recv)
#     connect.sendto(bytes(str_return, 'utf-8'), addr)
#
#     connect.close()