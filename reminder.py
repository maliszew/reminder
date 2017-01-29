#!/usr/bin/python
# https://github.com/maliszew/reminder
import sys

helptext = "Task Reminder 1.2 by maliszew\n\nUsage:\nAdd tasks typing their name and time interval (in seconds - in future version also in minutes). For example: \"Drink  some water!\" or \"Stand up and exercise!\" every 600 second.\nApp will popup a message about this task every n second. Perform the task and hit \"Done!\". Otherwise app will remind you again in n seconds, closing old window and creating a new one.\n\nYou can delete tasks - popup will not appear anymore.\n\nThis app needs tkinter library to work. Installation guide on Windows, Linux and MacOS: http://www.tkdocs.com/tutorial/install.html"

if ("-h" in sys.argv) or ("--help" in sys.argv):
    print(helptext)
    exit()

try:
    import tkinter as tk  # python 3.x
except:
    try:
        import Tkinter as tk  # python 2.7
    except:
        print(helptext)
        exit()
import time
import threading

try:
    import queue as qu  # python 3.x
except:
    import Queue as qu  # python 2.7

exit_flag = threading.Event()
task_flag = threading.Event()
global queue
queue = qu.Queue()
global windows
windows = []


def settime():
    while not exit_flag.wait(timeout=1):
        queue.put("clock")


def configuretime():
    currenttime.configure(text=time.strftime("%H:%M:%S"))


def clickabout():
    newwindow = tk.Toplevel()
    newwindow.focus()
    newwindow.grab_set()
    info = tk.Label(newwindow, text=helptext)
    info.grid(column=0, row=0)
    closebutton = tk.Button(newwindow, text="Close this window!", command=newwindow.destroy)
    closebutton.grid(column=0, row=1)


def adderror():
    newwindow = tk.Toplevel()
    newwindow.focus()
    newwindow.grab_set()
    info = tk.Label(newwindow,
                    text="To add a new task, provide both:\n\n1. Name of the task;\n2. Reminder interval in seconds (integer)")
    info.grid(column=0, row=0)
    closebutton = tk.Button(newwindow, text="Try one more time!", command=newwindow.destroy)
    closebutton.grid(column=0, row=1)


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def addtask(*args):
    task = name.get()
    int = interval.get()

    if not (task and int) or not (is_int(int)):
        adderror()
        return

    newtask = threading.Thread(target=reminder, args=(task_flag, task, int))
    newtask.daemon = True
    newtask.start()

    id = newtask.ident
    tup = (task, int, id)
    tasklist.insert(tk.END, tup)


# for i, task in enumerate(tasklist.get(0,tk.END)):
# print(i, task, "id:", task[2])

def checkqueue():
    # print("queue check.....")
    processqueue()
    main.after(100, checkqueue)


# for tup in windows:
# print ("windows", tup)

def processqueue():
    while queue.qsize():
        try:
            msg = queue.get(0)
            curthread = threading.currentThread().ident
        # print("processqueue thread nr", curthread)
        # print("queue: ", msg)
        except Queue.Empty:
            # main.after(100, processqueue)
            # print("queue empty!!")
            pass

        # print("============== CURRENT WINDOWS", windows)

        if msg[0] == "open":
            pid = msg[4]
            # print("open new for", msg)
            main.after(10, popup, msg)
        elif msg[0] == "close":
            pid = msg[1]
            # print("close for", msg)
            main.after(10, closewindow, pid)
        elif msg == "clock":
            main.after(0, configuretime)
            # else:
            # print("queue error!!", msg, msg[0], msg[1], msg[2])


def checkthreadstatus(id):
    for i, task in enumerate(tasklist.get(0, tk.END)):
        if task[2] == id:
            return True
    return False


def checkwindowstatus(id, name):
    for tup in windows:
        if tup[1] == id:
            # print ("okineko istnieje!", id, name)
            return True
    # print ("okineka nie ma, tworze!", id, name)
    return False


def reminder(flag, name, interval):
    # print("reminder start")
    curthread = threading.currentThread().ident
    # print("reminder thread nr", curthread)

    curtask = checkthreadstatus(curthread)
    # print("task", curtask)

    queueargs = ("open", flag, name, interval, curthread)

    while (not flag.wait(timeout=int(interval))) and checkthreadstatus(curthread):
        if checkwindowstatus(curthread, name):
            queue.put(("close", curthread))
        queue.put(queueargs)

    # print("reminder close")
    queue.put(("close", curthread))


def popup(tuple):
    flag = tuple[1]
    name = tuple[2]
    interval = tuple[3]
    pid = tuple[4]
    timenow = str(time.strftime("%H:%M:%S"))

    curthread = threading.currentThread().ident
    # print("popup thread nr", curthread, "name", name, "pid", pid)

    notify = tk.Toplevel()
    windows.append((notify, pid, timenow))
    # print("popup while", "name", name)
    notify.focus()
    notify.lift()
    notify.attributes('-topmost', 1)
    notify.attributes('-topmost', 0)

    info = tk.Label(notify, text=name, font="-size 20")
    info.grid(column=0, row=0, sticky=(tk.W, tk.N))
    clock = tk.Label(notify, text=timenow)
    clock.grid(column=1, row=0, sticky=(tk.E, tk.N))
    closebutton = tk.Button(notify, width=40, height=3, text="Done!", font="-size 15",
                            command=lambda: queue.put(("close", pid, "Close it!")))
    closebutton.grid(column=0, row=1, columnspan=2, sticky=(tk.E, tk.W))


def deletetask(*args):
    todelete = tasklist.curselection()
    # print(todelete)
    j = 0
    for i in todelete:
        # print("usuwam ", i)
        curtask = tasklist.get(i)
        tasklist.delete(i - j)
        j += 1


def closewindow(pid):
    global windows
    # print("usuwam okienko pida", pid)
    # print("before close", windows)
    w_copy = [x for x in windows]
    for tup in w_copy:
        if tup[1] == pid:
            tup[0].destroy()
            # print("okienko papa pid", pid)
            windows[:] = [tup for tup in windows if not tup[1] == pid]
            # print("after close", windows)


def kill():
    mainframe.destroy()
    main.destroy()


main = tk.Tk()
main.title("Task Reminder 1.2 by maliszew")
main.columnconfigure(0, weight=1)
main.rowconfigure(0, weight=1)

mainframe = tk.Frame(main, padx=5, pady=5)
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=2)
mainframe.rowconfigure(0, weight=2)
mainframe.rowconfigure(1, weight=2)

header = tk.Label(mainframe, text="Type task name and reminder\ninterval in seconds.")
header.grid(column=0, row=9, rowspan=2)
currenttime = tk.Label(mainframe, text=time.strftime("%H:%M:%S"))
currenttime.grid(column=3, row=10)

systemclock = threading.Thread(target=settime)
systemclock.daemon = True
systemclock.start()

tasklist = tk.Listbox(mainframe, selectmode=tk.EXTENDED, width=50,
                      height=12)  # to be replaced by Ttk/Tkinker Treeview!!
tasklist.grid(column=0, row=0, columnspan=2, rowspan=9)
scroll = tk.Scrollbar(mainframe, command=tasklist.yview, orient=tk.VERTICAL)
scroll.grid(column=2, row=0, sticky=(tk.N, tk.S), rowspan=9)
tasklist.config(yscrollcommand=scroll.set)
tasklist.columnconfigure(0, weight=1)
tasklist.rowconfigure(0, weight=1)

namelabel = tk.Label(mainframe, text="Name", width=15)
namelabel.grid(column=3, row=2, sticky=(tk.W, tk.E))
intlabel = tk.Label(mainframe, text="Interval", width=15)
intlabel.grid(column=3, row=4, sticky=(tk.W, tk.E))

name = tk.StringVar()
interval = tk.StringVar()

taskname = tk.Entry(mainframe, textvariable=name, width=15)
taskname.grid(column=3, row=3, sticky=(tk.W, tk.E))
taskinterval = tk.Entry(mainframe, textvariable=interval, width=15)
taskinterval.grid(column=3, row=5, sticky=(tk.W, tk.E))

addtaskbutton = tk.Button(mainframe, text="Add", command=addtask, width=15)
addtaskbutton.grid(column=3, row=7, sticky=(tk.W, tk.E))
deletetaskbutton = tk.Button(mainframe, text="Delete", command=deletetask, width=15)
deletetaskbutton.grid(column=3, row=8, sticky=(tk.W, tk.E))

# taskname.focus()
taskname.bind('<Return>', addtask)
# taskinterval.focus()
taskinterval.bind('<Return>', addtask)

aboutbutton = tk.Button(mainframe, text="About", command=clickabout, width=15)
aboutbutton.grid(column=3, row=1, sticky=(tk.N, tk.W, tk.E))

closebutton = tk.Button(mainframe, text="Close", command=kill, width=15)
closebutton.grid(column=3, row=0, sticky=(tk.N, tk.W, tk.E))

checkqueue()
main.mainloop()
exit_flag.set()
task_flag.set()
