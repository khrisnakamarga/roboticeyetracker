# Robotic Test Rig for Eye Trackers
This repository contains Python scripts to control the Servo motors in the Eye Tracker Test Rig developed by Microsoft
and MATLAB scripts that plots the response of the Servo motors.

# Working Scripts
..* RoboticEyesController.py - uses the keyboard to control the movement of the test rig's component
..* RoboticEyesControllerTESTCOPY.py - performs gaze calibraion with the keyboard
..* XboxController.py - uses the xbox controller to control the movement of the test rig's component, visualizes the control
..* display_to_screen.py - calibration dots

# Microsoft Demo
The Microsoft Demo folder contains the scripts necessary to calibrate the Eye Test Rig, then performing feed forward control to tell the robot to stare at a certain spot on the screen.

To do so:
1. Connect the power sources and connect the Pololu board to the computer
2. Run XboxControl.py
3. Guide the Eye Test Rig to the specific calibration dots
4. Press RB and advance to the next position
5. Press start after all the calibration dots are hit
6. Use the methods to instruct the test rig to stare at the screen
