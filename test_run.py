'''
Author: Kaiyu Shi
Project: Microsoft Robotic Eyes Test Run Script
Description: This script serves as the primary control script for the Robotic Eyes Program. Click Run to hopefully test run the whole program.

Layout:
- communication between method by referencing variables from each module (all imported here on run). no need to pass arguments and return variables.
- refer to the software diagram for which variables to call

'''

#importing modules
import joystick_control
import display_to_screen
import save_servo_state
import user_interface
import coordinate_gen
import servo_control


#importing libraries
import time
import threading
import numpy


def program_run():
    while True:  # calibration mode

        if MODEFLAG:    #switch to mode
            break

    while True:  # feedforward control mode

    return





thread1 = threading.Thread(target=user_interface, args=())
thread2 = threading.Thread(target=program_run, args=())

thread1.start() #start threads
thread2.start()

thread1.join() #wait until both threads are complete
thread2.join()




