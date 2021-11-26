# Autoweigh UI
 UI for the Automated soil weighing robot.

# What is this code?
This is the UI for the Automated Soil Weighing System Robot nicknamed Autoweigh 2020.
 It consists of 4 main parts:
 1. There is a main menu which controls weight data collection and displays it to the screen.
 2. There is a calibration menu for calibrating the load cells on the robot.
 3. There is a setup parameters menu for setting the alphanumeric code of each output file and number of trays and number of cups.
 4. There is a maintenance parameters menu for setting the locations of each cup and setting the weight bounds and colors displayed for each weight bound on the UI.

# How do I run this code?
There are two ways to run this code.
1. Run the "UI-Full.exe" file in the dist folder. This is a standalone executable and I believe should not require any python dependencies. It must be recompiled via py2exe if any edits to the source code are made.
2. Run the "UI-Full.py" file in the Autoweigh-UI folder. This is a python script file which requires several dependencies in order to run. However, it can be run immediately upon any changes being made; it does not need to be recompiled.

# How do I recompile this code?
You must have python 3 and py2exe installed on your computer to recompile the code. Once you have these installed, as well as the required dependencies (pyserial and tkinter) you can recompile the code by deleting the dist folder and then running "python setup.py py2exe" in the command line in the Autoweigh-UI folder.

# Questions?
If you have questions concerning modification or fixing of this code, contact Katherine Farrelly at KatFarrelly@protonmail.com. I am aware this readme is a bit barebones so if anything is unclear I will try to help the best I can to clarify.
As of 11/26/2021 I am no longer regularly maintaining this code. I will only respond to reports of critical bug fixes or feature requirements by the NC Agronomics Division.
