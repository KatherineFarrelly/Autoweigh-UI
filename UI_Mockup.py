#ECE 485 Soil Robot GUI Program
#Written by Katherine Farrelly, Matthew Kelly, Steven Moore, Jonathan Medju
#This program is the entire Laptop/GUI side of the Soil Weighing robot.
#It handles robot communications, displaying of data, and control of the robot.
#It also handles file output of the robot data.

#importing all the libraries. Of note are serial and tkinter.
import sys
import tkinter as tk
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
    xposarray = [0, 1270, 2600]
    yposarray = [0, 1440, 2880, 4390, 5900, 7410, 8920, 10430, 11920, 13470, 14980, 16590]

    class Setup(tk.Toplevel):
        def __init__(self, master):
            super().__init__(master)
            self.master = master
            self.wm_title("Setup Parameters")
            self.geometry("800x360")
            self.buttonfont = "Helvetica 24"

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
            #alphanumberic codes for the runs that can be chosen.
            optionList = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
            self.v = tk.StringVar(self)
            self.v.set(optionList[0]) #optionlist that you should be able to type into hopefully.

            #setup GUI section for the alphanumeric code entering.
            self.label = tk.Label(self,  text='Select Tray Labelling:', font = self.buttonfont)
            self.label.grid(column=0, row=0) #All of this GUI is setup as a grid.

            self.alphabetical = tk.OptionMenu(self, self.v, *optionList)
            self.alphabetical.config(font = self.buttonfont)
            self.alphabetical.grid(column=1, row=0)

            #setup all the entry forms and radio buttons for the number of trays and number of cups per tray.
            self.traylabel1 = tk.Label(self,  text='Select Tray Numbering:', font = self.buttonfont)
            self.traylabel1.grid(column=0, row=1)
            self.tray1 = tk.Entry(self, font = self.buttonfont, textvariable = self.setentry1)
            self.tray1.grid(column=1, row=1)
            self.checktray1 = tk.Checkbutton(self, variable= self.setcheck1)
            self.checktray1.grid(column=2, row=1)

            self.traylabel2 = tk.Label(self,  text='Select Tray Numbering:', font = self.buttonfont)
            self.traylabel2.grid(column=0, row=2)
            self.tray2 = tk.Entry(self, font = self.buttonfont,textvariable = self.setentry2)
            self.tray2.grid(column=1, row=2)
            self.checktray2 = tk.Checkbutton(self, variable= self.setcheck2)
            self.checktray2.grid(column=2, row=2)

            self.traylabel3 = tk.Label(self,  text='Select Tray Numbering:', font = self.buttonfont)
            self.traylabel3.grid(column=0, row=3)
            self.tray3 = tk.Entry(self, font = self.buttonfont, textvariable = self.setentry3)
            self.tray3.grid(column=1, row=3)
            self.checktray3 = tk.Checkbutton(self, variable= self.setcheck3)
            self.checktray3.grid(column=2, row=3)

            self.traylabel4 = tk.Label(self,  text='Select Tray Numbering:', font = self.buttonfont)
            self.traylabel4.grid(column=0, row=4)
            self.tray4 = tk.Entry(self, font = self.buttonfont, textvariable = self.setentry4)
            self.tray4.grid(column=1, row=4)
            self.checktray4 = tk.Checkbutton(self, variable= self.setcheck4)
            self.checktray4.grid(column=2, row=4)

            self.traylabel5 = tk.Label(self,  text='Select Tray Numbering:', font = self.buttonfont)
            self.traylabel5.grid(column=0, row=5)
            self.tray5 = tk.Entry(self, font = self.buttonfont, textvariable = self.setentry5)
            self.tray5.grid(column=1, row=5)
            self.checktray5 = tk.Checkbutton(self, variable= self.setcheck5)
            self.checktray5.grid(column=2, row=5)

            #apply setup parameters.
            self.okay = tk.Button(self, font = self.buttonfont)
            self.okay["text"] = "Apply"
            self.okay.grid(column=1,row=6)

    class Maintenance(tk.Toplevel):
        def __init__(self, master):
            super().__init__(master)
            self.master = master
            self.wm_title("Maintenance Parameters")
            self.geometry("1500x360")
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

            self.buttonfont = "Helvetica 24"

            self.create_widgets()

        def create_widgets(self):
            #setup GUI section for the alphanumeric code entering.
            self.xlab = tk.Label(self,  text='X Positions', font = self.buttonfont)
            self.xlab.grid(column=0, row=0)
            self.xpos1 = tk.Entry(self, font = self.buttonfont, textvariable = self.xposi0)
            self.xpos1.insert('0', xposarray[0])
            self.xpos1.grid(column=1, row=0)
            self.xpos2 = tk.Entry(self, font = self.buttonfont, textvariable = self.xposi1)
            self.xpos2.insert('0', xposarray[1])
            self.xpos2.grid(column=2, row=0)
            self.xpos3 = tk.Entry(self, font = self.buttonfont, textvariable = self.xposi2)
            self.xpos3.insert('0', xposarray[2])
            self.xpos3.grid(column=3, row=0)

            self.ylab1 = tk.Label(self,  text='Y Positions 1-3', font = self.buttonfont)
            self.ylab1.grid(column=0, row=1)
            self.ypos1 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi0)
            self.ypos1.insert('0', yposarray[0])
            self.ypos1.grid(column=1, row=1)
            self.ypos2 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi1)
            self.ypos2.insert('0', yposarray[1])
            self.ypos2.grid(column=2, row=1)
            self.ypos3 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi2)
            self.ypos3.insert('0', yposarray[2])
            self.ypos3.grid(column=3, row=1)

            self.ylab2 = tk.Label(self,  text='Y Positions 4-6', font = self.buttonfont)
            self.ylab2.grid(column=0, row=2)
            self.ypos4 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi3)
            self.ypos4.insert('0', yposarray[3])
            self.ypos4.grid(column=1, row=2)
            self.ypos5 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi4)
            self.ypos5.insert('0', yposarray[4])
            self.ypos5.grid(column=2, row=2)
            self.ypos6 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi5)
            self.ypos6.insert('0', yposarray[5])
            self.ypos6.grid(column=3, row=2)

            self.ylab3 = tk.Label(self,  text='Y Positions 7-9', font = self.buttonfont)
            self.ylab3.grid(column=0, row=3)
            self.ypos7 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi6)
            self.ypos7.insert('0', yposarray[6])
            self.ypos7.grid(column=1, row=3)
            self.ypos8 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi7)
            self.ypos8.insert('0', yposarray[7])
            self.ypos8.grid(column=2, row=3)
            self.ypos9 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi8)
            self.ypos9.insert('0', yposarray[8])
            self.ypos9.grid(column=3, row=3)

            self.ylab4 = tk.Label(self,  text='Y Positions 10-12', font = self.buttonfont)
            self.ylab4.grid(column=0, row=4)
            self.ypos10 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi9)
            self.ypos10.insert('0', yposarray[9])
            self.ypos10.grid(column=1, row=4)
            self.ypos11 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi10)
            self.ypos11.insert('0', yposarray[10])
            self.ypos11.grid(column=2, row=4)
            self.ypos12 = tk.Entry(self, font = self.buttonfont, textvariable = self.yposi11)
            self.ypos12.insert('0', yposarray[11])
            self.ypos12.grid(column=3, row=4)

            #apply setup parameters.
            self.okay = tk.Button(self, font = self.buttonfont)
            self.okay["text"] = "Apply"
            self.okay["command"] = self.set_maintenance
            self.okay.grid(column=0,row=5)
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


    class App(tk.Tk):
        def quitout(self):
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
                        if(not robot.is_open and self.disconnected): #attempt to connect or reconnect
                            robot.port = it.device #sets port number to Arduino's port.
                            robot.baudrate = 9600 #sets baud rate. This can be a constant.
                            robot.open() #opens the serial port. This function only opens if the port is valid and not in use.
                            self.disconnected = False
                            self.connect.configure(text = "Connected", bg = "green")
                if(not self.arduinoflag): #device was disconnected, update status.
                    robot.close()
                    self.disconnected = True
                    self.connect.configure(text = "Disconnected", bg = "red")
                time.sleep(1)
            robot.close()

        def __init__(self): #Initializes the main GUI
            super().__init__()
            self.create_widgets()
            #similar to global variables
            self.pauseflag = False #These are two flag variables I use to handle the program state.
            self.termflag = False #Currently the 3 states are normal, paused, and terminate run.
            self.disconnected = True #this variable determines if the robot is connected or not. This is so we are safe from communication errors.
            self.protocol("WM_DELETE_WINDOW", self.quitout)



        def create_widgets(self): #Creates all the buttons and Visual stuff.
            self.killThreads = False

            #GUI size and fonts
            self.tray = tk.Canvas(self, width = "1000", height = "900")
            self.tray.pack()
            self.buttonfont = "Helvetica 24"
            self.buttonfontmain = "Helvetica 36"

            #here are all the buttons
            self.run = tk.Button(self, font = self.buttonfont)
            self.run["text"] = "Run"
            self.run["command"] = self.run_button
            self.run.place(x = 5, y = 700)

            self.pause = tk.Button(self, font = self.buttonfont)
            self.pause["text"] = "Pause"
            self.pause["command"] = self.pause_button
            self.pause.place(x = 105, y = 700)

            self.terminate = tk.Button(self, font = self.buttonfont)
            self.terminate["text"] = "Terminate"
            self.terminate["command"] = self.term_button
            self.terminate.place(x = 235, y = 700)

            self.calibrate = tk.Button(self, font = self.buttonfont)
            self.calibrate["text"] = "Calibrate"
            self.calibrate["command"] = self.term_button
            self.calibrate.place(x = 415, y = 700)

            self.testrun = tk.Button(self, font = self.buttonfont)
            self.testrun["text"] = "Test Run"
            self.testrun["command"] = self.test_button
            self.testrun.place(x = 580, y = 700)

            self.connect = tk.Button(self, font = self.buttonfont)
            self.connect["text"] = "Disconnected"
            self.connect["bg"] = "red"
            self.connect.place(x = 750, y = 700)

            self.maintenance = tk.Button(self, font = self.buttonfont)
            self.maintenance["text"] = "Maintenance"
            self.maintenance["command"] = self.maintenance_param
            self.maintenance.place(x = 5, y = 800)

            self.setup = tk.Button(self, font = self.buttonfont)
            self.setup["text"] = "Setup Parameters"
            self.setup["command"] = self.setup_param
            self.setup.place(x = 230, y = 800)

            self.write = tk.Button(self, font = self.buttonfont)
            self.write["text"] = "Write to File"
            self.write["command"] = self.write_to_file
            self.write.place(x = 520, y = 800)

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
                    self.samples[x][y] = self.tray.create_oval((200 * math.floor(x/3)) + (55 * (x % 3)) + 5, 55 * y + 5, (200 * math.floor(x/3)) + (55 * (x % 3)) + 55, 55 * y + 55, fill = "gray")
                    self.sampletext[x][y] = self.tray.create_text((200 * math.floor(x/3)) + (55 * (x % 3)) + 30, 55 * y + 30, text = "0", justify = tk.CENTER, font = "Helvetica 16")
                    self.sampleweight[x][y] = 0
            autoneg = threading.Thread(target = self.autoneg)
            autoneg.start()

        def write_to_file(self):
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
        def write_to_sample(self, x, y): #takes x and y position in array as parameters.
            weight = round(random.gauss(50, 5), 2) #generates a random number based on gaussian distribution.
            color = "green"
            if weight < 45: #oh yeah these weight comparison values also should not be constants.
                color = "red"
            elif weight > 55:
                color = "blue"
            self.tray.itemconfig(self.samples[x][y], fill = color) #Write color to array.
            self.tray.itemconfig(self.sampletext[x][y], text = str(weight)) #Write weight to array.
            self.sampleweight[x][y] = weight

        def data_output(self):
            #First we create a text file with proper formatting to be written to.
            now = datetime.now() #Gets the date and time
            dt = now.strftime("%y_%m_%d Time_%Hh%Mm%Ss") #Formats dte and time for filename purposes
            traytxt1 = "AA" #Initial tray of the run. Temporary variable: should be replaced with traytxt from setup parameters
            tray1 = traytxt1 #String that holds tray alphanumerics
            tray2 = "AB" #These trays are just examples. Each one should have its own corresponding traytxt(number) derived from the setup parameters
            tray3 = "AC"
            tray4 = "AD"
            tray5 = "AE"
            cupnumber = 1 #Initial cup of the run. Temporary variable: Should be replaced with cupnumber from setup parameters
            cup = '{0:05d}'.format(cupnumber) #Formats cup number properly
            filename = tray1 + cup + "_" + dt + ".txt" #collates the information into the proper file name
            file = open(r"./Data_Testing/"+filename, "w") #Creates a file with the correct name
            file.write("***********************************\n") #This and the next few lines create the header for the text file
            file.write("        Weight Data File\n")
            file.write("***********************************\n")
            file.write("\n")
            file.write("Sample, Weight\n")
            file.write("\n")
            for x in range(3): #These for loops iterate over the sampletext matrix,
                for y in range(12):
                    file.write(tray1 + cup + ",  " + str(self.sampleweight[x][y]) + "\n")
                    cupnumber = cupnumber + 1
                    cup = '{0:05d}'.format(cupnumber)
            for x in range(3, 6):
                for y in range(12):
                    file.write(tray2 + cup + ",  " + str(self.sampleweight[x][y]) + "\n")
                    cupnumber = cupnumber + 1
                    cup = '{0:05d}'.format(cupnumber)
            for x in range (6, 9):
                for y in range(12):
                    file.write(tray3 + cup + ",  " + str(self.sampleweight[x][y]) + "\n")
                    cupnumber = cupnumber + 1
                    cup = '{0:05d}'.format(cupnumber)
            for x in range(9, 12):
                for y in range(12):
                    file.write(tray4 + cup + ",  " + str(self.sampleweight[x][y]) + "\n")
                    cupnumber = cupnumber + 1
                    cup = '{0:05d}'.format(cupnumber)
            for x in range (12, 15):
                for y in range(12):
                    file.write(tray5 + cup + ",  " + str(self.sampleweight[x][y]) + "\n")
                    cupnumber = cupnumber + 1
                    cup = '{0:05d}'.format(cupnumber)

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
                self.write_to_sample(x, y) #calls write to sample 5 times because there are 5 claws that make measurements.
                self.write_to_sample(x+3, y)
                self.write_to_sample(x+6, y)
                self.write_to_sample(x+9, y)
                self.write_to_sample(x+12, y)
                time.sleep(.1)
                x = x+1
                if(x > 2):
                    x = 0
                    y = y+1
                if(y > 11):
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
            robot.reset_input_buffer() #This flushes the serial buffer.
            cmd = bytes('rr', 'utf-8') #all UART communications must be made as UTF-8 encoded byte strings. This command resets the robot.
            robot.write(cmd) #Write to serial buffer.

            s = robot.read().decode('utf-8') #wait until robot makes a reply, basically. 'D' is our ACK character.

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
                            robot.write(cmd)
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
                        robot.write(cmd)
                    for j in range(15): #resets all the cup colors and weights.
                        for k in range(12):
                            self.tray.itemconfig(self.samples[j][k], fill = "gray")
                            self.tray.itemconfig(self.sampletext[j][k], text = "0")
                    self.termflag = False
                    return
                #okay this is a bit complicated.
                #basically I have a "cmdstring" which is the current command I am sending to the robot.
                #The exact string changes based on the iterator i, but the default is the claw idle 'hh'.
                #List of states currently in app:
                #0: move gantry in X direction
                #1: move gantry in Y direction
                #2: close claws
                #3: measure weights
                #4: open claws
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
                elif(i == 3): #this tells the robot to make a weight measurement.
                    cmdstring = 'nn'
                cmd = bytes(cmdstring, 'utf-8') #writes cmdstring to the UART buffer.
                robot.write(cmd)
                time.sleep(.5) #Pause between each iteration to prevent robot from moving between states too quickly.

                s = robot.read().decode('utf-8') #reads ACKS and data from robot.
                if(s == 'N'): #right now 'N' stands for "I got data!" This needs to be changed so that the app can collect actual numerical data sent by the robot.
                    self.write_to_sample(x, y) #calls write to sample 5 times because there are 5 claws that make measurements.
                    self.write_to_sample(x+3, y)
                    self.write_to_sample(x+6, y)
                    self.write_to_sample(x+9, y)
                    self.write_to_sample(x+12, y)
                    if(x >= 2): #after making a measurement we go to the next x or y based on what the current robot positon is.
                        y = y+1
                        x = 0
                    else:
                        x = x+1
                    if(y >= 12): #if we reach the end of a run we open claws and reset the robot.
                        cmd = bytes('hh', 'utf-8')
                        robot.write(cmd)
                        s = robot.read().decode('utf-8')
                        cmd = bytes('rr', 'utf-8')
                        robot.write(cmd)
                        return
                while(s != 'D'): #waits until robot ACK received before going to the next state. Robot ACKs after completing a command.
                    s = robot.read().decode('utf-8')
                i = i+1 #after each loop we go to the next state.
                if(i > 4): #go back to the first state if we reached last state.
                    i = 0

        #This sets up the popup GUI for setup parameters.
        def setup_param(self):
            self.setup_popup = Setup(self) #since this is a separate GUI it needs a separate tk instance.


        #This sets up the popup GUI for maintenence parameters.
        def maintenance_param(self):
            self.maintenance_popup = Maintenance(self)

        #when the run button is pressed it begins a thread that handles the robot serial function.
        def run_button(self):
            if((threading.active_count() <= 2) and not self.disconnected):
                serthread = threading.Thread(target = self.robotSer)
                serthread.start()

        def test_button(self):
            if(threading.active_count() <= 2):
                testthread = threading.Thread(target = self.examplerun)
                testthread.start()

    app = App()
    app.mainloop()
