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
import generate_map
import feedforward_control

#importing libraries
import time
import threading
import numpy

def program_run():
    while True:  # calibration mode
        if MODEFLAG:   #calibration mode
            coordinate_gen()        #generates current target coordinate
            display_to_screen()     #shows it on the screen
            joystick_control()      #set the current target servo positions
            servo_control()         #move servos to positions
            save_servo_state()      #save to array if ENTERFLAG is on
            generate_map()       #generates the interpolated map if the is filled up


        else:    #feedforward mode
            joystick_control()      #set current target screen coordinates
            feedforward_control()   #convert target coordinates to servo positions
            servo_control()         #move servos to positions
            display_to_screen()     #display target coordinates on screen for comparison
    return


thread1 = threading.Thread(target=user_interface, args=())
thread2 = threading.Thread(target=program_run, args=())

thread1.start() #start threads
thread2.start()

thread1.join() #wait until both threads are complete
thread2.join()




