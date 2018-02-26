#! python  
#
# dispatcher.py
#
# Code written for CS471 Semester Project to display knowledge of priority queue and dispatcher
#
# Written by Matthew Stevenson
# 
# Email: mstev019@odu.edu


from Tkinter import *
from ttk import *
import time
import numpy
import tkMessageBox

# initial time value at program start
timeProg = time.time()

# global pid counter
pid = 0
priority = 0
# class process to store process object
class process:

	def __init__(self, pid, arrival, priority, status):
		self.pid = pid
		self.arrival = arrival
		self.priority = priority
		self.status = status

# context switch	
def run_process():
	i = 0
	j = 0
	save = []
	while i < waitArray.__len__():
		if waitArray[i].status == "ready":
			save.append(i)
			j += 1
		i += 1
	target = save[0]
	mess =  "PID " + str(runArray[0].pid) + " moved to ready! \nPID " + str(waitArray[target].pid) + " running!"
	mbox = tkMessageBox.showinfo("Context Switch", mess)
	runArray[0].status = "ready"
	runArray.append(waitArray.pop(save[0]))
	waitArray.append(runArray.pop(0))
	runArray[0].status = "running"
	map(treeWait.delete, treeWait.get_children())
	map(treeRunning.delete, treeRunning.get_children())
	sort_ready()
	treeRunning.insert("" , 0, values=(runArray[0].pid,runArray[0].arrival,runArray[0].priority,runArray[0].status))

# prioritize ready queue
def sort_ready():
	waitArray.sort(key=lambda x: x.priority, reverse=False)
	i = 0
	while i < waitArray.__len__():
		treeWait.insert("" , i , values=(waitArray[i].pid,waitArray[i].arrival,waitArray[i].priority,waitArray[i].status))
		i += 1

# create new process
def create_process():
	global timeProg, pid
	priority = int(newpriority.get())
	arrival = round((time.time() - timeProg))
	pid +=1
	newprocess = process(pid, arrival, priority, "ready")
	waitArray.append(newprocess)
	map(treeWait.delete, treeWait.get_children())
	sort_ready()
	i = 0
	j = 0
	save = []
	while i < waitArray.__len__():
		if waitArray[i].status == "ready":
			save.append(i)
			j += 1
		i += 1
	target = save[0]
	if numpy.greater_equal(runArray[0].priority,newprocess.priority) == True & numpy.greater_equal(waitArray[target].priority,newprocess.priority) == True:
		check_priority()

# preemptive call to compare priority of running pid with top of the ready queue
def check_priority():
	if numpy.greater_equal(runArray[0].priority,waitArray[0].priority) == True:
		run_process()

# initialize dispatcher with initial queues
def first_create_process():
	sort_ready()
	treeRunning.insert("" , 0, values=(runArray[0].pid,runArray[0].arrival,runArray[0].priority,runArray[0].status))

# force run process from waiting by click on item
def select_item_wait(self):
	rowitem = treeWait.item(treeWait.selection())
	target = rowitem.values()[2][0]
	i = 0
	while target != waitArray[i].pid:
		i += 1
	if rowitem.values()[2][3] == "ready":
		mess =  "PID " + str(runArray[0].pid) + " moved to waiting! \nPID " + str(waitArray[i].pid) + " running!"
		mbox = tkMessageBox.showinfo("Context Switch", mess)
		runArray[0].status = "waiting"
		runArray.append(waitArray.pop(i))
		waitArray.append(runArray.pop(0))
		runArray[0].status = "running"
		map(treeWait.delete, treeWait.get_children())
		map(treeRunning.delete, treeRunning.get_children())
		sort_ready()
		treeRunning.insert("" , 0, values=(runArray[0].pid,runArray[0].arrival,runArray[0].priority,runArray[0].status))
	else:
		mess =  "PID " + str(waitArray[i].pid) + " moved from waiting to ready!"
		mbox = tkMessageBox.showinfo("Context Switch", mess)
		waitArray[i].status = "ready"
		map(treeWait.delete, treeWait.get_children())
		sort_ready()

# force kill process from running by click on item
def select_item_running(self):
	run_process()  

# main loop for event listeners
root = Tk();
newpriority = StringVar()
root.title("CS471 Project - Fall 2017 - Matthew Stevenson")
root.minsize(width=500, height=620)
root.maxsize(width=500, height=620)
root.configure(background='grey')
progLabel = Label(root,text="Simple dispatcher to demonstrate priority queue").pack()
prog1Label = Label(root,text="*Click on row items to kill/run them*").pack()

# initialize starting contraints for starting processes
if pid == 0:
	pid += 1
	test1 = process(pid,0,5,'running')
	pid += 1
	test2 = process(pid,0,7,'ready')
	pid += 1
	test3 = process(pid,0,8,'ready')

	runArray = []
	runArray.append(test1)
	runArray.sort(key=lambda x: x.priority, reverse=False)
	waitArray = []
	waitArray.append(test2)
	waitArray.append(test3)
	waitArray.sort(key=lambda x: x.priority, reverse=False)

# create running table
runLabel = Label(root,text="Running Process:").pack()
treeRunning = Treeview(root)
treeRunning["show"] = ["headings"]
treeRunning["columns"]=("pid","arrival","priority","status")
treeRunning.column("pid", width=100)
treeRunning.column("arrival", width=100)
treeRunning.column("priority", width=100)
treeRunning.column("status",width=100)
treeRunning.heading("pid", text="pid")
treeRunning.heading("arrival", text="arrival")
treeRunning.heading("priority", text="priority")
treeRunning.heading("status", text="status")
treeRunning.pack()

# create waiting table
waitLabel = Label(root,text="Ready/Waiting Processes:").pack()
treeWait = Treeview(root)
treeWait["show"] = ["headings"]
treeWait["columns"]=("pid","arrival","priority","status")
treeWait.column("pid", width=100)
treeWait.column("arrival", width=100)
treeWait.column("priority", width=100)
treeWait.column("status",width=100)
treeWait.heading("pid", text="pid")
treeWait.heading("arrival", text="arrival")
treeWait.heading("priority", text="priority")
treeWait.heading("status", text="status")
treeWait.pack()

# initialize dispatcher
first_create_process()

# click on item event
treeWait.bind('<ButtonRelease-1>', select_item_wait)
treeRunning.bind('<ButtonRelease-1>', select_item_running)

# create process function
createLabel = Label(root,text="Create Process").pack()
newProc = Label(root,text="Priority:").pack()
createProc = Entry(root,width=5,textvariable=newpriority).pack()
createButt = Button(root,text="Create",command=create_process).pack()

root.mainloop()
