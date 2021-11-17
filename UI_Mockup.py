#ECE 485 Soil Robot GUI Program
#Written by Katherine Farrelly, Matthew Kelly, Steven Moore, Jonathan Medju
#This program is the entire Laptop/GUI side of the Soil Weighing robot.
#It handles robot communications, displaying of data, and control of the robot.
#It also handles file output of the robot data.

#importing all the libraries. Of note are serial and tkinter.
import os
import sys
import tkinter as tk
from tkinter import ttk
import serial
import math
import random
import threading
import time
import datetime
from datetime import datetime
from serial.tools import list_ports

#This code initializes the serial communication with the arduino
#There are several phases to opening a serial port. I will describe each on their own line.
with serial.Serial() as robot: #this creates the serial object "robot" used in the rest of the app.

    #These are the X and Y positions for all 36 cups in the robot.
    #These arrays are dvided into separate X and Y arrays to take up less space.
    xposarray = [0, 1400, 2900]
    yposarray = [0, 1440, 2880, 4390, 5900, 7600, 8800, 10400, 12100, 13600, 15000, 16700]
    zposarray = [0, 0]
    wb = [45,55]
    wbc = ['red','blue','green']
    checkarray = [1,1,1,1,1]
    cuparray = [36,36,36,36,36]
    zeroarray = [0,0,0,0,0]
    tarearray = [0.0,0.0,0.0,0.0,0.0]
    alphavar = ['AA']
    zeroflags = [0,0,0,0,0]
    tareflags = [0,0,0,0,0]
    weightfloat = [50]
    disconnected = [True]
    commError = [False]

    try: #massive try block lets go
        configFile = open(r"./config.cfg", "r")
        tmps = 'x'
        while(tmps != ''):
            tmps = configFile.readline()
            iter = 0
            if('xposarray' in tmps):
                for z in tmps.split():
                    if z.isdigit():
                        xposarray[iter] = int(z)
                        iter += 1
                        if(iter >= len(xposarray)):
                            break
            if('yposarray' in tmps):
                for z in tmps.split():
                    if z.isdigit():
                        yposarray[iter] = int(z)
                        iter += 1
                        if(iter >= len(yposarray)):
                            break
            if('zposarray' in tmps):
                for z in tmps.split():
                    if z.isdigit():
                        zposarray[iter] = int(z)
                        iter += 1
                        if(iter >= len(zposarray)):
                            break
            if('weight bounds' in tmps):
                for z in tmps.split():
                    if z.isdigit():
                        wb[iter] = int(z)
                        iter += 1
                        if(iter >= len(wb)):
                            break
            if('weight bound colors' in tmps):
                for z in tmps.split():
                    if iter > 2:
                        wbc[iter] = int(z)
                        iter += 1
                        if(iter + 3 >= len(wbc)):
                            break
        configFile.close()
    except OSError:
        pass
    class Calibrate(tk.Toplevel):
        def __init__(self, master):
            super().__init__(master)
            self.master = master
            self.wm_title("Setup Parameters")
            self.geometry("1100x480")
            self.buttonfont = "Helvetica 24"

            self.loadcellflag = 0 #decides which load cells to read from. 0 reads all 5 load cells.
            self.weightvar = tk.StringVar()
            #all the variables for displaying the zero and tare values
            self.zeroloadcell1 = tk.StringVar()
            self.zeroloadcell2 = tk.StringVar()
            self.zeroloadcell3 = tk.StringVar()
            self.zeroloadcell4 = tk.StringVar()
            self.zeroloadcell5 = tk.StringVar()
            self.tareloadcell1 = tk.StringVar()
            self.tareloadcell2 = tk.StringVar()
            self.tareloadcell3 = tk.StringVar()
            self.tareloadcell4 = tk.StringVar()
            self.tareloadcell5 = tk.StringVar()
            self.create_widgets()

        def create_widgets(self):
            vcmd = (self.register(self.validate)) #command that gets issued when a command box is edited to make sure only integers get written

            self.zeroloadcell1.set(zeroarray[0])
            self.zeroloadcell2.set(zeroarray[1])
            self.zeroloadcell3.set(zeroarray[2])
            self.zeroloadcell4.set(zeroarray[3])
            self.zeroloadcell5.set(zeroarray[4])

            self.tareloadcell1.set(tarearray[0])
            self.tareloadcell2.set(tarearray[1])
            self.tareloadcell3.set(tarearray[2])
            self.tareloadcell4.set(tarearray[3])
            self.tareloadcell5.set(tarearray[4])

            self.zerolabel = tk.Label(self, text = 'Zero Value', font = self.buttonfont)
            self.zerolabel.grid(column=1, row=0)
            self.tarelabel = tk.Label(self, text = 'Tare Value', font = self.buttonfont)
            self.tarelabel.grid(column=2, row=0)

            self.labelcell1 = tk.Label(self, text = 'Load Cell 1', font = self.buttonfont)
            self.labelcell1.grid(column=0, row=1)
            self.labelcell2 = tk.Label(self, text = 'Load Cell 2', font = self.buttonfont)
            self.labelcell2.grid(column=0, row=2)
            self.labelcell3 = tk.Label(self, text = 'Load Cell 3', font = self.buttonfont)
            self.labelcell3.grid(column=0, row=3)
            self.labelcell4 = tk.Label(self, text = 'Load Cell 4', font = self.buttonfont)
            self.labelcell4.grid(column=0, row=4)
            self.labelcell5 = tk.Label(self, text = 'Load Cell 5', font = self.buttonfont)
            self.labelcell5.grid(column=0, row=5)

            self.zerocelllabel1 = tk.Label(self, textvariable = self.zeroloadcell1, font = self.buttonfont)
            self.zerocelllabel1.grid(column=1,row=1)
            self.zerocelllabel2 = tk.Label(self, textvariable = self.zeroloadcell2, font = self.buttonfont)
            self.zerocelllabel2.grid(column=1,row=2)
            self.zerocelllabel3 = tk.Label(self, textvariable = self.zeroloadcell3, font = self.buttonfont)
            self.zerocelllabel3.grid(column=1,row=3)
            self.zerocelllabel4 = tk.Label(self, textvariable = self.zeroloadcell4, font = self.buttonfont)
            self.zerocelllabel4.grid(column=1,row=4)
            self.zerocelllabel5 = tk.Label(self, textvariable = self.zeroloadcell5, font = self.buttonfont)
            self.zerocelllabel5.grid(column=1,row=5)

            self.tarecelllabel1 = tk.Label(self, textvariable = self.tareloadcell1, font = self.buttonfont)
            self.tarecelllabel1.grid(column=2,row=1)
            self.tarecelllabel2 = tk.Label(self, textvariable = self.tareloadcell2, font = self.buttonfont)
            self.tarecelllabel2.grid(column=2,row=2)
            self.tarecelllabel3 = tk.Label(self, textvariable = self.tareloadcell3, font = self.buttonfont)
            self.tarecelllabel3.grid(column=2,row=3)
            self.tarecelllabel4 = tk.Label(self, textvariable = self.tareloadcell4, font = self.buttonfont)
            self.tarecelllabel4.grid(column=2,row=4)
            self.tarecelllabel5 = tk.Label(self, textvariable = self.tareloadcell5, font = self.buttonfont)
            self.tarecelllabel5.grid(column=2,row=5)

            self.weightlabel = tk.Label(self, text = 'Tare Weight:', font = self.buttonfont)
            self.weightlabel.grid(column=0,row=7)
            self.weightentry = tk.Entry(self, font = self.buttonfont, textvariable = self.weightvar, validate = 'key', validatecommand = (vcmd, '%P'))
            self.weightentry.insert('0', weightfloat[0])
            self.weightentry.grid(column=1, row=7)

            self.zeroall = tk.Button(self, font = self.buttonfont)
            self.zeroall["text"] = "Zero All Load Cells"
            self.zeroall["command"] = self.zero_all_cells
            self.zeroall.grid(column=1,row=6)

            self.openclaw = tk.Button(self, font = self.buttonfont)
            self.openclaw["text"] = "Open Claws"
            self.openclaw["command"] = self.open_claws
            self.openclaw.grid(column=2,row=6)

            self.closeclaw = tk.Button(self, font = self.buttonfont)
            self.closeclaw["text"] = "Close Claws"
            self.closeclaw["command"] = self.close_claws
            self.closeclaw.grid(column=3,row=6)

            self.tarecell1 = tk.Button(self, font = self.buttonfont)
            self.tarecell1["text"] = "Tare Load Cell 1"
            self.tarecell1["command"] = self.tare_cell_one
            self.tarecell1.grid(column=3,row=1)

            self.tarecell2 = tk.Button(self, font = self.buttonfont)
            self.tarecell2["text"] = "Tare Load Cell 2"
            self.tarecell2["command"] = self.tare_cell_two
            self.tarecell2.grid(column=3,row=2)

            self.tarecell3 = tk.Button(self, font = self.buttonfont)
            self.tarecell3["text"] = "Tare Load Cell 3"
            self.tarecell3["command"] = self.tare_cell_three
            self.tarecell3.grid(column=3,row=3)

            self.tarecell4 = tk.Button(self, font = self.buttonfont)
            self.tarecell4["text"] = "Tare Load Cell 4"
            self.tarecell4["command"] = self.tare_cell_four
            self.tarecell4.grid(column=3,row=4)

            self.tarecell5 = tk.Button(self, font = self.buttonfont)
            self.tarecell5["text"] = "Tare Load Cell 5"
            self.tarecell5["command"] = self.tare_cell_five
            self.tarecell5.grid(column=3,row=5)

        def calibrateSer(self):
            robot.reset_input_buffer() #This flushes the serial buffer.
            cmd = bytes('nn', 'utf-8')
            try:
                robot.write(cmd)
            except serial.SerialException:
                commError[0] = True
                return
            s = ''
            tempstr = ""
            while(s != 'D'): #clearing buffer before issuing commands
                try:
                    s = robot.read(1).decode('utf-8')
                except serial.SerialException:
                    commError[0] = True
                    return

            if(self.loadcellflag == 0 or self.loadcellflag == 1):
                cmd = bytes('t1t', 'utf-8') #all UART communications must be made as UTF-8 encoded byte strings. This command resets the robot.
                try:
                    robot.write(cmd) #write to serial buffer.
                except serial.SerialException:
                    commError[0] = True
                    return
                while(s != 'N'):
                    try:
                        s = robot.read(1).decode('utf-8')
                    except serial.SerialException:
                        commError[0] = True
                        return
                    if(s != 'N'):
                        tempstr += s
                while(s != 'D'):
                    try:
                        s = robot.read().decode('utf-8')
                    except serial.SerialException:
                        commError[0] = True
                        return
                if(self.loadcellflag == 0):
                    zeroarray[0] = int(tempstr)
                    self.zeroloadcell1.set(int(tempstr))
                    zeroflags[0] = 1
                elif(zeroflags[0] == 1):
                    tareflags[0] = 1
                    tarearray[0] = (float(tempstr) - float(zeroarray[0])) / float(weightfloat[0])
                    self.tareloadcell1.set(str(tarearray[0]))

            if(self.loadcellflag == 0 or self.loadcellflag == 2):
                tempstr = ""
                cmd = bytes('t2t', 'utf-8')
                try:
                    robot.write(cmd)
                except serial.SerialException:
                    commError[0] = True
                    return
                while(s != 'N'):
                    try:
                        s = robot.read(1).decode('utf-8')
                    except serial.SerialException:
                        commError[0] = True
                        return
                    if(s != 'N'):
                        tempstr += s
                while(s != 'D'):
                    try:
                        s = robot.read().decode('utf-8')
                    except serial.SerialException:
                        commError[0] = True
                        return
                if(self.loadcellflag == 0):
                    zeroarray[1] = int(tempstr)
                    self.zeroloadcell2.set(int(tempstr))
                    zeroflags[1] = 1
                elif(zeroflags[1] == 1):
                    tareflags[1] = 1
                    tarearray[1] = (float(tempstr) - float(zeroarray[1])) / float(weightfloat[0])
                    self.tareloadcell2.set(str(tarearray[1]))

            if(self.loadcellflag == 0 or self.loadcellflag == 3):
                tempstr = ""
                cmd = bytes('t3t', 'utf-8')
                try:
                    robot.write(cmd)
                except serial.SerialException:
                    commError[0] = True
                    return
                while(s != 'N'):
                    try:
                        s = robot.read(1).decode('utf-8')
                    except serial.SerialException:
                        commError[0] = True
                        return
                    if(s != 'N'):
                        tempstr += s
                while(s != 'D'):
                    try:
                        s = robot.read().decode('utf-8')
                    except serial.SerialException:
                        commError[0] = True
                        return
                if(self.loadcellflag == 0):
                    zeroarray[2] = int(tempstr)
                    self.zeroloadcell3.set(int(tempstr))
                    zeroflags[2] = 1
                elif(zeroflags[2] == 1):
                    tareflags[2] = 1
                    tarearray[2] = (float(tempstr) - float(zeroarray[2])) / float(weightfloat[0])
                    self.tareloadcell3.set(str(tarearray[2]))

            if(self.loadcellflag == 0 or self.loadcellflag == 4):
                tempstr = ""
                cmd = bytes('t4t', 'utf-8') #she's just like me!
                try:
                    robot.write(cmd)
                except serial.SerialException:
                    commError[0] = True
                    return
                while(s != 'N'):
                    try:
                        s = robot.read(1).decode('utf-8')
                    except serial.SerialException:
                        commError[0] = True
                        return
                    if(s != 'N'):
                        tempstr += s
                while(s != 'D'):
                    try:
                        s = robot.read().decode('utf-8')
                    except serial.SerialException:
                        commError[0] = True
                        return
                if(self.loadcellflag == 0):
                    zeroarray[3] = int(tempstr)
                    self.zeroloadcell4.set(int(tempstr))
                    zeroflags[3] = 1
                elif(zeroflags[3] == 1):
                    tareflags[3] = 1
                    tarearray[3] = (float(tempstr) - float(zeroarray[3])) / float(weightfloat[0])
                    self.tareloadcell4.set(str(tarearray[3]))

            if(self.loadcellflag == 0 or self.loadcellflag == 5):
                tempstr = ""
                cmd = bytes('t5t', 'utf-8')
                try:
                    robot.write(cmd)
                except serial.SerialException:
                    commError[0] = True
                    return
                while(s != 'N'):
                    try:
                        s = robot.read(1).decode('utf-8')
                    except serial.SerialException:
                        commError[0] = True
                        return
                    if(s != 'N'):
                        tempstr += s
                while(s != 'D'):
                    try:
                        s = robot.read().decode('utf-8')
                    except serial.SerialException:
                        commError[0] = True
                        return
                if(self.loadcellflag == 0):
                    zeroarray[4] = int(tempstr)
                    self.zeroloadcell5.set(int(tempstr))
                    zeroflags[4] = 1
                elif(zeroflags[4] == 1):
                    tareflags[4] = 1
                    tarearray[4] = (float(tempstr) - float(zeroarray[4])) / float(weightfloat[0])
                    self.tareloadcell5.set(str(tarearray[4]))

        def zero_all_cells(self):
            self.loadcellflag = 0
            if((threading.active_count() <= 3) and not disconnected[0]):
                serthread = threading.Thread(target = self.calibrateSer)
                serthread.start()

        def tare_cell_one(self):
            self.loadcellflag = 1
            if((threading.active_count() <= 3) and not disconnected[0]):
                serthread = threading.Thread(target = self.calibrateSer)
                serthread.start()

        def tare_cell_two(self):
            self.loadcellflag = 2
            if((threading.active_count() <= 3) and not disconnected[0]):
                serthread = threading.Thread(target = self.calibrateSer)
                serthread.start()

        def tare_cell_three(self):
            self.loadcellflag = 3
            if((threading.active_count() <= 3) and not disconnected[0]):
                serthread = threading.Thread(target = self.calibrateSer)
                serthread.start()

        def tare_cell_four(self):
            self.loadcellflag = 4
            if((threading.active_count() <= 3) and not disconnected[0]):
                serthread = threading.Thread(target = self.calibrateSer)
                serthread.start()

        def tare_cell_five(self):
            self.loadcellflag = 5
            if((threading.active_count() <= 3) and not disconnected[0]):
                serthread = threading.Thread(target = self.calibrateSer)
                serthread.start()

        def open_claws(self):
            if(not disconnected[0]):
                cmd = bytes('yy', 'utf-8')
                try:
                    robot.write(cmd)
                except serial.SerialException:
                    commError[0] = True
                    return
                s = robot.read().decode('utf-8')
                while(s != 'D'):
                    s = robot.read().decode('utf-8')

        def close_claws(self):
            if(not disconnected[0]):
                cmd = bytes('hh', 'utf-8')
                try:
                    robot.write(cmd)
                except serial.SerialException:
                    commError[0] = True
                    return
                s = robot.read().decode('utf-8')
                while(s != 'D'):
                    s = robot.read().decode('utf-8')

        def validate(self, P): #ensures entered character is an integer
            if str.isdigit(P) or P == "":
                weightfloat[0] = P
                return True
            else:
                return False

    class Setup(tk.Toplevel):
        def __init__(self, master):
            super().__init__(master)
            self.master = master
            self.wm_title("Setup Parameters")
            self.geometry("800x360")
            self.buttonfont = "Helvetica 24"

            self.optionvar = tk.StringVar()
            self.setentry1= tk.StringVar()
            self.setentry2= tk.StringVar()
            self.setentry3= tk.StringVar()
            self.setentry4= tk.StringVar()
            self.setentry5= tk.StringVar()
            self.setcheck1= tk.IntVar()
            self.setcheck2= tk.IntVar()
            self.setcheck3= tk.IntVar()
            self.setcheck4= tk.IntVar()
            self.setcheck5= tk.IntVar()

            self.create_widgets()

        def create_widgets(self):
            vcmd = (self.register(self.validate)) #command that gets issued when a command box is edited to make sure only integers get written
            vcmda = (self.register(self.validatealpha)) #same as above for only letters

            alphaOptions = []
            tmpstr = 'A'
            ENC_TYPE = 'ascii'
            while(tmpstr != 'ZZ'):
                alphaOptions.append(tmpstr)
                s = bytearray(tmpstr, ENC_TYPE)
                if(len(s) == 2):
                    if(s[1] == ord('Z')):
                        s[1] = ord('A')
                        if(s[0] == ord('Z')):
                            tmpstr = 'A'
                        else:
                            s[0] = s[0] + 1
                            tmpstr = s.decode(ENC_TYPE)
                    else:
                        s[1] = s[1] + 1
                        tmpstr = s.decode(ENC_TYPE)
                else:
                    if(s[0] == ord('Z')):
                        tmpstr = 'AA'
                    else:
                        s[0] = s[0] + 1
                        tmpstr = s.decode(ENC_TYPE)
            alphaOptions.append(tmpstr)

            #setup GUI section for the alphanumeric code entering.
            self.label = tk.Label(self,  text='Select Tray Labelling:', font = self.buttonfont)
            self.label.grid(column=0, row=0) #All of this GUI is setup as a grid.

            self.alphabetical = ttk.Combobox(self, font = self.buttonfont, textvariable = self.optionvar)
            self.alphabetical.set(alphavar[0])
            self.alphabetical['values'] = alphaOptions
            self.alphabetical.grid(column=1, row=0)

            #setup all the entry forms and radio buttons for the number of trays and number of cups per tray.
            self.traylabel1 = tk.Label(self,  text='Select Tray Numbering:', font = self.buttonfont)
            self.traylabel1.grid(column=0, row=1)
            self.tray1 = tk.Entry(self, font = self.buttonfont, textvariable = self.setentry1, validate = 'key', validatecommand = (vcmd, '%P'))
            self.tray1.insert('0', cuparray[0])
            self.tray1.grid(column=1, row=1)
            self.checktray1 = tk.Checkbutton(self, variable= self.setcheck1)
            if(checkarray[0] == 1):
                self.checktray1.select()
            else:
                self.checktray1.deselect()
            self.checktray1.grid(column=2, row=1)

            self.traylabel2 = tk.Label(self,  text='Select Tray Numbering:', font = self.buttonfont)
            self.traylabel2.grid(column=0, row=2)
            self.tray2 = tk.Entry(self, font = self.buttonfont,textvariable = self.setentry2, validate = 'key', validatecommand = (vcmd, '%P'))
            self.tray2.insert('0', cuparray[1])
            self.tray2.grid(column=1, row=2)
            self.checktray2 = tk.Checkbutton(self, variable= self.setcheck2)
            if(checkarray[1] == 1):
                self.checktray2.select()
            else:
                self.checktray2.deselect()
            self.checktray2.grid(column=2, row=2)

            self.traylabel3 = tk.Label(self,  text='Select Tray Numbering:', font = self.buttonfont)
            self.traylabel3.grid(column=0, row=3)
            self.tray3 = tk.Entry(self, font = self.buttonfont, textvariable = self.setentry3, validate = 'key', validatecommand = (vcmd, '%P'))
            self.tray3.insert('0', cuparray[2])
            self.tray3.grid(column=1, row=3)
            self.checktray3 = tk.Checkbutton(self, variable= self.setcheck3)
            if(checkarray[2] == 1):
                self.checktray3.select()
            else:
                self.checktray3.deselect()
            self.checktray3.grid(column=2, row=3)

            self.traylabel4 = tk.Label(self,  text='Select Tray Numbering:', font = self.buttonfont)
            self.traylabel4.grid(column=0, row=4)
            self.tray4 = tk.Entry(self, font = self.buttonfont, textvariable = self.setentry4, validate = 'key', validatecommand = (vcmd, '%P'))
            self.tray4.insert('0', cuparray[3])
            self.tray4.grid(column=1, row=4)
            self.checktray4 = tk.Checkbutton(self, variable= self.setcheck4)
            if(checkarray[3] == 1):
                self.checktray4.select()
            else:
                self.checktray4.deselect()
            self.checktray4.grid(column=2, row=4)

            self.traylabel5 = tk.Label(self,  text='Select Tray Numbering:', font = self.buttonfont)
            self.traylabel5.grid(column=0, row=5)
            self.tray5 = tk.Entry(self, font = self.buttonfont, textvariable = self.setentry5, validate = 'key', validatecommand = (vcmd, '%P'))
            self.tray5.insert('0', cuparray[4])
            self.tray5.grid(column=1, row=5)
            self.checktray5 = tk.Checkbutton(self, variable= self.setcheck5)
            if(checkarray[4] == 1):
                self.checktray5.select()
            else:
                self.checktray5.deselect()
            self.checktray5.grid(column=2, row=5)

            #apply setup parameters.
            self.okay = tk.Button(self, font = self.buttonfont)
            self.okay["text"] = "Apply"
            self.okay["command"] = self.set_setup
            self.okay.grid(column=1,row=6)

        def validate(self, P): #ensures entered character is an integer
            if str.isdigit(P) or P == "":
                return True
            else:
                return False

        def validatealpha(self, P): #ensures entered character is an integer
            if (str.isalpha(P) and str.isupper(P)) or P == "":
                return True
            else:
                return False

        def set_setup(self):
            alphavar[0] = str(self.optionvar.get())
            checkarray[0] = int(self.setcheck1.get())
            checkarray[1] = int(self.setcheck2.get())
            checkarray[2] = int(self.setcheck3.get())
            checkarray[3] = int(self.setcheck4.get())
            checkarray[4] = int(self.setcheck5.get())
            cuparray[0] = int(self.setentry1.get())
            cuparray[1] = int(self.setentry2.get())
            cuparray[2] = int(self.setentry3.get())
            cuparray[3] = int(self.setentry4.get())
            cuparray[4] = int(self.setentry5.get())
            self.destroy()

    class Maintenance(tk.Toplevel):
        def __init__(self, master):
            super().__init__(master)
            self.master = master
            self.wm_title("Maintenance Parameters")
            self.geometry("1500x550")

            self.optionList = ('red', 'orange', 'yellow', 'green', 'blue', 'purple')
            self.wbc0 = tk.StringVar()
            self.wbc0.set(wbc[0])
            self.wbc1 = tk.StringVar()
            self.wbc1.set(wbc[1])
            self.wbc2 = tk.StringVar()
            self.wbc2.set(wbc[2])

            self.wb0 = tk.StringVar()
            self.wb1 = tk.StringVar()

            self.xposi0 = tk.StringVar()
            self.xposi1 = tk.StringVar()
            self.xposi2 = tk.StringVar()

            self.yposi0 = tk.StringVar()
            self.yposi1 = tk.StringVar()
            self.yposi2 = tk.StringVar()
            self.yposi3 = tk.StringVar()
            self.yposi4 = tk.StringVar()
            self.yposi5 = tk.StringVar()
            self.yposi6 = tk.StringVar()
            self.yposi7 = tk.StringVar()
            self.yposi8 = tk.StringVar()
            self.yposi9 = tk.StringVar()
            self.yposi10 = tk.StringVar()
            self.yposi11 = tk.StringVar()

            self.zposi0 = tk.StringVar()
            self.zposi1 = tk.StringVar()
            self.zsteps = tk.StringVar()

            self.buttonfont = "Helvetica 24"

            self.create_widgets()

        def create_widgets(self):
            #setup GUI section for the alphanumeric code entering.
            vcmd = (self.register(self.validate)) #command that gets issued when a command box is edited to make sure only integers get written
            self.xlab = tk.Label(self,  text='X Positions', font = self.buttonfont)
            self.xlab.grid(column=0, row=0)
            self.xpos1 = tk.Entry(self, font = self.buttonfont, textvariable = self.xposi0, validate = 'key', validatecommand = (vcmd, '%P'))
            self.xpos1.insert('0', xposarray[0])
            self.xpos1.grid(column=1, row=0)
            self.xpos2 = tk.Entry(self, font = self.buttonfont, textvariable = self.xposi1, validate = 'key', validatecommand = (vcmd, '%P'))
            self.xpos2.insert('0', xposarray[1])
            self.xpos2.grid(column=2, row=0)
            self.xpos3 = tk.Entry(self, font = self.buttonfont, textvariable = self.xposi2, validate = 'key', validatecommand = (vcmd, '%P'))
            self.xpos3.insert('0', xposarray[2])
            self.xpos3.grid(column=3, row=0)

            self.ylab1 = tk.Label(self,  text='Y Positions 1-3', font = self.buttonfont)
            self.ylab1.grid(column=0, row=1)
            self.ypos1 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi0, validate = 'key', validatecommand = (vcmd, '%P'))
            self.ypos1.insert('0', yposarray[0])
            self.ypos1.grid(column=1, row=1)
            self.ypos2 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi1, validate = 'key', validatecommand = (vcmd, '%P'))
            self.ypos2.insert('0', yposarray[1])
            self.ypos2.grid(column=2, row=1)
            self.ypos3 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi2, validate = 'key', validatecommand = (vcmd, '%P'))
            self.ypos3.insert('0', yposarray[2])
            self.ypos3.grid(column=3, row=1)

            self.ylab2 = tk.Label(self,  text='Y Positions 4-6', font = self.buttonfont)
            self.ylab2.grid(column=0, row=2)
            self.ypos4 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi3, validate = 'key', validatecommand = (vcmd, '%P'))
            self.ypos4.insert('0', yposarray[3])
            self.ypos4.grid(column=1, row=2)
            self.ypos5 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi4, validate = 'key', validatecommand = (vcmd, '%P'))
            self.ypos5.insert('0', yposarray[4])
            self.ypos5.grid(column=2, row=2)
            self.ypos6 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi5, validate = 'key', validatecommand = (vcmd, '%P'))
            self.ypos6.insert('0', yposarray[5])
            self.ypos6.grid(column=3, row=2)

            self.ylab3 = tk.Label(self,  text='Y Positions 7-9', font = self.buttonfont)
            self.ylab3.grid(column=0, row=3)
            self.ypos7 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi6, validate = 'key', validatecommand = (vcmd, '%P'))
            self.ypos7.insert('0', yposarray[6])
            self.ypos7.grid(column=1, row=3)
            self.ypos8 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi7, validate = 'key', validatecommand = (vcmd, '%P'))
            self.ypos8.insert('0', yposarray[7])
            self.ypos8.grid(column=2, row=3)
            self.ypos9 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi8, validate = 'key', validatecommand = (vcmd, '%P'))
            self.ypos9.insert('0', yposarray[8])
            self.ypos9.grid(column=3, row=3)

            self.ylab4 = tk.Label(self,  text='Y Positions 10-12', font = self.buttonfont)
            self.ylab4.grid(column=0, row=4)
            self.ypos10 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi9, validate = 'key', validatecommand = (vcmd, '%P'))
            self.ypos10.insert('0', yposarray[9])
            self.ypos10.grid(column=1, row=4)
            self.ypos11 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi10, validate = 'key', validatecommand = (vcmd, '%P'))
            self.ypos11.insert('0', yposarray[10])
            self.ypos11.grid(column=2, row=4)
            self.ypos12 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi11, validate = 'key', validatecommand = (vcmd, '%P'))
            self.ypos12.insert('0', yposarray[11])
            self.ypos12.grid(column=3, row=4)

            self.zlab0 = tk.Label(self,  text='Z Distance To Cups', font = self.buttonfont)
            self.zlab0.grid(column=0, row=5)
            self.zpos0 = tk.Entry(self, font = self.buttonfont, textvariable = self.zposi0, validate = 'key', validatecommand = (vcmd, '%P'))
            self.zpos0.insert('0', zposarray[0])
            self.zpos0.grid(column=1, row=5)

            self.zlab1 = tk.Label(self,  text='Z Weight Meas Dist', font = self.buttonfont)
            self.zlab1.grid(column=2, row=5)
            self.zpos1 = tk.Entry(self, font = self.buttonfont, textvariable = self.zposi1, validate = 'key', validatecommand = (vcmd, '%P'))
            self.zpos1.insert('0', zposarray[1])
            self.zpos1.grid(column=3, row=5)

            self.cblab0 = tk.Label(self,  text='Weight Too Low Color', font = self.buttonfont)
            self.cblab0.grid(column=0, row=6)
            self.cb0 = tk.OptionMenu(self, self.wbc0, *self.optionList)
            self.cb0.config(font = self.buttonfont)
            self.cb0.grid(column=1, row=6)

            self.wblab0 = tk.Label(self,  text='Weight Too Low Bound', font = self.buttonfont)
            self.wblab0.grid(column=2, row=6)
            self.wbentry0 = tk.Entry(self, font = self.buttonfont, textvariable = self.wb0, validate = 'key', validatecommand = (vcmd, '%P'))
            self.wbentry0.insert('0', wb[0])
            self.wbentry0.grid(column=3, row=6)

            self.cblab1 = tk.Label(self,  text='Weight Too High Color', font = self.buttonfont)
            self.cblab1.grid(column=0, row=7)
            self.cb1 = tk.OptionMenu(self, self.wbc1, *self.optionList)
            self.cb1.config(font = self.buttonfont)
            self.cb1.grid(column=1, row=7)

            self.wblab1 = tk.Label(self,  text='Weight Too High Bound', font = self.buttonfont)
            self.wblab1.grid(column=2, row=7)
            self.wbentry1 = tk.Entry(self, font = self.buttonfont, textvariable = self.wb1, validate = 'key', validatecommand = (vcmd, '%P'))
            self.wbentry1.insert('0', wb[1])
            self.wbentry1.grid(column=3, row=7)

            self.cblab2 = tk.Label(self,  text='Weight In Bounds Color', font = self.buttonfont)
            self.cblab2.grid(column=0, row=8)
            self.cb2 = tk.OptionMenu(self, self.wbc2, *self.optionList)
            self.cb2.config(font = self.buttonfont)
            self.cb2.grid(column=1, row=8)

            self.wblab1 = tk.Label(self,  text='Number of Steps', font = self.buttonfont)
            self.wblab1.grid(column=0, row=9)
            self.wbentry1 = tk.Entry(self, font = self.buttonfont, textvariable = self.zsteps, validate = 'key', validatecommand = (vcmd, '%P'))
            self.wbentry1.insert('0', 100)
            self.wbentry1.grid(column=1, row=9)

            self.mvtrup = tk.Button(self, font = self.buttonfont)
            self.mvtrup["text"] = "Move Tray Up N Steps"
            self.mvtrup["command"] = self.move_up
            self.mvtrup.grid(column=2,row=9)

            self.mvtrdn = tk.Button(self, font = self.buttonfont)
            self.mvtrdn["text"] = "Move Tray Down N Steps"
            self.mvtrdn["command"] = self.move_down
            self.mvtrdn.grid(column=3,row=9)

            #apply setup parameters.
            self.okay = tk.Button(self, font = self.buttonfont)
            self.okay["text"] = "Apply"
            self.okay["command"] = self.set_maintenance
            self.okay.grid(column=0,row=10)

        def validate(self, P): #ensures entered character is an integer
            if str.isdigit(P) or P == "":
                return True
            else:
                return False

        def move_up(self):
            if(not disconnected[0] and int(self.zsteps.get()) > 0):
                robot.reset_input_buffer() #This flushes the serial buffer.
                cmdstring = 'u' + '{0:05d}'.format(int(self.zsteps.get()))
                cmd = bytes(cmdstring, 'utf-8')
                try:
                    robot.write(cmd)
                except serial.SerialException:
                    commError[0] = True
                    return
                s = ''
                while(s != 'D'): #clearing buffer before issuing commands
                    try:
                        s = robot.read().decode('utf-8') #wait until robot makes a reply, basically. 'D' is our ACK character.
                    except serial.SerialException:
                        commError[0] = True
                        return
        def move_down(self):
            if(not disconnected[0] and int(self.zsteps.get()) > 0):
                robot.reset_input_buffer() #This flushes the serial buffer.
                cmdstring = 'o' + '{0:05d}'.format(int(self.zsteps.get()))
                cmd = bytes(cmdstring, 'utf-8')
                try:
                    robot.write(cmd)
                except serial.SerialException:
                    commError[0] = True
                    return

                s = ''
                while(s != 'D'): #clearing buffer before issuing commands
                    try:
                        s = robot.read().decode('utf-8') #wait until robot makes a reply, basically. 'D' is our ACK character.
                    except serial.SerialException:
                        commError[0] = True
                        return

        def set_maintenance(self):
            xposarray[0] = int(self.xposi0.get())
            xposarray[1] = int(self.xposi1.get())
            xposarray[2] = int(self.xposi2.get())
            yposarray[0] = int(self.yposi0.get())
            yposarray[1] = int(self.yposi1.get())
            yposarray[2] = int(self.yposi2.get())
            yposarray[3] = int(self.yposi3.get())
            yposarray[4] = int(self.yposi4.get())
            yposarray[5] = int(self.yposi5.get())
            yposarray[6] = int(self.yposi6.get())
            yposarray[7] = int(self.yposi7.get())
            yposarray[8] = int(self.yposi8.get())
            yposarray[9] = int(self.yposi9.get())
            yposarray[10] = int(self.yposi10.get())
            yposarray[11] = int(self.yposi11.get())
            zposarray[0] = int(self.zposi0.get())
            zposarray[1] = int(self.zposi1.get())
            wbc[0] = self.wbc0.get()
            wb[0] = int(self.wb0.get())
            wbc[1] = self.wbc1.get()
            wb[1] = int(self.wb1.get())
            wbc[2] = self.wbc2.get()
            if(not disconnected[0] and int(self.zposi0.get()) > 0):
                robot.reset_input_buffer() #This flushes the serial buffer.
                cmdstring = 'o' + '{0:05d}'.format(int(self.zposi0.get()))
                cmd = bytes(cmdstring, 'utf-8')
                try:
                    robot.write(cmd)
                except serial.SerialException:
                    commError[0] = True
                s = ''
                while(s != 'D'): #clearing buffer before issuing commands
                    try:
                        s = robot.read().decode('utf-8') #wait until robot makes a reply, basically. 'D' is our ACK character.
                    except serial.SerialException:
                        commError[0] = True
                        break
            try:
                if os.path.exists("config.cfg"):
                    os.remove("config.cfg")
                newConfig = open('config.cfg', 'w')
                newConfig.write('xposarray' + ' ' + self.xposi0.get() + ' ' + self.xposi1.get() + ' ' + self.xposi2.get() + '\n')
                newConfig.write('yposarray' + ' ' + self.yposi0.get() + ' ' + self.yposi1.get() + ' ' + self.yposi2.get())
                newConfig.write(' ' + self.yposi3.get() + ' ' + self.yposi4.get() + ' ' + self.yposi5.get())
                newConfig.write(' ' + self.yposi6.get() + ' ' + self.yposi7.get() + ' ' + self.yposi8.get())
                newConfig.write(' ' + self.yposi9.get() + ' ' + self.yposi10.get() + ' ' + self.yposi11.get() + '\n')
                newConfig.write('zposarray' + ' ' + self.zposi0.get() + ' ' + self.zposi1.get() + '\n')
                newConfig.write('weight bounds' + ' ' + self.wb0.get() + ' ' + self.wb1.get() + '\n')
                newConfig.write('weight bound colors' + ' ' + self.wbc0.get() + ' ' + self.wbc1.get() + ' ' + self.wbc2.get() + '\n')
                newConfig.close()
            except OSError:
                pass
            self.destroy()


    class App(tk.Tk):
        def quitout(self): #kills all threads then exits
            self.killThreads = True
            app.destroy()

        def autoneg(self): #autonegotiation function. This is always running while the GUI is. It connects to the robot serial port.
            while(not self.killThreads):
                listports = serial.tools.list_ports.comports() #lists all COM ports on the computer.
                self.arduinoflag = False
                for it in listports:
                    descstring = str(it.description) #convert to a string
                    if("Arduino" in descstring): #looks for Arduino to connect to.
                        self.arduinoflag = True
                        commError[0] = False
                        self.CommErrorFlag = False
                        if(not robot.is_open and self.disconnected): #attempt to connect or reconnect
                            robot.port = it.device #sets port number to Arduino's port.
                            robot.baudrate = 9600 #sets baud rate. This can be a constant.
                            robot.open() #opens the serial port. This function only opens if the port is valid and not in use.
                            self.disconnected = False
                            disconnected[0] = False
                            self.connect.configure(text = "Connected", bg = "green")
                if(not self.arduinoflag): #device was disconnected, update status.
                    robot.close()
                    self.disconnected = True
                    disconnected[0] = True
                    self.connect.configure(text = "Disconnected", bg = "red")
                time.sleep(1)
            robot.close()

        def alert_loop(self):
            while(not self.killThreads):
                if(commError[0]):
                    self.CommErrorFlag = True
                if(self.CommErrorFlag):
                    self.tray.configure(bg='red')
                    time.sleep(1)
                elif(self.doneFlag):
                    self.tray.configure(bg='green')
                    time.sleep(1)
                self.tray.configure(bg='white')
                time.sleep(1)

        def __init__(self): #Initializes the main GUI
            super().__init__()
            self.disconnected = True #this variable determines if the robot is connected or not. This is so we are safe from communication errors.
            self.doneFlag = False
            self.CommErrorFlag = False
            self.EntryErrorFlag = False
            self.killThreads = False
            autoneg = threading.Thread(target = self.autoneg)
            autoneg.start()
            self.create_widgets()
            #similar to global variables
            self.pauseflag = False #These are two flag variables I use to handle the program state.
            self.termflag = False #Currently the 3 states are normal, paused, and terminate run.
            self.protocol("WM_DELETE_WINDOW", self.quitout)



        def create_widgets(self): #Creates all the buttons and Visual stuff.

            #GUI size and fonts
            self.tray = tk.Canvas(self, width = "1900", height = "1000")
            self.tray.pack()

            alert = threading.Thread(target = self.alert_loop)
            alert.start()

            self.buttonfont = "Helvetica 24"
            self.buttonfontmain = "Helvetica 36"

            #here are all the buttons
            self.run = tk.Button(self, font = self.buttonfont)
            self.run["text"] = "Run"
            self.run["command"] = self.run_button
            self.run.place(x = 1450, y = 25)

            self.pause = tk.Button(self, font = self.buttonfont)
            self.pause["text"] = "Pause"
            self.pause["command"] = self.pause_button
            self.pause.place(x = 1540, y = 25)

            self.terminate = tk.Button(self, font = self.buttonfont)
            self.terminate["text"] = "Terminate"
            self.terminate["command"] = self.term_button
            self.terminate.place(x = 1660, y = 25)

            self.calibrate = tk.Button(self, font = self.buttonfont)
            self.calibrate["text"] = "Calibrate"
            self.calibrate["command"] = self.calibrate_cells
            self.calibrate.place(x = 1450, y = 125)

            self.testrun = tk.Button(self, font = self.buttonfont)
            self.testrun["text"] = "Test Run"
            self.testrun["command"] = self.test_button
            self.testrun.place(x = 1450, y = 425)

            self.connect = tk.Button(self, font = self.buttonfont)
            self.connect["text"] = "Disconnected"
            self.connect["bg"] = "red"
            self.connect.place(x = 1655, y = 325)

            self.maintenance = tk.Button(self, font = self.buttonfont)
            self.maintenance["text"] = "Maintenance"
            self.maintenance["command"] = self.maintenance_param
            self.maintenance.place(x = 1605, y = 125)

            self.setup = tk.Button(self, font = self.buttonfont)
            self.setup["text"] = "Setup Parameters"
            self.setup["command"] = self.setup_param
            self.setup.place(x = 1450, y = 225)

            self.write = tk.Button(self, font = self.buttonfont)
            self.write["text"] = "Write to File"
            self.write["command"] = self.write_to_file
            self.write.place(x = 1450, y = 325)

            #These are the arrays that display the color and weight data of each cup onto the GUI.
            #They are 12 by 15, which is 180 cups.
            #We could make an array that stores all the cup weights as floats to print to the text file.
            #Though the existing string array "sampletext" may be fine for this.
            self.samples = [[0 for x in range(12)] for y in range(15)]
            self.sampletext = [[0 for x in range(12)] for y in range(15)]
            self.sampleweight = [[0 for x in range(12)] for y in range(15)]

            #This generates all the positions for the cup visualization in the GUI.
            for x in range(15):
                for y in range(12):
                    self.samples[x][y] = self.tray.create_oval((300 * math.floor(x/3)) + (80 * (x % 3)) + 5, 80 * y + 5, (300 * math.floor(x/3)) + (80 * (x % 3)) + 80, 80 * y + 80, fill = "gray")
                    self.sampletext[x][y] = self.tray.create_text((300 * math.floor(x/3)) + (80 * (x % 3)) + 40, 80 * y + 40, text = "0", justify = tk.CENTER, font = "Helvetica 20")
                    self.sampleweight[x][y] = 0

        def write_to_file(self):
            if(self.doneFlag == True):
                writefile = threading.Thread(target = self.data_output)
                writefile.start()

        #The termination button sets the GUI into termination state.
        def term_button(self):
            self.termflag = True

        #The pause button puts the GUI into Pause state. It unpauses as well.
        def pause_button(self):
            if(self.pauseflag):
                self.pauseflag = False
            else:
                self.pauseflag = True

        #This function generates fake weight data and writes it to the GUI array.
        #It also handles the cup colors, so when we implement customs cup colors we need to make sure
        #The cup colors are not constants like they are right now.
        def write_to_sample(self, x, y, weight): #takes x and y position in array as parameters.
            color = wbc[2]
            if weight < wb[0]: #oh yeah these weight comparison values also should not be constants.
                color = wbc[0]
            elif weight > wb[1]:
                color = wbc[1]
            self.tray.itemconfig(self.samples[x][y], fill = color) #Write color to array.
            self.tray.itemconfig(self.sampletext[x][y], text = str(weight)) #Write weight to array.
            self.sampleweight[x][y] = weight

        def data_output(self):
            #Turn off the completion alert
            self.doneFlag = False
            #First we create a text file with proper formatting to be written to.
            now = datetime.now() #Gets the date and time
            dt = now.strftime("%y_%m_%d Time_%Hh%Mm%Ss") #Formats dte and time for filename purposes
            tray1 = alphavar[0] #String that holds tray alphanumerics
            cupnumber = 1 #Initial cup of the run. Temporary variable: Should be replaced with cupnumber from setup parameters
            cup = '{0:05d}'.format(cupnumber) #Formats cup number properly
            filename = tray1 + cup + "_" + dt + ".txt" #collates the information into the proper file name
            try:
                file = open(r"./Output_Data/"+filename, "w") #Creates a file with the correct name
            except OSError:
                os.makedirs('Output_Data')
                file = open(r"./Output_Data/"+filename, "w") #Creates a file with the correct name
            file.write("***********************************\n") #This and the next few lines create the header for the text file
            file.write("        Weight Data File\n")
            file.write("***********************************\n")
            file.write("\n")
            file.write("Sample, Weight\n")
            file.write("\n")
            if(checkarray[0] == 1):
                for x in range(3): #These for loops iterate over the sampletext matrix,
                    for y in range(12):
                        if(cuparray[0] > 12*x + y):
                            file.write(tray1 + cup + ",  " + str(self.sampleweight[x][y]) + "\n")
                            cupnumber = cupnumber + 1
                            cup = '{0:05d}'.format(cupnumber)
            if(checkarray[1] == 1):
                for x in range(3, 6):
                    for y in range(12):
                        if(cuparray[1] > 12*(x-3) + y):
                            file.write(tray1 + cup + ",  " + str(self.sampleweight[x][y]) + "\n")
                            cupnumber = cupnumber + 1
                            cup = '{0:05d}'.format(cupnumber)
            if(checkarray[2] == 1):
                for x in range(6, 9):
                    for y in range(12):
                        if(cuparray[2] > 12*(x-6) + y):
                            file.write(tray1 + cup + ",  " + str(self.sampleweight[x][y]) + "\n")
                            cupnumber = cupnumber + 1
                            cup = '{0:05d}'.format(cupnumber)
            if(checkarray[3] == 1):
                for x in range(9, 12):
                    for y in range(12):
                        if(cuparray[3] > 12*(x-9) + y):
                            file.write(tray1 + cup + ",  " + str(self.sampleweight[x][y]) + "\n")
                            cupnumber = cupnumber + 1
                            cup = '{0:05d}'.format(cupnumber)
            if(checkarray[4] == 1):
                for x in range(12, 15):
                    for y in range(12):
                        if(cuparray[4] > 12*(x-12) + y):
                            file.write(tray1 + cup + ",  " + str(self.sampleweight[x][y]) + "\n")
                            cupnumber = cupnumber + 1
                            cup = '{0:05d}'.format(cupnumber)

            ENC_TYPE = 'ascii'
            s = bytearray(tray1, ENC_TYPE)
            if(len(s) == 2):
                if(s[1] == ord('Z')):
                    s[1] = ord('A')
                    if(s[0] == ord('Z')):
                        alphavar[0] = 'A'
                    else:
                        s[0] = s[0] + 1
                        alphavar[0] = s.decode(ENC_TYPE)
                else:
                    s[1] = s[1] + 1
                    alphavar[0] = s.decode(ENC_TYPE)
            else:
                if(s[0] == ord('Z')):
                    alphavar[0] = 'AA'
                else:
                    s[0] = s[0] + 1
                    alphavar[0] = s.decode(ENC_TYPE)
            file.close()


        def examplerun(self):
            x = 0
            y = 0
            for j in range(15): #resets all the cup colors and weights.
                for k in range(12):
                    self.tray.itemconfig(self.samples[j][k], fill = "gray")
                    self.tray.itemconfig(self.sampletext[j][k], text = "0")
            while(not self.killThreads):
                while(self.pauseflag): #While loop that basically holds the program while it is paused.
                    time.sleep(.5)
                    if(self.termflag): #I still want to be able to terminate while paused so i copied the code.
                        for j in range(15): #resets all the cup colors and weights.
                            for k in range(12):
                                self.tray.itemconfig(self.samples[j][k], fill = "gray")
                                self.tray.itemconfig(self.sampletext[j][k], text = "0")
                        self.termflag = False #puts UI back in normal state after term routine is finished, then exits loop.
                        self.pauseflag = False
                        return
                if(self.termflag): #same as above, just for when the run is unpaused.
                    for j in range(15): #resets all the cup colors and weights.
                        for k in range(12):
                            self.tray.itemconfig(self.samples[j][k], fill = "gray")
                            self.tray.itemconfig(self.sampletext[j][k], text = "0")
                    self.termflag = False
                    return
                if(tareflags[0] == 1 and checkarray[0] == 1 and (cuparray[0] > 12*x + y)):
                    self.write_to_sample(x, y, round(random.gauss(50, 5), 2)) #generates a random number based on gaussian distribution.) #calls write to sample 5 times because there are 5 claws that make measurements.
                if(tareflags[1] == 1 and checkarray[1] == 1 and (cuparray[1] > 12*x + y)):
                    self.write_to_sample(x+3, y, round(random.gauss(50, 5), 2))
                if(tareflags[2] == 1 and checkarray[2] == 1 and (cuparray[2] > 12*x + y)):
                    self.write_to_sample(x+6, y, round(random.gauss(50, 5), 2))
                if(tareflags[3] == 1 and checkarray[3] == 1 and (cuparray[3] > 12*x + y)):
                    self.write_to_sample(x+9, y, round(random.gauss(50, 5), 2))
                if(tareflags[4] == 1 and checkarray[4] == 1 and (cuparray[4] > 12*x + y)):
                    self.write_to_sample(x+12, y, round(random.gauss(50, 5), 2))
                time.sleep(.1)
                y = y+1
                if(y > 11):
                    y = 0
                    x = x+1

                if(x > 2):
                    self.doneFlag = True
                    return

        #This function handles all robot communications.
        #It's a bit complex at the moment. There are several parts.
        #This function consists of a state machine which sends commands to the robot.
        #I will explain the commands as they show up; however, this code does not have the full routine yet
        #so it is not exhaustive.
        #OH YEAH I SHOULD NOTE THAT THIS ONLY GETS EXECUTED AS A THREAD.
        #THIS IS BECAUSE THERES A HUGE LOOP IN HERE THAT I DO NOT WANT TO HAVE BLOCKING GUI INTERACTION.
        #The thread gets initialized in a different function below.
        def robotSer(self):
            x = 0 #setting position variables and iterators.
            y = 0
            xpos = 0
            ypos = 0
            i = 0
            tmpstr = ""
            robot.reset_input_buffer() #This flushes the serial buffer.
            cmd = bytes('rr', 'utf-8')
            try:
                robot.write(cmd)
            except serial.SerialException:
                self.CommErrorFlag = True
                return
            s = ''
            while(s != 'D'): #clearing buffer before issuing commands
                try:
                    s = robot.read(1).decode('utf-8')
                except serial.SerialException:
                    self.CommErrorFlag = True
                    return
            for j in range(15): #resets all the cup colors and weights.
                for k in range(12):
                    self.tray.itemconfig(self.samples[j][k], fill = "gray")
                    self.tray.itemconfig(self.sampletext[j][k], text = "0")
            #This loops until we either terminate the run or the run finishes. I use 'return' to exit the loop.
            while(not self.killThreads):
                while(self.pauseflag): #While loop that basically holds the program while it is paused.
                    time.sleep(.5)
                    if(self.termflag): #I still want to be able to terminate while paused so i copied the code.
                        if(i > 2):
                            cmd = bytes('hh', 'utf-8') #This ensures the claws are in the idle position so they dont consume power.
                            try:
                                robot.write(cmd)
                            except serial.SerialException:
                                self.CommErrorFlag = True
                                return
                        for j in range(15): #resets all the cup colors and weights.
                            for k in range(12):
                                self.tray.itemconfig(self.samples[j][k], fill = "gray")
                                self.tray.itemconfig(self.sampletext[j][k], text = "0")
                        self.termflag = False #puts UI back in normal state after term routine is finished, then exits loop.
                        self.pauseflag = False
                        return
                if(self.termflag): #same as above, just for when the run is unpaused.
                    if(i > 2):
                        cmd = bytes('hh', 'utf-8')
                        try:
                            robot.write(cmd)
                        except serial.SerialException:
                            self.CommErrorFlag = True
                            return
                    for j in range(15): #resets all the cup colors and weights.
                        for k in range(12):
                            self.tray.itemconfig(self.samples[j][k], fill = "gray")
                            self.tray.itemconfig(self.sampletext[j][k], text = "0")
                    self.termflag = False
                    return
                #okay this is a bit complicated.
                #basically I have a "cmdstring" which is the current command I am sending to the robot.
                #The exact string changes based on the iterator i, but the default is the claw idle 'hh'.
                #0: move gantry in X direction
                #1: move gantry in Y direction
                #2: open claws
                #3: move tray up
                #4: close claws
                #5: move tray down
                #6: measure weights
                #7: move tray up
                #8: open claws
                #9: move tray down
                #10: close claws
                cmdstring = 'hh'
                xmove = xposarray[x] - xpos #tells the robot how many steps to move from current position.
                ymove = yposarray[y] - ypos #these only change when x and y get iterated.
                if(i == 0 and xmove == 0): #if the robot does not need to move in the x or y direction, tell iterator to skip that state.
                    i = 1

                if(i == 1 and ymove == 0):
                    i = 2

                if(i == 0): #handles whether the robot needs to move forward or backward in x direction and makes a command for how many steps to move.
                    if(xmove > 0):
                        cmdstring = 'i' + '{0:05d}'.format(xmove) #standard move commaand is 5 digits but can be made smaller by putting a letter at the end like 'i123h'
                    else:
                        xmove = -xmove #We need to make sure all the movement values are positive, this makes the xmove positive.
                        cmdstring = 'k' + '{0:05d}'.format(xmove)
                    xpos = xposarray[x] #after we make a move command we update the robot position *in the app* to reflect where we expect it to go.
                elif(i == 1): #same as x but for the y axis.
                    if(ymove > 0):
                        cmdstring = 'j' + '{0:05d}'.format(ymove)
                    else:
                        ymove = -ymove
                        cmdstring = 'l' + '{0:05d}'.format(ymove)
                    ypos = yposarray[y]
                elif(i == 2): #this turns on the claw solenoids.
                    cmdstring = 'yy'
                elif(i == 3):
                    if(zposarray[0] > 0):
                        cmdstring = 'u' + '{0:05f}'.format(zposarray[0])
                elif(i == 4):
                    cmdstring = 'hh'
                elif(i == 5):
                    if(zposarray[1] > 0):
                        cmdstring = 'o' + '{0:05f}'.format(zposarray[1])
                elif(i == 6): #this tells the robot to make a weight measurement.
                    cmdstring = 'zz'
                elif(i == 7):
                    if(zposarray[1] > 0):
                        cmdstring = 'u' + '{0:05f}'.format(zposarray[1])
                elif(i == 8):
                    cmdstring = 'yy'
                elif(i == 9):
                    if(zposarray[0] > 0):
                        cmdstring = 'o' + '{0:05f}'.format(zposarray[0])
                cmd = bytes(cmdstring, 'utf-8') #writes cmdstring to the UART buffer.
                try:
                    robot.write(cmd)
                except serial.SerialException:
                    self.CommErrorFlag = True
                    return
                time.sleep(.5) #Pause between each iteration to prevent robot from moving between states too quickly.
                try:
                    s = robot.read(1).decode('utf-8') #reads ACKS and data from robot.
                except serial.SerialException:
                    self.CommErrorFlag = True
                    return
                if(s != 'D'):
                    while(s != 'N'):
                        tmpstr += s
                        try:
                            s = robot.read(1).decode('utf-8') #reads ACKS and data from robot.
                        except serial.SerialException:
                            self.CommErrorFlag = True
                            return
                    celloutput = tmpstr.split()
                    tmpstr = ""
                    if(tareflags[0] == 1 and checkarray[0] == 1 and (cuparray[0] > 12*x + y)):
                        self.write_to_sample(x, y, round(abs(float(int(celloutput[0]) - zeroarray[0]) / tarearray[0]), 2)) #calls write to sample 5 times because there are 5 claws that make measurements.
                    if(tareflags[1] == 1 and checkarray[1] == 1 and (cuparray[1] > 12*x + y)):
                        self.write_to_sample(x+3, y, round(abs(float(int(celloutput[1]) - zeroarray[1]) / tarearray[1]), 2))
                    if(tareflags[2] == 1 and checkarray[2] == 1 and (cuparray[2] > 12*x + y)):
                        self.write_to_sample(x+6, y, round(abs(float(int(celloutput[2]) - zeroarray[2]) / tarearray[2]), 2))
                    if(tareflags[3] == 1 and checkarray[3] == 1 and (cuparray[3] > 12*x + y)):
                        self.write_to_sample(x+9, y, round(abs(float(int(celloutput[3]) - zeroarray[3]) / tarearray[3]), 2))
                    if(tareflags[4] == 1 and checkarray[4] == 1 and (cuparray[4] > 12*x + y)):
                        self.write_to_sample(x+12, y, round(abs(float(int(celloutput[4]) - zeroarray[4]) / tarearray[4]), 2))
                if(s == 'N'):
                    if(y >= 11): #after making a measurement we go to the next x or y based on what the current robot positon is.
                        x = x+1
                        y = 0
                    else:
                        y = y+1
                    if(x >= 3): #if we reach the end of a run we open claws and reset the robot.
                        cmd = bytes('hh', 'utf-8')
                        robot.write(cmd)
                        s = robot.read().decode('utf-8')
                        cmd = bytes('rr', 'utf-8')
                        robot.write(cmd)
                        self.doneFlag = True
                        return
                while(s != 'D'): #waits until robot ACK received before going to the next state. Robot ACKs after completing a command.
                    try:
                        s = robot.read(1).decode('utf-8')
                    except serial.SerialException:
                        self.CommErrorFlag = True
                        return
                i = i+1 #after each loop we go to the next state.
                if(i > 10): #go back to the first state if we reached last state.
                    i = 0

        #This sets up the popup GUI for Calibrating the load cells.
        def calibrate_cells(self):
            self.calibrate_popup = Calibrate(self)

        #This sets up the popup GUI for setup parameters.
        def setup_param(self):
            self.setup_popup = Setup(self) #since this is a separate GUI it needs a separate tk instance.


        #This sets up the popup GUI for maintenence parameters.
        def maintenance_param(self):
            self.maintenance_popup = Maintenance(self)

        #when the run button is pressed it begins a thread that handles the robot serial function.
        def run_button(self):
            self.doneFlag = False
            if((threading.active_count() <= 3) and not self.disconnected):
                serthread = threading.Thread(target = self.robotSer)
                serthread.start()

        def test_button(self):
            self.doneFlag = False
            if(threading.active_count() <= 3):
                testthread = threading.Thread(target = self.examplerun)
                testthread.start()

    app = App()
    app.mainloop()
