'''
Author: Kaiyu Shi
Project: Microsoft Robotic Eyes Test Run Script
Description: This script serves as the primary control script for the Robotic Eyes Program. Click Run to hopefully test run the whole program.
'''

#importing modules
import joystickControl
import displayToScreen
import saveServoState
import userInterface
import getCalibrationCoordinates
import ServoControl


#importing libraries
import time
import threading
import numpy

def run():
    while True:  # calibration mode

    if SOMETHING:
        break

    while True:  # feedforward control mode

    return


thread1 = threading.Thread(target=userInterface, args=(10,))
thread2 = threading.Thread(target=run, args=(10,))


thread1.start() #start threads
thread2.start()

thread1.join() #wait until both threads are complete
thread2.join()




