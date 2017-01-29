# simple recurring task reminder app

Python + Tkinter

### How to run

```
python reminder.py
```

### Requirements

Works (or at least should work) with both Python 2.x and 3.x - tested with 2.7.12 and 3.5.2. Although **more recommended is Python 3.x**, as it is more stable when speaking of threads.

Also you need **Tkinter** to run the GUI. Check installation guide: http://www.tkdocs.com/tutorial/install.html

Should work on any platform (Windows, Linux, MacOS), but has been tested only on the first one.

### What it does

Add recurring / routine tasks you want to be reminded about - e.g. "Drink some water!" or "Stand up and exercise a little bit!" or "Take your medicine!" or "Roll your eyes!" (no, seriously! Check this out: http://www.wikihow.com/Exercise-Your-Eyes)... You can imagine.

Each task will have its own thread, which will popup a message with a reminder.

### What it should do

Task interval also in minutes

Deamon functionality - start up with the system

Saving tasks

Task statistics, graphs etc.

Executable files

Better app architecture (instead of just one file)

Some tests...