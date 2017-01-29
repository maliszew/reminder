#!/usr/bin/python
# https://github.com/maliszew/reminder
import sys

helptext = "Reminder 1.1 by maliszew\n\nUsage:\nAdd tasks typing their name and time interval (in seconds - in future version also in minutes). App will popup a message about this task every n second.\nYou can delete tasks - popup will not appear anymore.\n\nThis app needs tkinter library to work. Installation guide on Windows, Linux and MacOS: http://www.tkdocs.com/tutorial/install.html"

if ("-h" in sys.argv) or ("--help" in sys.argv):
    print(helptext)
    exit()

from tkinter import *  # http://www.tkdocs.com/index.html
from tkinter import ttk
import time
from threading import Thread
import threading

# exit = False
exit_flag = threading.Event()
task_flag = threading.Event()


def settime(s):
    while not exit_flag.wait(timeout=s):
        currenttime.configure(text=time.strftime("%H:%M:%S"))


def clickabout():
    newwindow = Toplevel()
    newwindow.focus()
    info = Label(newwindow, text=helptext)
    info.grid(column=0, row=0)
    closebutton = Button(newwindow, text="Close", command=newwindow.destroy)
    closebutton.grid(column=0, row=1)


def addtask(*args):
    task = name.get()
    int = interval.get()

    newtask = Thread(target=reminder, daemon=True, args=(task_flag, task, int))
    newtask.start()
    id = newtask.ident

    tup = (task, int, id)
    tasklist.insert(END, tup)
    testinput.set(task + int)


# for i, task in enumerate(tasklist.get(0,END)):
# print(i, task, "id:", task[2])

# for i in tasklist:
# print(tasklist.get(0,END))

def checkthreadstatus(id):
    for i, task in enumerate(tasklist.get(0, END)):
        if task[2] == id:
            return True
    return False


def reminder(flag, name, interval):
    curthread = threading.currentThread().ident
    # print("thread nr", curthread)

    curtask = checkthreadstatus(curthread)
    # print("task", curtask)

    while (not flag.wait(timeout=int(interval))) and checkthreadstatus(threading.currentThread().ident):
        try:
            notify.destroy()
        except (NameError, AttributeError):
            pass
        notify = Toplevel()
        notify.focus()
        info = Label(notify, text=name)
        info.grid(column=0, row=0)
        closebutton = Button(notify, text="Close", command=notify.destroy)
        closebutton.grid(column=0, row=1)
        # print(name, " ", threading.currentThread())


def deletetask(*args):
    todelete = tasklist.curselection()
    # print(todelete)
    j = 0
    for i in todelete:
        # print("usuwam ", i)
        curtask = tasklist.get(i)

        tasklist.delete(i - j)
        j += 1


        # tup_temp = (curtask[0], curtask[1], curtask[2], False)
        # tasklist.insert(END, tup_temp)


main = Tk()
main.title("Task Reminder")

mainframe = ttk.Frame(main)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

header = Label(main, text="Reminder 1.1 by maliszew")
header.grid(column=0, row=0)
currenttime = Label(main, text=time.strftime("%H:%M:%S"))
currenttime.grid(column=2, row=0)

systemclock = Thread(target=settime, args=(1,))
systemclock.start()

tasklist = Listbox(main, selectmode=EXTENDED)  # to be replaced by Ttk/Tkinker Treeview!!
tasklist.grid(column=0, row=1)

test = Label(main, text="")
test.grid(column=1, row=3)

namelabel = Label(main, text="Task name")
namelabel.grid(column=0, row=2)
intlabel = Label(main, text="Reminder interval in seconds")
intlabel.grid(column=1, row=2)

name = StringVar()
interval = StringVar()

taskname = Entry(main, textvariable=name)
taskname.grid(column=0, row=3)
taskinterval = Entry(main, textvariable=interval)
taskinterval.grid(column=1, row=3)

testinput = StringVar()
test.configure(textvariable=testinput)

addtaskbutton = Button(main, text="Add task", command=addtask)
addtaskbutton.grid(column=2, row=3)
deletetaskbutton = Button(main, text="Delete selected task", command=deletetask)
deletetaskbutton.grid(column=3, row=3)

# for i in range(7):
#	tup = ("test!", i)
#	tasklist.insert(END, tup)

# taskname.focus()
taskname.bind('<Return>', addtask)
# taskinterval.focus()
taskinterval.bind('<Return>', addtask)

aboutbutton = Button(main, text="About Reminder", command=clickabout)
aboutbutton.grid(column=1, row=0)

main.mainloop()
exit_flag.set()
task_flag.set()